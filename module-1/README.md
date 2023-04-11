## Module 1 : Introduction to Containers and Docker
### Setting up Docker on a Linux host
> Linux

#### Set up the repository
```
sudo apt-get update
```
```
sudo apt-get install ca-certificates curl gnupg
```
```
sudo mkdir -m 0755 -p /etc/apt/keyrings
```
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```
```
echo "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | sudo tee /etc/apt/sources.list.d/docker.list /dev/null
```
#### Install Docker Engine
```
sudo apt-get update
```
```
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
```
sudo docker ps
```
#### Manage Docker as a non-root user
```
sudo groupadd docker
```
```
sudo usermod -aG docker $USER
```
```
newgrp docker
```
```
docker ps
```
#### Configure Docker to start on boot with systemd
```
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
```
#### To stop this behavior, use disable instead
```
sudo systemctl disable docker.service
sudo systemctl disable containerd.service
```
> Mac 

[Download docker desktop for mac here](https://docs.docker.com/desktop/install/mac-install/)

> Windows

[Download docker desktop for windows here](https://docs.docker.com/desktop/install/windows-install/)

### Building and managing Docker images

#### Requirements
- app.py
- Dockerfile

Build Docker Image
```
docker build -t hello-world:v1.0.0 .
```
Check Docker Image
```
docker images | grep hello-world
```
Run Docker Container from previously created image
```
docker run -p 5000:5000 hello-world:v1.0.0
```
Check Docker Container
```
docker ps -a
```
Access Application
```
curl http://localhost:5000
```
