from typing import Annotated

from pydantic import Field


NonEmptyString = Annotated[str, Field(min_length=1)]
