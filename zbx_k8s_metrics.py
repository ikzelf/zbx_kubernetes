#!/usr/bin/env python
# should work with python 2.7 and 3
import json
import subprocess
import sys
import time

if len(sys.argv[1:]) < 2:
    print("Usage {} zabbix_host zabbix_server".format(sys.argv[0]), file=sys.stderr)
    sys.exit(1)
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

    for i in data["items"]:
        # print("item:{}".format(i))
        # print("item.metadata:{}".format(i['metadata']))
        # print("item.containers:{}".format(i['containers']))
        pod = i['metadata']['name']
        namespace = i['metadata']['namespace']

        for c in i["containers"]:
            memory = c['usage']['memory']
            munit = memory[-2:]
            count = memory[:-2]

            cpu = c['usage']['cpu']
            cunit = cpu[-1:]
            ccount = cpu[:-1]

            if munit.isdigit():
                munit = "bytes"
                count = memory

            if cunit.isdigit():
                cunit = "cpu"
                ccount = cpu

            if munit == "bytes":
                bytess = count
            elif munit == "Ki":
                bytess = int(count) * 1024
            elif munit == "Mi":
                bytess = int(count) * 1024 * 1024
            elif munit == "Gi":
                bytess = int(count) * 1024 * 1024 * 1024

            if cunit == "m":
                cpus = int(ccount) * 0.001
            else:
                cpus = int(ccount)

            print("{} \"ns[{}] name[{}] container[{}] memory\" {} {}".format(
                zabbix_host, namespace, pod, c['name'], str(timestamp),
                bytess))
            print("{} \"ns[{}] name[{}] container[{}] cpu\" {} {}".format(
                zabbix_host, namespace, pod, c['name'], str(timestamp),
                cpus))

else:
    print(err, file=sys.stderr)

sys.exit(exit_code)
