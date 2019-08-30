#!/usr/bin/env python
# should work with python 2.7 and 3
import json
import subprocess

process = subprocess.Popen(["kubectl get pods -o json"],
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           close_fds=True)
data = process.stdout.read().decode()
err = process.stderr.read().decode()
exit_code = process.wait()
# with open("get_pods.json","r") as readfile:
    # data = json.load(readfile)

containers = []
# print(data)

for i in data["items"]:
    # print("{} {} {:>5} {}".format(
        # i["kind"],
        # i["metadata"]["namespace"],
        # i["metadata"]["resourceVersion"],
        # i["metadata"]["name"]
        # ))

    for c in i["spec"]["containers"]:
        e = {"{#NAME}": i["metadata"]["name"], "{#NAMESPACE}":
                i["metadata"]["namespace"], "{#CONTAINER}": c["name"]}
        # print("    {} {}".format(c["name"],c["image"]))
        containers.append(e)

# print(containers)
print("{\"data\":"+json.dumps(containers)+"}")
