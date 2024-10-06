# Docker image python-watchdog
https://hub.docker.com/r/evit15/python-watchdog

# How to use
This will guide users on how to build and run the Docker image using the provided .
## Build the Docker image
```sh
docker build -t python-watchdog .
```

## Run the docker image
```sh
docker run --rm -v $HOME/test:/apps/ evit15/python-watchdog:latest /apps "echo 'Folder has changed'" --delay 5
```