"""main.py
Python FastAPI Auth0 integration example
https://auth0.com/blog/build-and-secure-fastapi-server-with-auth0/
"""

from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBearer
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

# Scheme for the Authorization header
token_auth_scheme = HTTPBearer()

# Creates app instance
app = FastAPI()

security = HTTPBasic()

MY_USERNAME = b"gkorodi"
MY_PASSWORD = b"supersecret"


@app.get("/api/public")
def public():
    """No access token required to access this route"""

    result = {
        "status": "success",
        "msg": ("Hello from a public endpoint! You don't need to be "
                "authenticated to see this.")
    }
    return result


@app.get("/api/private")
def private(token: str = Depends(token_auth_scheme)):
    """A valid access token is required to access this route"""

    if (token.credentials == "bu rocks"):
        result = {
            "status": "success",
            "msg": ("Hello from a private endpoint! You need to be authenticated "
                    "to see this.")
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return result


def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = MY_USERNAME
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = MY_PASSWORD
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/api/profile")
def read_current_user(username: Annotated[str, Depends(get_current_username)]):
    return {"username": username}


# curl -u gkorodi:supersecret http://localhost:8000/api/profile
# curl -u gkorodi:supersecret333 http://localhost:8000/api/profile
# curl http://localhost:8000/api/private --header 'Authorization: Bearer FastAPI is awesome'
# curl http://localhost:8000/api/private --header 'Authorization: Bearer bu rocks'
