from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse, name = "home")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="home.jinja", context={}
    )

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(
        request=request, name="about.jinja", context={}
    )

@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
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
        post_content = {
            "status": "ERROR", "message": f"File not found: {file_path}"
        }
    except json.JSONDecodeError:
        post_content = {
            "status": "ERROR", "message": f"Error: Invalid JSON format in: {file_path}"
        }
    except Exception as e:
        post_content = {
            "status": "ERROR", "message": f"An unexpected error occurred: {e}"
        }

    return templates.TemplateResponse(
        request=request, name="post.jinja", context={"post_content": post_content}
    )

@app.get("/posts", response_class=HTMLResponse)
async def get_all_posts(request: Request):
    items = getAllItems()
    return templates.TemplateResponse(
        request=request, name="items.jinja", context={"items": items}
    )

@app.post("/posts", response_class=RedirectResponse)
async def add_new_post(request: Request, id: Annotated[str, Form()], title: Annotated[str, Form()], copy_text: Annotated[str, Form()]):

    file_path = f"post_{id}.json"

    with open(file_path, 'w') as fp:
        json.dump(sample, fp)


    return RedirectResponse(url_for('get_all_posts'), status_code=status.HTTP_303_SEE_OTHER) 