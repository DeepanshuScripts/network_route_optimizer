from django.urls import path,include

urlpatterns = [
    path("api/v1/",include("network.api.v1.urls")),
]
