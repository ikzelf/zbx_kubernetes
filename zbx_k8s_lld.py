#!/usr/bin/env python
# should work with python 2.7 and 3
from __future__ import print_function
import json
import platform
import subprocess
import sys

data = ""
cmd = "kubectl get pod -o=custom-columns=NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName  --all-namespaces -o json"

if int(platform.python_version().split('.')[0]) < 3:
    msg = cmd.decode()
else:
    msg = cmd
process = subprocess.Popen( [msg],
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           close_fds=True)
(out, err) = process.communicate()
exit_code = process.wait()

if exit_code == 0:
    data = json.loads(out)
    # data = json.loads(process.stdout.read().decode())

containers = []

if data:

    for i in data["items"]:

        for c in i["spec"]["containers"]:
            e = {"{#NAME}": i["metadata"]["name"], "{#NAMESPACE}":
                    i["metadata"]["namespace"], "{#CONTAINER}": c["name"],
                    "{#NODE}": i["spec"]["nodeName"]}
            containers.append(e)

    print("{\"data\":"+json.dumps(containers)+"}")
else:
    print(err, file=sys.stderr)

sys.exit(exit_code)
