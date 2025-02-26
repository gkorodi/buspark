from typing import Annotated
from fastapi import FastAPI, Request, Form, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import csv
import requests
import os
import json

app = FastAPI()


class Post(BaseModel):
    id: str
    title: str
    text_copy: str | None = None


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse, name="home")
async def home(request: Request):
    """Home Page, where everything starts from."""
    return templates.TemplateResponse(
        request=request, name="home.jinja", context={}
    )


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """Every app should have an About page with some useful information."""
    return templates.TemplateResponse(
        request=request, name="about.jinja", context={}
    )


@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    """The Contact page has some limited information about where to contact the business."""
    return templates.TemplateResponse(
        request=request, name="contact.jinja", context={}
    )


@app.get("/posts/{id}", response_class=HTMLResponse)
async def get_post_by_id(request: Request, id: str):
    file_path = f"post_{id}.json"

    post_content = {}
    try:
        with open(file_path, 'r') as file:
            post_content = json.load(file)
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Post {id} not found",
            headers={"X-Error": "The filename has a parrent of post_{id}.json"},
        )

    except json.JSONDecodeError:
        post_content = {
            "status": "ERROR", "message": f"Error: Invalid JSON format in: {file_path}"
        }
    except Exception as e:
        post_content = {
            "status": "ERROR", "message": f"An unexpected error occurred: {e}"
        }

    return templates.TemplateResponse(
        request=request, name="post.jinja", context={"post": post_content}
    )


def getAllPosts():
    items = []
    for file in os.listdir():
        if file.endswith(".json"):
            with open(file, 'r') as fp:
                items.append(json.load(fp))
    return items


@app.get("/posts", response_class=HTMLResponse)
async def get_all_posts(request: Request):
    posts = getAllPosts()
    return templates.TemplateResponse(
        request=request, name="posts.jinja", context={"posts": posts}
    )


def csv_url_to_dict(url):
    """
    Reads a CSV file from a URL and returns a list of dictionaries.

    Args:
        url (str): The URL of the CSV file.

    Returns:
        list: A list of dictionaries, where each dictionary represents a row in the CSV file.
              Keys of the dictionaries are the header fields of the CSV.
              Returns an empty list if there's an error.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        csv_data = csv.DictReader(response.text.splitlines())
        return list(csv_data)
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return []
    except csv.Error as e:
        print(f"CSV error: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []


@app.get("/events")
async def get_all_events(request: Request):
    csv_url = "https://data.boston.gov/dataset/9076010d-663a-40da-b683-a46ec4d09555/resource/ea7f0605-ffc0-4ad4-a786-02c50b276f54/download/tmpmxxupepy.csv"
    data = csv_url_to_dict(csv_url)

    events = [d for d in data if d['status']
              not in ['Expired', 'Cancelled', 'Inactive']]
    return templates.TemplateResponse(
        request=request, name="events.jinja", context={"events": events}
    )


@app.post("/posts", response_class=RedirectResponse)
async def add_new_post(request: Request, id: Annotated[str, Form()], title: Annotated[str, Form()], copy_text: Annotated[str, Form()]):

    file_path = f"post_{id}.json"

    with open(file_path, 'w') as fp:
        json.dump({
            "id": id,
            "title": title,
            "content": copy_text
        }, fp)

    # https://stackoverflow.com/questions/63682956/fastapi-retrieve-url-from-view-name-route-name
    return RedirectResponse(app.url_path_for('get_all_posts'), status_code=status.HTTP_303_SEE_OTHER)


@app.put("/api/post")
async def create_new_post(post: Post):
    """Create a new Post file from JSON in the request body
    example: curl -X PUT http://localhost:8000/api/post -H "Content-type: application/json" --data '{"id":"103","title":"test","text_copiy":"aaaa"}'
    """
    file_path = f"post_{post.id}.json"

    with open(file_path, 'w') as fp:
        json.dump({
            "id": post.id,
            "title": post.title,
            "content": post.text_copy
        }, fp)
    return post


def delete_file_if_exists(filename):
    """Deletes a file if it exists in the current directory.

    Args:
        filename: The name of the file to delete.
    """
    if os.path.exists(filename):
        try:
            os.remove(filename)
            return f"File '{filename}' deleted successfully."
        except Exception as e:
            return f"Error deleting file '{filename}': {e}"
    else:
        return f"File '{filename}' not found."


@app.delete("/posts/{id}")
async def delete_post(request: Request, id: str) -> str:
    return delete_file_if_exists(f"post_{id}.json")
