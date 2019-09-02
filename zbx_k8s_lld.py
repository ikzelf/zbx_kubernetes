#!/usr/bin/env python
# should work with python 2.7 and 3
import json
import subprocess
import sys

data = ""
process = subprocess.Popen(["kubectl get pods -o json"],
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           close_fds=True)
exit_code = process.wait()

if exit_code == 0:
    data = json.loads(process.stdout.read().decode())
err = process.stderr.read().decode()
# with open("get_pods.json","r") as readfile:
    # data = json.load(readfile)

containers = []

if data:
    for i in data["items"]:

        for c in i["spec"]["containers"]:
            e = {"{#NAME}": i["metadata"]["name"], "{#NAMESPACE}":
                    i["metadata"]["namespace"], "{#CONTAINER}": c["name"]}
            containers.append(e)

    print("{\"data\":"+json.dumps(containers)+"}")
else:
    print(err, file=sys.stderr)

sys.exit(exit_code)
