#!/usr/bin/env python
# should work with python 2.7 and 3
import json
import subprocess
import sys

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
print()

if data:
    for i in data["items"]:
        # print("item:{}".format(i))
        # print("item.metadata:{}".format(i['metadata']))
        # print("item.containers:{}".format(i['containers']))
        pod = i['metadata']['name']
        namespace = i['metadata']['namespace']

        for c in i["containers"]:
            print("pod {} ns {} container {} usage {}".format(pod, namespace, c['name'], c['usage']))

else:
    print(err, file=sys.stderr)

sys.exit(exit_code)
