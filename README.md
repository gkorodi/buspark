# BU Spark! Hackathon - FastAPI

The website: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)

In plain terms, FastAPI is a python library that enables a Python application to act act as an HTTP (mostly) server for producing dynamic responses to requests. A FastAPI enabled application is used to build APIs with Python and a standard type hint. It is used to specifically create RESTful APIs. It also provides automation for producing documentation for the service you created. It’s currently used by Uber, Microsoft, Explosion AI and others.

Key Features

* **Built-in Security**: Fast API provides built-in security mechanisms through features like **validation** and **sanitization** of user input and dependency injection for various authentication mechanisms.
* **Scalability**: Can handle large volumes of **concurrent** requests and is ideal to be used for real-time applications.
* Automatic Data Validation: **Data validation** ensures that the data (input and output) matches predefined structures and FastAPI provides an automatic data validation mechanism which is much faster than traditional manual validation. Integrated with **Pydantic models**. These models use Python-type annotations which help validate the requests and responses to and from the API.
* High Performance: FastAPI is a modern framework which provides performance at par with NodeJS and Go
* **type hints**
* **asynchronous support**, easy to handle asynchronous operations and I/O-bound tasks.
* Automatically generates detailed and user-friendly **error messages**. By default, FastAPI displays error messages in JSON format.
* In-built automatic documentation support. It helps provide a UI for testing your service. To access these automatically generated documentation, hit the endpoint of the API that has to be tested with /docs.


## Local

```sh
# Create an '/app' directory
mkdir /app
# Change directory into '/app' directory
cd /app
# Update the installed software and add the 'vim' editor, just in case
apt-get update && apt-get -y upgrade && apt-get install -y vim
# Update python library manager (pip) to latest version
pip install --upgrade pip
# Install 'fastapi' library
pip install "fastapi[standard]"
# Create a basic server with two routes
cat << EOF > main.py
from typing import Union
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
EOF

# Start the server, for any client, on port 8001
fastapi dev --host 0.0.0.0 --port 8001 main.py

```

To try the above script, start up a latest `python` image, and copy paste the above lines

`docker run -it --rm --name buspark-app -p 8001:8001 python /bin/bash`

To test your first server, from your own machine open a browser at

[http://localhost:8001/](http://localhost:8001/)

### For DigitalOcean

```sh
# Update the latest mirrors
apt update
# Add the 'vi' editor
apt install -y vim
# Add 'pip' module, to manage libraries
apt install -y python3-pip
# Add the 'venv' module, to manage virtual environments
apt install python3.12-venv
# Create a virtual environment (subdirectory)
python3 -m venv venv
# Switch to the virtual environment in 'venv' subdirectory
source venv/bin/activate
# Add the 'fastapi' library to the virtual environment
pip install "fastapi[standard]"

nohup fastapi dev --host 0.0.0.0 --port 8001 main.py &

```


### Notes

Flask is a synchronous app server enabling library. It is worth knowing and the below comparison can help evaluate the benefits of each implementation.
[https://www.geeksforgeeks.org/flask-vs-fastapi/](https://www.geeksforgeeks.org/flask-vs-fastapi/)


[Swagger.io](https://swagger.io/) is the SmartBear developed de-facto standard for API development. They provide tools and maintain up-to-date standard compliant utilities to speed up API development. 

[REST](https://en.wikipedia.org/wiki/REST) is the basic architectural principle that drives current/common API implementations. The patterns included and the standards based on it are quite useful for all sorts of projects.

[What is RESTful API? by AWS](https://aws.amazon.com/what-is/restful-api/#:~:text=RESTful%20API%20is%20an%20interface,and%20efficient%20software%20communication%20standards.) is AWS's interpretation of the pattern.

[What is a REST API? by RedHat](https://www.redhat.com/en/topics/api/what-is-a-rest-api) is RedHat's interpretation of the same.

[REST API Introduction](https://www.geeksforgeeks.org/rest-api-introduction/) is GeeksForGeeks' explanation of some of the concepts of the pattern.




