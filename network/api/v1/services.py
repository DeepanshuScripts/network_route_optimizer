import heapq
from collections import defaultdict
from network.models import NetworkEdge


class ShortestPathService:

    @staticmethod
    def build_graph():
        graph = defaultdict(list)

        edges = NetworkEdge.objects.select_related(
            "source_node",
            "destination_node",
        )

        for edge in edges:
            graph[edge.source_node.name].append(
                (
                    edge.destination_node.name,
                    edge.latency,
                )
            )

        return graph

    @staticmethod
    def find_shortest_path(source, destination):
        graph = ShortestPathService.build_graph()

        priority_queue = [(0, source, [])]

        visited = set()

        while priority_queue:
            total_latency, current_node, path = heapq.heappop(priority_queue)

            if current_node in visited:
                continue

            visited.add(current_node)

            path = path + [current_node]

            if current_node == destination:
                return {
                    "total_latency": total_latency,
                    "path": path,
                }

            for neighbor, latency in graph[current_node]:
                if neighbor not in visited:
                    heapq.heappush(
                        priority_queue,
                        (
                            total_latency + latency,
                            neighbor,
                            path,
                        ),
                    )

        return None