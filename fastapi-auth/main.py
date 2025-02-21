"""main.py
Python FastAPI Auth0 integration example
https://auth0.com/blog/build-and-secure-fastapi-server-with-auth0/
"""

from fastapi import FastAPI

# Creates app instance
app = FastAPI()


@app.get("/api/public")
def public():
    """No access token required to access this route"""

    result = {
        "status": "success",
        "msg": ("Hello from a public endpoint! You don't need to be "
                "authenticated to see this.")
    }
    return result
