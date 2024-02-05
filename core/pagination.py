from contextlib import contextmanager
from typing import Any, Generic, Optional, Sequence, TypeVar
from typing_extensions import Self

from fastapi import Query
from fastapi_pagination.bases import AbstractPage, AbstractParams, RawParams
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from db.session import get_db
from db.repository.product_footprints import count_product_footprints


"""
TODO: This module needs some serious attention and basically needs to be reworked in
order to be understandable and testable, it was taken from somewhere else during the
PoC process in order to move forward, and ideally it would have been edited into
something cleaner before graduating to Alpha, but it will take too much time, so
it will be worked on in Alpha and will be redone and tested before Beta release.
The main issue is that testing programmatically leads to RuntimeErrors, and it
is (to me), currently incomprehensible without spending a significant amount of 
time to understand some of the more arcane parts of it.
"""


class JSONAPIParams(BaseModel, AbstractParams):
    offset: int = Query(1, ge=1)
    limit: int = Query(10, ge=1, le=100)

    def to_raw_params(self) -> RawParams:
        return RawParams(limit=self.limit, offset=self.offset)


class JSONAPIPageInfoMeta(BaseModel):
    total: int


class JSONAPIPageMeta(BaseModel):
    page: JSONAPIPageInfoMeta


T = TypeVar("T")


class JSONAPIPage(AbstractPage[T], Generic[T]):
    data: Sequence[T]
    #meta: JSONAPIPageMeta

    __params_type__ = JSONAPIParams

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        params: AbstractParams,
        *,
        total: Optional[int] = None,
        **kwargs: Any,
    ) -> Self:
        assert isinstance(params, JSONAPIParams)
        assert total is not None

        return cls(
            data=items,
            #meta={"page": {"total": total}},
            **kwargs,
        )


class PaginationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        with contextmanager(get_db)() as db:
            product_footprint_count = count_product_footprints(db=db)

        limit = request.query_params.get('limit')
        offset = request.query_params.get('offset', 1)
        if limit:
            # Get current URL, adjust for next page
            http_url = request.url
            url = http_url.replace(scheme='https')
            next_offset = int(offset) + int(limit)
            next_url = url.include_query_params(offset=next_offset)
            print(f'limit: {limit}, offset:{offset}, next_offset:{next_offset}, count:{product_footprint_count}')

            # Construct Link header
            if next_offset < product_footprint_count:
                response.headers['Link'] = f'<{next_url}>; rel="next"'
                print(f"link: {response.headers['Link']}")
        return response