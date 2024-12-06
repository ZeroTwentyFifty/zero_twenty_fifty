from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/.well-known/openid-configuration")
def openid_configuration():
    config = {
        "issuer": "https://id.example.org",
        "authorization_endpoint": "https://id.example.org/auth/authorize",
        "token_endpoint": "https://id.example.org/auth/token",
        "userinfo_endpoint": "https://id.example.org/auth/userinfo",
        "jwks_uri": "https://id.example.org/.well-known/jwks.json",
        "response_types_supported": ["code", "token", "id_token"],
        "subject_types_supported": ["public"],
        "id_token_signing_alg_values_supported": ["RS256"]
    }
    return JSONResponse(content=config)