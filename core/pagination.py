from contextlib import contextmanager
from typing import Any, Generic, Optional, Sequence, TypeVar
from typing_extensions import Self

from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.limit_offset import OptionalLimitOffsetParams
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


T = TypeVar("T")


class JSONAPIPage(AbstractPage[T], Generic[T]):
    """
    Represents a single page of results in a JSON:API compliant response.

    Attributes:
        data (Sequence[T]): The list of data items for the current page.
        __params_type__ (JSONAPIParams): Specifies the expected pagination parameter type.

    Methods:
        create(cls, items, params, *, total, **kwargs): Creates a JSONAPIPage object.
            Requires total record count for proper pagination metadata generation.

    Testing Notes:
        * Create unit tests for this class as well. Focus on:
            * Correct creation of JSONAPIPage objects with varying data, parameters, and total counts.
            * If/when 'meta' attributes are implemented, ensure they are serialized as expected.
    """
    data: Sequence[T]
    meta: dict[str, int] = {}

    __params_type__ = OptionalLimitOffsetParams

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        params: OptionalLimitOffsetParams = None,
        *,
        total: Optional[int] = None,
        **kwargs: Any,
    ) -> Self:
        assert isinstance(params, OptionalLimitOffsetParams)
        assert total is not None

        return cls(
            data=items,
            meta={"total": total},
            **kwargs,
        )


class PaginationMiddleware(BaseHTTPMiddleware):
    """
    Starlette middleware to intercept API responses and add pagination-related headers.

    Responsibilities:
        1. Counts total product footprints in the database.
        2. Calculates the URL for the 'next' page of results (if applicable).
        3. Adds a 'Link' header to the response, guiding clients on how to fetch the next data set.

    Testing Notes:
        * Consider extracting link-generation logic into a separate, testable helper function.
        * Use mocking to replace 'count_product_footprints' in endpoint tests. This lets you focus on
          pagination behavior without requiring a live database.
        * Write a few integration tests focused on the middleware, where realistic requests
          trigger Link header creation.
    """
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        with contextmanager(get_db)() as db:
            product_footprint_count = count_product_footprints(db=db)

        limit = request.query_params.get('limit')
        print(f"we have a limit here: {limit}")
        offset = request.query_params.get('offset')
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
