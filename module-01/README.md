# Module 1 : Introduction to Containers and Docker
## Setting up Docker on a Linux host
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

## Building And Managing Docker Images
### Part-1 : Building Docker Images 
#### Requirements
- app.py
- Dockerfile

Clone this repo
```
git clone https://github.com/dopevs/labs.git
```

#### Example-01 : Basic Dockerfile

Change directory to example one
```
cd module-01/example-01
```
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
Run Docker Container as background process
```
docker run -d -p 5000:5000 hello-world:v1.0.0
```
Check Docker Container
```
docker ps | grep hello-world
```
Access Application
```
curl http://localhost:5000
```
#### Example-02 : Dockerfile with custom env

Change directory to example two
```
cd module-01/example-02
```
Set Port
```
PORT=8080
```
Build Docker Image
```
docker build -t hello-world:v1.0.1 --build-arg PORT=$PORT .
```
Check Docker Image
```
docker images | grep hello-world
```
Run Docker Container from previously created image
```
docker run -p $PORT:$PORT hello-world:v1.0.1
```
Run Docker Container as background process
```
docker run -d -p $PORT:$PORT hello-world:v1.0.1
```
Check Docker Container
```
docker ps | grep hello-world
```
Access Application
```
curl http://localhost:$PORT
```

### Part-2 : Managin Docker Images
Access docker container
```
docker exec -it <container_name> <command>
```
Stops a running container
```
docker stop <container_name>
```
Starts a stopped container
```
docker start <container_name>
```
Restart a running container
```
docker restart <container_name>
```
Lists all running containers
```
docker ps
```
Lists all containers, including stopped ones
```
docker ps -a
```
Removes a stopped container
```
docker rm <container_name>
```
Forcefully removes a running container
```
docker rm -f <container_name>
```
Displays the logs of a container
```
docker logs <container_name>
```
Displays detailed information about a container
```
docker inspect <container_name>
```
Displays resource usage statistics for all running containers
```
docker stats
```
Renames a container
```
docker rename <old_container_name> <new_container_name>
```
Pauses a running container
```
docker pause <container_name>
```
Unpauses a paused container
```
docker unpause <container_name>
```
Displays the processes running in a container
```
docker top <container_name>
```
