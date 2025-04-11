from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import GraphQLView
from todolist.graphql.schema import schema


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("todolist.urls")),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]
