from pydantic import BaseModel


class Token(BaseModel):
    """
    In reality this should be much stricter. the token_type should be
    restricted to a smaller amount of options.
    """
    access_token: str
    token_type: str
