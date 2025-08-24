import arcade
import random
from typing import List, Dict, Any, Tuple


class PencilTool:
    name = "PENCIL"

    def draw_traces(self, traces: List[Dict[str, Any]]):
        for trace in traces:
            if trace["tool"] == self.name:
                arcade.draw_line_strip(trace["trace"], trace["color"], line_width=1)


class MarkerTool:
    name = "MARKER"

    def draw_traces(self, traces: List[Dict[str, Any]]):
        for trace in traces:
            if trace["tool"] == self.name:
                arcade.draw_line_strip(trace["trace"], trace["color"], line_width=8)


class SprayTool:
    name = "SPRAY"

    def make_spray_points(self, x: int, y: int, count: int = 80, radius: int = 24) -> List[Tuple[int, int]]:
        points = []
        import math
        for _ in range(count):
            r = random.random() * radius
            angle = random.random() * 2 * math.pi
            sx = int(x + r * math.cos(angle))
            sy = int(y + r * math.sin(angle))
            points.append((sx, sy))
        return points

    def draw_traces(self, traces: List[Dict[str, Any]]):
        for trace in traces:
            if trace["tool"] == self.name:
                for px, py in trace["trace"]:
                    arcade.draw_circle_filled(px, py, 1.5, trace["color"])


class EraserTool:
    name = "ERASER"

    def draw_traces(self, traces: List[Dict[str, Any]]):
        return
