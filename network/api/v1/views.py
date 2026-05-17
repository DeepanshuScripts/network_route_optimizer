from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView

from network.models import (
    NetworkNode,
    RouteHistory,
    NetworkEdge,
)

from network.api.v1.serializers import (
    NetworkNodeSerializer,
    NetworkEdgeSerializer,
    RouteHistorySerializer,
    ShortestRouteRequestSerializer,
    ShortestRouteResponseSerializer,
)

from network.api.v1.services import (
    ShortestPathService,
)

from utils.responses import (
    success_response,
    error_response,
)

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
    OpenApiTypes,
)

@extend_schema(
    tags=["Nodes"],
    summary="Create and list network nodes",
    description=(
        "API for creating and listing "
        "network nodes."
    ),
)
class NetworkNodeListCreateAPIView(generics.ListCreateAPIView):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data )

        if not serializer.is_valid():
            return error_response(
                message="Validation failed.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        self.perform_create(serializer)

        return success_response(
            message="Node created successfully.",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED,
        )

    def list(self, request):
        queryset = self.get_queryset()

        serializer = self.get_serializer(queryset,many=True)

        return success_response(
            message="Nodes fetched successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


@extend_schema(
    tags=["Edges"],
    summary="Create and list network edges",
    description=(
        "API for managing network edges."
    ),
)
class NetworkEdgeListCreateAPIView(generics.ListCreateAPIView):
    queryset = (
        NetworkEdge.objects
        .select_related(
            "source_node",
            "destination_node",
        )
        .all()
    )

    serializer_class = NetworkEdgeSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return error_response(
                message="Validation failed.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        self.perform_create(serializer)

        return success_response(
            message="Edge created successfully.",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED,
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = self.get_serializer(
            queryset,
            many=True,
        )

        return success_response(
            message="Edges fetched successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


@extend_schema(
    tags=["Routes"],
    summary="Find the shortest route between two nodes",
    description=(
        "API for finding the shortest route "
        "between two network nodes."
    ),
    request=ShortestRouteRequestSerializer,
    responses={
        200: ShortestRouteResponseSerializer,
        400: OpenApiResponse(
            description=(
                "Validation error or "
                "invalid node."
            )
        ),
        404: OpenApiResponse(
            description="No path exists."
        ),
    },
)
class ShortestRouteAPIView(APIView):
    def post(self, request):

        source = request.data.get("source")
        destination = request.data.get("destination")

        if not source or not destination:
            return error_response(
                message=(
                    "Source and destination "
                    "are required."
                ),
                status_code=(
                    status.HTTP_400_BAD_REQUEST
                ),
            )

        if not NetworkNode.objects.filter(name=source).exists():
            return error_response(
                message="Source node not found.",
                status_code=(
                    status.HTTP_400_BAD_REQUEST
                ),
            )

        if not NetworkNode.objects.filter(name=destination).exists():
            return error_response(
                message=(
                    "Destination node not found."
                ),
                status_code=(
                    status.HTTP_400_BAD_REQUEST
                ),
            )

        result = (
            ShortestPathService.find_shortest_path(
                source=source,
                destination=destination,
            )
        )

        if not result:

            return error_response(
                message=(
                    f"No path exists between "
                    f"{source} and {destination}"
                ),
                status_code=(
                    status.HTTP_404_NOT_FOUND
                ),
            )

        RouteHistory.objects.create(
            source=source,
            destination=destination,
            total_latency=result[
                "total_latency"
            ],
            path=result["path"],
        )

        return success_response(
            message=(
                "Shortest route fetched "
                "successfully."
            ),
            data=result,
            status_code=status.HTTP_200_OK,
        )    

@extend_schema(
    tags=["Routes"],

    summary="Route history",

    description=(
        "Returns previous route searches."
    ),

    parameters=[
        OpenApiParameter(
            name="source",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Filter by source node.",
        ),

        OpenApiParameter(
            name="destination",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description=(
                "Filter by destination node."
            ),
        ),

        OpenApiParameter(
            name="limit",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Limit number of records.",
        ),

        OpenApiParameter(
            name="date_from",
            type=OpenApiTypes.DATE,
            location=OpenApiParameter.QUERY,
            required=False,
            description=(
                "Filter records from date."
            ),
        ),

        OpenApiParameter(
            name="date_to",
            type=OpenApiTypes.DATE,
            location=OpenApiParameter.QUERY,
            required=False,
            description=(
                "Filter records until date."
            ),
        ),
    ],
)
class RouteHistoryAPIView( generics.ListAPIView):
    serializer_class = RouteHistorySerializer

    def get_queryset(self):
        queryset = RouteHistory.objects.all()

        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")
        limit = self.request.query_params.get("limit")
        date_from = self.request.query_params.get("date_from" )
        date_to = self.request.query_params.get( "date_to")

        if source:
            queryset = queryset.filter(source=source)

        if destination:
            queryset = queryset.filter(
                destination=destination
            )

        if date_from:
            queryset = queryset.filter(
                created_at__date__gte=date_from
            )

        if date_to:
            queryset = queryset.filter(
                created_at__date__lte=date_to
            )

        if limit:
            queryset = queryset[:int(limit)]

        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer( queryset, many=True,)

        return success_response(
            message=(
                "Route history fetched successfully."
            ),
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


@extend_schema(
    tags=["Nodes"],
    summary="Delete and retrieve network nodes",
    description=(
        "API for creating and listing "
        "network nodes."
    ),
)
class NetworkNodeRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return success_response(
            message="Node deleted successfully.",
            data={},
            status_code=status.HTTP_200_OK,
        )

@extend_schema(
    tags=["Edges"],
    summary="Delete and retrieve network edges",
    description=(
        "API for managing network edges."
    ),
) 
class NetworkEdgeRetrieveDestroyAPIView( generics.RetrieveDestroyAPIView):
    queryset = (
        NetworkEdge.objects
        .select_related(
            "source_node",
            "destination_node",
        )
    )
    serializer_class = NetworkEdgeSerializer

    def destroy(self, requests, *args, **kwargs):

        instance = self.get_object()

        self.perform_destroy(instance)

        return success_response(
            message="Edge deleted successfully.",
            data={},
            status_code=status.HTTP_200_OK,
        )