from rest_framework import serializers

from network.models import (
    NetworkNode,
    NetworkEdge,
    RouteHistory,
)


class NetworkNodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = NetworkNode
        fields = [
            "id",
            "name",
        ]

    def validate_name(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Node name cannot be empty."
            )

        if NetworkNode.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                "Node with this name already exists."
            )

        return value


class NetworkEdgeSerializer(serializers.ModelSerializer):
    source = serializers.CharField(write_only=True)
    destination = serializers.CharField(write_only=True)

    class Meta:
        model = NetworkEdge

        fields = [
            "id",
            "source",
            "destination",
            "latency",
        ]

    def validate(self, attrs):
        source_name = (
            attrs.get("source", "")
            .strip()
        )

        destination_name = (
            attrs.get("destination", "")
            .strip()
        )

        latency = attrs.get("latency")

        if latency <= 0:
            raise serializers.ValidationError(
                {
                    "latency": (
                        "Latency must be greater than zero."
                    )
                }
            )

        if source_name == destination_name:
            raise serializers.ValidationError(
                {
                    "destination": (
                        "Source and destination "
                        "cannot be same."
                    )
                }
            )

        try:
            source_node = (
                NetworkNode.objects.get(
                    name=source_name
                )
            )

        except NetworkNode.DoesNotExist:

            raise serializers.ValidationError(
                {
                    "source": (
                        "Source node not found."
                    )
                }
            )

        try:
            destination_node = (
                NetworkNode.objects.get(
                    name=destination_name
                )
            )

        except NetworkNode.DoesNotExist:

            raise serializers.ValidationError(
                {
                    "destination": (
                        "Destination node "
                        "not found."
                    )
                }
            )

        if NetworkEdge.objects.filter(
            source_node=source_node,
            destination_node=destination_node,
        ).exists():

            raise serializers.ValidationError(
                {
                    "edge": (
                        "Edge already exists."
                    )
                }
            )

        attrs["source_node"] = source_node
        attrs["destination_node"] = destination_node

        return attrs

    def create(self, validated_data):

        validated_data.pop("source")
        validated_data.pop("destination")

        return NetworkEdge.objects.create(
            **validated_data
        )

    def to_representation(self, instance):

        return {
            "id": instance.id,
            "source":instance.source_node.name,
            "destination": instance.destination_node.name,
            "latency": instance.latency,
        }


class RouteHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = RouteHistory

        fields = [
            "id",
            "source",
            "destination",
            "total_latency",
            "path",
            "created_at",
        ]

class ShortestRouteRequestSerializer( serializers.Serializer):
    source = serializers.CharField()
    destination = serializers.CharField()


class ShortestRouteResponseSerializer(serializers.Serializer):
    total_latency = serializers.FloatField()
    path = serializers.ListField(child=serializers.CharField())