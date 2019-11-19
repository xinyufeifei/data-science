# Supergirl

By running the command below we can build a image called **supergilr** based on the DockerFile on the current directory.
```
docker build -t supergirl .
```
The image will provide an environment to execute the Jupyter notebook included in notebook directory. Here is the command to run the image as a container.
```
docker run --rm supergirl
```
Adding `--`rm option, the container created based on the image `supergirl` will be automatically removed. After we run the code above, the Jupyter notebook will be executed as it is stated in the DockerFile. And a visualization chart will be generated and saved as a html file. However this html file is not visible to the host, such as your local laptop because it sits in the container. In order to save the file in the host, we need add `--volume` option. This option maps our host directory to the container directory.<br>
```
docker run --rm --volume "$PWD:/supergirl" supergirl
```
`$PWD` means that I map the directory where I saved the DockerFile to root directory on the container. If you need to choose different directory on the host, you need to create an exact same file directory on the host as the container. Otherwise, the run command won't succeed.

