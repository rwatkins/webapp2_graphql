from __future__ import annotations

import typing
from typing import TYPE_CHECKING, Any, Mapping, Optional, Union

import strawberry
from strawberry.http.sync_base_view import (
    SyncBaseHTTPView,
    SyncHTTPRequestAdapter,
)
from strawberry.http.types import HTTPMethod
from strawberry.http.typevars import Context, RootValue
from strawberry.utils.graphiql import get_graphiql_html
from webapp2 import (
    RequestHandler,
    WSGIApplication,
    Request,
    Response,
    RedirectHandler,
    Route,
)

from schema import schema

if TYPE_CHECKING:
    from strawberry.http import GraphQLHTTPResponse
    from strawberry.schema.base import BaseSchema


class Webapp2HTTPRequestAdapter(SyncHTTPRequestAdapter):
    def __init__(self, request: Request):
        self.request = request

    @property
    def query_params(self):
        return dict(self.request.params)

    @property
    def body(self) -> Union[str, bytes]:
        return self.request.body

    @property
    def method(self) -> HTTPMethod:
        return self.request.method.upper()

    @property
    def headers(self) -> Mapping[str, str]:
        return self.request.headers

    @property
    def content_type(self) -> Optional[str]:
        return self.request.headers.get("Content-Type")

    @property
    def post_data(self) -> Mapping[str, Union[str, bytes]]:
        return dict(self.request.POST)

    @property
    def files(self) -> Mapping[str, Any]:
        raise NotImplementedError()


class BaseGraphQLView:
    def __init__(
        self,
        schema: BaseSchema,
        graphiql: bool = True,
        allow_queries_via_get: bool = True,
    ):
        self.schema = schema
        self.graphiql = graphiql
        self.allow_queries_via_get = allow_queries_via_get

    def render_graphiql(self, request: Request) -> Response:
        template = get_graphiql_html(False)
        self.response.write(template)

    def create_response(
        self, response_data: GraphQLHTTPResponse, sub_response: Response
    ) -> Response:
        sub_response.write(self.encode_json(response_data))  # type: ignore
        return sub_response


class GraphQLView(
    BaseGraphQLView,
    SyncBaseHTTPView[Request, Response, Response, Context, RootValue],
    RequestHandler,
):
    allow_queries_via_get: bool = True
    request_adapter_class = Webapp2HTTPRequestAdapter

    def __init__(self, request, response):
        RequestHandler.__init__(self, request, response)
        BaseGraphQLView.__init__(
            self, schema=schema, graphiql=True, allow_queries_via_get=True
        )

    def get(self, *args, **kwargs):
        self.run(request=self.request)

    def post(self, *args, **kwargs):
        self.run(request=self.request)

    def get_context(self, request: Request, response: Response) -> Context:
        """
        Required by SyncBaseHTTPView
        """
        return {"request": request, "response": response}  # type: ignore

    def get_root_value(self, request: Request) -> Optional[RootValue]:
        """
        Required by SyncBaseHTTPView
        """
        return None

    def get_sub_response(self, request: Request) -> Response:
        """
        Required by SyncBaseHTTPView
        """
        return self.response


app = WSGIApplication(
    [
        Route("/", RedirectHandler, defaults={"_uri": "/graphql"}),
        Route("/graphql<:/?>", GraphQLView),
    ],
    debug=True,
)
