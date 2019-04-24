###
FROM python:3-alpine
COPY requirements.txt .

# Set the working directory to /cs162-book-lending
WORKDIR /cs162-book-lending

# Copy the current directory contents into the container at /cs162-book-lending
ADD . /cs162-book-lending
RUN apk add --no-cache curl python3 pkgconfig python3-dev openssl-dev libffi-dev musl-dev make gcc
RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENV database_pwd=cs162booklending
ENV database_username=tutorial_user
ENV database_host=minerva-book-lending.chzuzvcwsajf.us-east-2.rds.amazonaws.com:3306
ENV database_db=book_lending_club

# Make port 80 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "run.py"]
