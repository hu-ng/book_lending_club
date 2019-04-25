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

# Set the environment variables (already matched the ENV with the app/__init__.py)
ENV database_pwd=cs162booklending
ENV database_username=tutorial_user
ENV database_host=minerva-book-lending.chzuzvcwsajf.us-east-2.rds.amazonaws.com:3306
ENV database_db=book_lending_club

# Make port 80 available to the world outside this container
EXPOSE 5000

# Run run.py when the container launches
CMD ["python", "run.py"]
