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

"""Additional Testing Tips:


Edge cases: Consider tests for invalid form data (if the OAuth2ClientCredentialsRequestForm has validation constraints).
Negative scenarios: Write tests to ensure incorrect credentials or invalid scopes are rejected. 
Integration tests: If possible, set up tests that interact with a real token endpoint to validate the end-to-end flow.
"""


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_missing_authorization_header_results_in_403():
    response = client.get("/items")
    assert response.status_code == 403, response.text
    assert response.json() == {"detail": "AccessDenied OAuth2 Client Credentials"}


def test_invalid_bearer_token_returns_403():
    response = client.get("/items", headers={"Authorization": "Non-existent testtoken"})
    assert response.status_code == 403, response.text
    assert response.json() == {"detail": "AccessDenied OAuth2 Client Credentials"}


def test_valid_bearer_token_returns_200():
    response = client.get("/items", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 200, response.text
    assert response.json() == {"token": "testtoken"}


def test_valid_client_credentials_form():
    form = OAuth2ClientCredentialsRequestForm(
        client_id="client_id", client_secret="client_secret", scope="profile"
    )
    assert form.grant_type
    assert form.scopes
    assert form.client_id
    assert form.client_secret
