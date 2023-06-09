## Setup Kubernetes Cluster

Setting up a Kubernetes cluster with one Ubuntu master and one Ubuntu worker using Kubeadm is a straightforward process. Kubeadm is a tool that automates the installation and configuration of Kubernetes. Here are the steps to follow:

### Prerequisites
Before getting started, you need to have the following:

- Two Ubuntu servers (one for master, one for worker) with at least 2GB of RAM and 2 CPUs.
- Root access on both servers.
- A user with sudo privileges on both servers.


### Step 1: Install Kubeadm
**Run on both node**

To install Kubeadm, run the following command on both servers:
```bash
sudo apt-get update
```
```bash
sudo apt-get install -y apt-transport-https curl
```
```bash
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
```
```bash
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
```
```bash
sudo apt-get update
```
```bash
sudo apt-get install -y kubelet=1.23.9-00 kubeadm=1.23.9-00 kubectl=1.23.9-00
```
```bash
sudo apt-mark hold kubelet kubeadm kubectl
```
```bash
curl https://get.docker.com | bash
```
```bash
sudo swapoff -a
```
**IMPORTANT** : Remove swap partition on `/etc/fstab` also

### Step 2: Initialize the Master Node

```bash
sudo kubeadm init --pod-network-cidr=192.168.0.0/16
```

### Step 3: Configure kubectl
**Run on master node**

```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```
### Step 4: Install a Pod Network
**Run on master node**
```bash
kubectl apply -f https://github.com/weaveworks/weave/releases/download/v2.8.1/weave-daemonset-k8s.yaml
```

### Step 5: Join the Worker Node
**Run on worker node**
On the worker node, run the command that was generated by kubeadm init in Step 2. This command will join the worker node to the cluster.

### Step 6: Verify the Cluster
**Run on master node**
To verify that the cluster is up and running, run the following command on the master node:
```bash
kubectl get nodes
```
This should show both the master and worker nodes as ready.

