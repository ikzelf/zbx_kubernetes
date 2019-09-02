# zbx_kubernetes
zbx_k8s_lls.py returns a zabbix lld array containing for example:
```{"data":
[
  { 
     "{#NAME}": "coredns-5c98db65d4-62sdx"
  ,  "{#NAMESPACE}": "kube-system"
  ,  "{#CONTAINER}": "coredns"
  }
  , {
      "{#NAME}": "coredns-5c98db65d4-z8mlp"
  ,   "{#NAMESPACE}": "kube-system"
  ,   "{#CONTAINER}": "coredns"
  }
  , {
       "{#NAME}": "etcd-minikube"
  ,    "{#NAMESPACE}": "kube-system"
  ,    "{#CONTAINER}": "etcd"
  }
 ]
}```
