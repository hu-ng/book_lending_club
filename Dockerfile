###
FROM python:3-alpine
COPY requirements.txt .

# Set the working directory to /cs162-book-lending
WORKDIR /cs162-book-lending

# Copy the current directory contents into the container at /cs162-book-lending
ADD . /cs162-book-lending

# This line is to fix the cffi package dependecy. 
RUN apk add --no-cache curl python3 pkgconfig python3-dev openssl-dev libffi-dev musl-dev make gcc

# Install the required packages to run the Python files 
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Set the environment variables
ARG environment
# This is for cases the ARG isn't passed: the default will run the production (from production.env)
ENV environment=${environment:-production} 
# When we want to add testing environment, just create a test.env and modify this DockerFile accordingly!


# Make port 80 available to the world outside this container
EXPOSE 5000

# Run run.py when the container launches
CMD ["python", "run.py"]
