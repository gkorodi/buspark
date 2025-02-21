# BU Spark! Hackathon

# FastAPI presentation

The website: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)

## Up and Running

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

[https://www.geeksforgeeks.org/flask-vs-fastapi/](https://www.geeksforgeeks.org/flask-vs-fastapi/)

