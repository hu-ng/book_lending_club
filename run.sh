# <docker run> : run a container from an image. 
# <-d -it> : the command for daemon (running tasks in the background) + interactive terminal (interacting with the container). 
# <-p 80:8080> maps port 80 of our machine to port 8080 of the container. (as previously in DockerFile)
# <--name=cs162> gives our container the name cs162. 
# <booklending npm run ec2> starting the ec2 app named booklending
# < --host=0.0.0.0> : local host
# On Python we can run: docker run -d -it --name=cs162 booklending python run.py.

docker run -d -it -p 80:8080 --name=cs162 booklending npm run ec2 -- --host=0.0.0.0
