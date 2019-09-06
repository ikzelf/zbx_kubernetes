#!/usr/bin/env python
"""Usage zbx_k8s_metrics.py host server port
"""
# should work with python 2.7.14 and 3
from __future__ import print_function
import json
import subprocess
import sys
import time


def to_bytes(s):
    munit = s[-2:]
    count = s[:-2]

    if munit.isdigit():
        munit = "bytes"
        count = s

    if munit == "bytes":
        bytess = count
    elif munit == "Ki":
        bytess = int(count) * 1024
    elif munit == "Mi":
        bytess = int(count) * 1024 * 1024
    elif munit == "Gi":
        bytess = int(count) * 1024 * 1024 * 1024
    elif munit == "Ti":
        bytess = int(count) * 1024 * 1024 * 1024 * 1024
    elif munit == "Pi":
        bytess = int(count) * 1024 * 1024 * 1024 * 1024 * 1024
    elif munit == "Ei":
        bytess = int(count) * 1024 * 1024 * 1024 * 1024 * 1024 * 1024

    return bytess

def to_cpus(s):
    cunit = s[-1:]
    ccount = s[:-1]


    if cunit.isdigit():
        cunit = "cpu"
        ccount = s

    if cunit == "m":
        cpus = int(ccount) * 0.001
    else:
        cpus = int(ccount)

    return cpus

if len(sys.argv[1:]) < 3:
    print("Usage {} zabbix_host zabbix_server zabbix_server_port".format(
        sys.argv[0]), file=sys.stderr)
    sys.exit(1)
zabbix_server_port = sys.argv[3]
zabbix_server = sys.argv[2]
zabbix_host = sys.argv[1]
data = ""
process = subprocess.Popen(["kubectl get --raw /apis/metrics.k8s.io/v1beta1/pods"],
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           close_fds=True)
exit_code = process.wait()

if exit_code == 0:
    data = json.loads(process.stdout.read().decode())
err = process.stderr.read().decode()

containers = []

if data:
    # print(data["kind"])
    timestamp = int(time.time())

    process = subprocess.Popen(["zabbix_sender -z {} -p {} -T -i - -r -vv"
                                .format(zabbix_server, zabbix_server_port)],
                               shell=True,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               close_fds=True)

    for i in data["items"]:
        # print("item:{}".format(i))
        # print("item.metadata:{}".format(i['metadata']))
        # print("item.containers:{}".format(i['containers']))
        pod = i['metadata']['name']
        namespace = i['metadata']['namespace']

        for c in i["containers"]:
            memory = c['usage']['memory']
            bytess = to_bytes(memory)

            cpu = c['usage']['cpu']
            cpus = to_cpus(cpu)

            msg="{} \"ns[{}] name[{}] container[{}] memory\" {} {}".format(
                zabbix_host, namespace, pod, c['name'], str(timestamp),
                bytess)
            process.stdin.write(msg.encode())
            msg = "{} \"ns[{}] name[{}] container[{}] cpu\" {} {}".format(
                zabbix_host, namespace, pod, c['name'], str(timestamp),
                cpus)
            process.stdin.write(msg.encode())

    res = process.communicate()[0].decode()
    print("results zabbix_sender: {}".format(res))
    exit_code = process.wait()
    print("zabbix_sender exit_code: {}".format(exit_code))

    err = ""
    try:
        err = process.stderr.read().decode()
    except ValueError as e:
        print("zabbix_sender error msg: {}".format(err), file=sys.stderr)
    output = ""
    try:
        output = process.stdout.read().decode()
    except ValueError as e:
        print("zabbix_sender output msg: {}".format(output))

else:
    print(err, file=sys.stderr)

sys.exit(exit_code)
