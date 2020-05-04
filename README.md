# Helm template for Python Locust
This template for use load testing with python locust library.  
We defind python base to Kubernetes resources that on a-Master-to-many-slave.  
In this use Deployment on same master and slave to replicas

## Architectures
1 Master replicas  
N Slave replicas (Init in 2 replicas.)  
It can spawn replicas on slave value up to your resource.  

## How to use
Deploy with helm version 2 or 3 like:  
```bash
$ helm install -i locust --set "targets.url=<your service url-base>" -f values.yaml ./
```
Then, your resource can work normally open your browser and connect with ingress url  
configure in value file like this.  
```yaml
ingress:
  enabled: true
  annotations:
    ingress.kubernetes.io/ingress.class: nginx
    ingress.kubernetes.io/rewrite-traget: /
    ingress.kubernetes.io/ssl-redirect: "false"
  hosts:
    - host: load-test.k8s.opsta.in.th
      paths: ["/"]
  tls: []
```
In browser you can config user's configure with following.
1. `Number of user to simulate`  
It same user concurrency to send request and recieve response in times.
1. `Hatch rate`  
It number of user's spawn rate for simulate load creation.
1. `Host`  
It url base without "/" for inject to request script.
  
Finally click `start swarming` to start load testing.