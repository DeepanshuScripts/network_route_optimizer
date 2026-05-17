from django.urls import path

from network.api.v1.views import (
    ShortestRouteAPIView,
    NetworkNodeListCreateAPIView,
    NetworkEdgeListCreateAPIView,
    RouteHistoryAPIView,
    NetworkNodeRetrieveDestroyAPIView,
    NetworkEdgeRetrieveDestroyAPIView,
)

urlpatterns = [
    path("nodes",NetworkNodeListCreateAPIView.as_view(),name="nodes"),
    path("edges",NetworkEdgeListCreateAPIView.as_view(),name="edges"),
    path("routes/shortest", ShortestRouteAPIView.as_view(),name="shortest-route"),
    path("routes/history",RouteHistoryAPIView.as_view(), name="route-history"),
    ##
    path( "nodes/<int:pk>",NetworkNodeRetrieveDestroyAPIView.as_view(),name="node-delete"),
    path("edges/<int:pk>",NetworkEdgeRetrieveDestroyAPIView.as_view(), name="edge-delete"),
]