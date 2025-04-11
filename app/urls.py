from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import GraphQLView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from todolist.graphql.schema import schema


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("todolist.urls")),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]
