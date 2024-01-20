from enum import Enum
from typing import Dict, Optional, Annotated

from fastapi.exceptions import HTTPException
from fastapi.param_functions import Form
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.security.oauth2 import OAuth2, OAuthFlowsModel
from starlette.requests import Request


class SchemeName(str, Enum):
    OAUTH2_CLIENT_CREDENTIALS = "OAuth2ClientCredentials"


class OAuth2ClientCredentialsRequestForm:
    """
    This is a dependency class, use it like:
        token_scheme = HTTPBasicClientCredentials(
            auto_error=False, scheme_name="oAuth2ClientCredentials"
        )
        @router.post("/token")
        def create_access_token(
            form: OAuth2ClientCredentialsRequestForm = Depends(),
            basic_credentials: Optional[HTTPClientCredentials] = Depends(token_scheme),
        ):
            if form.client_id and form.client_secret:
                client_id = form.client_id
                client_secret = form.client_secret
            elif basic_credentials:
                client_id = basic_credentials.client_id
                client_secret = basic_credentials.client_secret
            else:
                HTTPException(status_code=400, detail="Client credentials not provided")
            pass
    This will allow the client to send its credentials either via headers or body with the request for a token.
    grant_type: the OAuth2 spec says it is required and MUST be the fixed string "client_credentials".
    scope: Optional string. Several scopes (each one a string) separated by spaces. E.g.
        "items:read items:write users:read profile openid"
    client_id: optional string. OAuth2 recommends sending the client_id and client_secret
        using HTTP Basic auth, as: client_id:client_secret
    client_secret: optional string. OAuth2 recommends sending the client_id and client_secret
        using HTTP Basic auth, as: client_id:client_secret
    """

    def __init__(
        self,
        grant_type: str = Form("client_credentials", pattern="client_credentials"),
        scope: str = Form(""),
        client_id: Optional[str] = Form(None),
        client_secret: Optional[str] = Form(None),
    ):
        self.grant_type = grant_type
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret


class OAuth2ClientCredentials(OAuth2):
    """
    Implement OAuth2 client_credentials workflow.

    This is modeled after the OAuth2PasswordBearer and OAuth2AuthorizationCodeBearer
    classes from FastAPI, but sets auto_error to True to avoid uncovered branches.
    See https://github.com/tiangolo/fastapi/issues/774 for original implementation,
    and to check if FastAPI added a similar class.

    See RFC 6749 for details of the client credentials authorization grant.
    """

    def __init__(
        self,
        tokenUrl: str,
        scopes: Optional[Dict[str, str]] = None,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            clientCredentials={"tokenUrl": tokenUrl, "scopes": scopes}
        )
        super().__init__(
            flows=flows,
            scheme_name=SchemeName.OAUTH2_CLIENT_CREDENTIALS,
            auto_error=True)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")

        # TODO: Try combining these lines after FastAPI 0.61.2 / mypy update
        scheme_param = get_authorization_scheme_param(authorization)
        scheme: str = scheme_param[0]
        param: str = scheme_param[1]

        if not authorization or scheme.lower() != "bearer":
            raise HTTPException(
                status_code=403,
                detail="AccessDenied OAuth2 Client Credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return param
