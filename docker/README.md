# Docker
## Install Docker
There are two ways to install docker on mac os. One way is to go to docker website to download [Docker Desktop for Mac](https://docs.docker.com/docker-for-mac/install/). The other way is to install docker using Homebrew. The [article](https://medium.com/@yutafujii_59175/a-complete-one-by-one-guide-to-install-docker-on-your-mac-os-using-homebrew-e818eb4cfc3) written by Yuta Fujii includes step by step guide on docker installation using Homebrew. The only issue I had when I was installing docker using Homebrew is that I need to unblock the software, such as virtual box, by clicking `Open Anyway` on the `General` tab of `Security & Privacy` setting. That is because the new Mac OS has a more strict security rule on installing new software on it.

## Create Docker Image
In order to create a Docker Image, we need to first create a `Dockerfile`. **Dockerfile** serves as a recipe that tells Docker the required ingredients and the instructions to build the image. A **Dockerfile** usually start with a `FROM` statement, retrieving some public available image from docker hub. That image is the base of the image we are creating, and it depends on the applications we are going to include in it. If the application/code is mostly written in python, then we can use the image `python:3.X-alpine`. Then we add on other required software. For python application which uses pandas, we need add `gcc g++ python3-dev`. Then we can start to copy files and running command. A python application also need to include requirements file `requirements.txt` that is supposed to include all the python libraries needed to run the python application. Here is an example of **DockerFile**. Once the **DockerFile** is ready, we can use the command below to build the image.
```
docker build -t <image name> .
```
If this is not our first time to create this image and we want to re-create the image from the scratch, we need to add option `--no-cache`. The command would look like this:
```
docker build --no-cache -t <image name> .
```
The most common failure I encountered when creating images is that software dependencies required by python libraries. Python libraries pandas, numpy, and matplotlib requires different add software. It might take several rounds to get all the software installed. Building these libraries from DockerFile may take 15-20 minutes.

## Housekeeping Docker Images
We can check all the available docker images using the command below.
```
docker images
```
If a image is successfully created, it will be shown in the list of result. Otherwise, a dangling image with no name will be created. I like to using the command below to clean up the dangling images and containers.
```
docker system prune
```

## Create Container based on Image
```
docker run -i -t <image name>:<version tag> --name <container name>
```
The command above can create a container based on a image.
