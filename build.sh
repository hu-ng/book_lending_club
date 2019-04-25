# <docker build> : tells Docker to build an image
# <-t booklending> sets the tag name of the Docker image to booklending
# <.> where to look for the Dockerfile that is needed for the build at the current directory
docker build -t booklending .

# Reference: https://medium.freecodecamp.org/docker-easy-as-build-run-done-e174cc452599
