from django.db import models


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class NetworkNode(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "network_nodes"
        ordering = ["id"]

    def __str__(self):
        return self.name


class NetworkEdge(BaseModel):
    source_node = models.ForeignKey(
        NetworkNode,
        on_delete=models.CASCADE,
        related_name="outgoing_edges",
    )

    destination_node = models.ForeignKey(
        NetworkNode,
        on_delete=models.CASCADE,
        related_name="incoming_edges",
    )

    latency = models.FloatField()

    class Meta:
        db_table = "network_edges"
        unique_together = ("source_node", "destination_node")

    def __str__(self):
        return f"{self.source_node} -> {self.destination_node}"


class RouteHistory(BaseModel):
    source = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)

    total_latency = models.FloatField()

    path = models.JSONField()

    class Meta:
        db_table = "route_history"
        ordering = ["-created_at"]