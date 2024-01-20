from typing import Optional

from fastapi import FastAPI, Security
from fastapi.testclient import TestClient

from core.oauth2_client_credentials import OAuth2ClientCredentials, OAuth2ClientCredentialsRequestForm


app = FastAPI()

oauth2_scheme = OAuth2ClientCredentials(tokenUrl="token")


@app.get("/items/")
async def read_items(token: Optional[str] = Security(oauth2_scheme)):
    if token:
        return {"token": token}


client = TestClient(app)

openapi_schema = {
    "openapi": "3.1.0",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/items/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
                "summary": "Read Items",
                "operationId": "read_items_items__get",
                "security": [{"OAuth2ClientCredentials": []}],
            }
        }
    },
    "components": {
        "securitySchemes": {
            "OAuth2ClientCredentials": {
                "type": "oauth2",
                "flows": {
                    "clientCredentials": {
                        "tokenUrl": "token",
                        "scopes": {},
                    }
                },
            }
        }
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_no_token():
    response = client.get("/items")
    assert response.status_code == 403, response.text
    assert response.json() == {"detail": "AccessDenied OAuth2 Client Credentials"}


def test_incorrect_token():
    response = client.get("/items", headers={"Authorization": "Non-existent testtoken"})
    assert response.status_code == 403, response.text
    assert response.json() == {"detail": "AccessDenied OAuth2 Client Credentials"}


def test_token():
    response = client.get("/items", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 200, response.text
    assert response.json() == {"token": "testtoken"}


def test_client_credentials_form():
    form = OAuth2ClientCredentialsRequestForm(
        client_id="client_id", client_secret="client_secret", scope="profile"
    )
    assert form.grant_type
    assert form.scopes
    assert form.client_id
    assert form.client_secret
