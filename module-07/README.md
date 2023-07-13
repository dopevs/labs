## Kubernetes user creation doc
This doc will follow through how to create k8s user dave and generate config for the user dave.

### Creation of a Private Key and a Certificate Signing Request (CSR)
Dave first needs to generate a private rsa key and a CSR. The private key can easily be created with this command:
```bash
$ openssl genrsa -out dave.key 4096
..................................................................................................................++++
.............................................................++++
e is 65537 (0x10001)
```
```bash
openssl req -new -key dave.key -out dave.csr -subj "/CN=dave"
```
### Signature of the CSR
We will use the following specification and save it in csr.yaml.
```yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: mycsr
spec:
  groups:
  - system:authenticated
  request: ${BASE64_CSR}
  signerName: kubernetes.io/kube-apiserver-client
  expirationSeconds: 315569260
  usages:
  - digital signature
  - key encipherment
  - client auth
```
```bash
# Encoding the .csr file in base64
$ export BASE64_CSR=$(cat ./dave.csr | base64 | tr -d '\n')
```
```bash
# Substitution of the BASE64_CSR env variable and creation of the CertificateSigninRequest resource
$ cat csr.yaml | envsubst | kubectl apply -f -
certificatesigningrequest.certificates.k8s.io/mycsr created
```
Checking the status of the newly created CSR, we can see it’s in Pending state.
```bash
$ kubectl get csr
NAME    AGE   SIGNERNAME                            REQUESTOR            REQUESTEDDURATION   CONDITION
mycsr   3s    kubernetes.io/kube-apiserver-client   docker-for-desktop   10y                 Pending
```
We can then approve this CSR with this command:
```bash
$ kubectl certificate approve mycsr
certificatesigningrequest.certificates.k8s.io/mycsr approved
```
Checking the status of the CSR once again, we can see it’s now approved.
```bash
$ kubectl get csr
NAME    AGE   SIGNERNAME                            REQUESTOR            REQUESTEDDURATION   CONDITION
mycsr   14s   kubernetes.io/kube-apiserver-client   docker-for-desktop   10y                 Approved,Issued
```
Let’s just extract it from the CSR resource and save it in a file named dave.crt to check what’s inside.
```bash
$ kubectl get csr mycsr -o jsonpath='{.status.certificate}' \
  | base64 --decode > dave.crt
```
### Creation of a Namespace
```bash
$ kubectl create ns development
namespace/development created
```

### Creation of a Role
```yaml
# role.yaml
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
 namespace: development
 name: dev
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["create", "get", "update", "list", "delete"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["create", "get", "update", "list", "delete"]
```
### Creation of a RoleBinding
```yaml
# rolebinding.yaml
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
 name: dev
 namespace: development
subjects:
- kind: User
  name: dave
  apiGroup: rbac.authorization.k8s.io
roleRef:
 kind: Role
 name: dev
 apiGroup: rbac.authorization.k8s.io
```
```bash
$ kubectl apply -f role.yaml
role.rbac.authorization.k8s.io/dev created
```
```bash
$ kubectl apply -f rolebinding.yaml
rolebinding.rbac.authorization.k8s.io/dev created
```
### Building a Kube Config for Dave
We’ll first create a kubeconfig.tpl file, with the following content, that we’ll use as a template.
```yaml
# kubconfig.tpl
apiVersion: v1
kind: Config
clusters:
- cluster:
    certificate-authority-data: ${CLUSTER_CA}
    server: ${CLUSTER_ENDPOINT}
  name: ${CLUSTER_NAME}
users:
- name: ${USER}
  user:
    client-certificate-data: ${CLIENT_CERTIFICATE_DATA}
contexts:
- context:
    cluster: ${CLUSTER_NAME}
    user: dave
  name: ${USER}-${CLUSTER_NAME}
current-context: ${USER}-${CLUSTER_NAME}
```
To build a base kube config from this template, we first need to set all the needed environment variables:
```bash
# User identifier
$ export USER="dave"
# Cluster Name (get it from the current context)
$ export CLUSTER_NAME=$(kubectl config view --minify -o jsonpath={.current-context})
# Client certificate
$ export CLIENT_CERTIFICATE_DATA=$(kubectl get csr mycsr -o jsonpath='{.status.certificate}')
# Cluster Certificate Authority
$ export CLUSTER_CA=$(kubectl config view --raw -o json | jq -r '.clusters[] | select(.name == "'$(kubectl config current-context)'") | .cluster."certificate-authority-data"')
# API Server endpoint
$ export CLUSTER_ENDPOINT=$(kubectl config view --raw -o json | jq -r '.clusters[] | select(.name == "'$(kubectl config current-context)'") | .cluster."server"')
```
and substitute them using, once again, the convenient `envsubst` utility:
```bash
$ cat kubeconfig.tpl | envsubst > kubeconfig
```
### Use of the Context
```bash
$ export KUBECONFIG=$PWD/kubeconfig
```
To add the private key, `dave.key` generated at the beginning of the process, Dave can use this command:
```bash
kubectl config set-credentials dave \
  --client-key=$PWD/dave.key \
  --embed-certs=true
```
Let’s go one step further and check if the current Role associated to Dave allows him to list the nodes of the cluster.
```bash
$ kubectl get nodes
Error from server (Forbidden): nodes is forbidden: User "dave" cannot list resource "nodes" in API group "" at the cluster scope
```
Of course not! But Dave should now be able to deploy stuff on the cluster—well, at least in the namespace named `development`.
```yaml
# www.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: www
  namespace: development
spec:
  replicas: 3
  selector:
    matchLabels:
      app: www
  template:
    metadata:
      labels:
        app: www
    spec:
      containers:
      - name: nginx
        image: nginx:1.14-alpine
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: www
  namespace: development
spec:
  selector:
    app: vote
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 80
```
We can see from the following command that Dave can create those resources in the cluster:
```bash
$ kubectl apply -f www.yaml
deployment.apps/www created
service/www created
```
Dave is limited to the development namespace.We can confirm it from the error message he gets when trying to list all the Pods within the default namespace:
```bash
$ kubectl get pods
Error from server (Forbidden): pods is forbidden: User “dave” cannot list resource “pods” in API group “” in the namespace “default”
```
But if we specify the namespace as `development`:
```bash
$ kubectl get pods -n development
NAME                 READY   STATUS    RESTARTS   AGE
www-756b7fff-75q5n   1/1     Running   0          17s
www-756b7fff-d9qh2   1/1     Running   0          17s
www-756b7fff-zczgk   1/1     Running   0          17s
```
