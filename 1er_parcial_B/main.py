import arcade
import sys
import json
import os
import tkinter as tk
from tkinter import filedialog
from tool import PencilTool, MarkerTool, SprayTool, EraserTool

WIDTH = 960
HEIGHT = 640
TITLE = "Paint"
SIDEBAR_WIDTH = 180
BUTTON_HEIGHT = 48
PADDING = 12
TOOLS = ["PENCIL", "MARKER", "SPRAY", "ERASER"]
COLOR_SWATCHES = [
    arcade.color.BLACK,
    arcade.color.RED,
    arcade.color.BLUE,
    arcade.color.GREEN,
    arcade.color.YELLOW,
    arcade.color.ORANGE,
    arcade.color.PURPLE,
    arcade.color.BROWN,
    arcade.color.CYAN,
    arcade.color.MAGENTA,
]

COLOR_SHORTCUTS = {
    arcade.key.A: COLOR_SWATCHES[0],
    arcade.key.S: COLOR_SWATCHES[1],
    arcade.key.D: COLOR_SWATCHES[2],
    arcade.key.F: COLOR_SWATCHES[3],
    arcade.key.G: COLOR_SWATCHES[4],
    arcade.key.H: COLOR_SWATCHES[5],
    arcade.key.J: COLOR_SWATCHES[6],
    arcade.key.K: COLOR_SWATCHES[7],
    arcade.key.Q: COLOR_SWATCHES[8],
    arcade.key.W: COLOR_SWATCHES[9],
}

def _rect_points(x, y, w, h):
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]

class Paint(arcade.View):
    def __init__(self, load_path: str = None):
        super().__init__()
        self.background_color = arcade.color.WHITE
        self.tool = PencilTool()
        self.used_tools = {self.tool.name: self.tool}
        self.color = arcade.color.BLACK
        self.traces = []
        if load_path is not None and os.path.exists(load_path):
            try:
                with open(load_path, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                self.traces = [
                    {
                        "tool": t["tool"],
                        "color": tuple(t["color"]) if isinstance(t.get("color"), list) else t.get("color"),
                        "trace": [tuple(p) for p in t.get("trace", [])]
                    } for t in raw
                ]
            except Exception:
                self.traces = []
        self.sidebar_x = WIDTH - SIDEBAR_WIDTH
        self.buttons = []
        self._create_buttons()
        self.mouse_x = None
        self.mouse_y = None

    def _create_buttons(self):
        x = self.sidebar_x + PADDING
        y = HEIGHT - PADDING - BUTTON_HEIGHT - 40
        for name in TOOLS:
            rect = (x, y, SIDEBAR_WIDTH - 2 * PADDING, BUTTON_HEIGHT)
            self.buttons.append(("tool", name, rect))
            y -= BUTTON_HEIGHT + PADDING
        y -= PADDING
        for idx, color in enumerate(COLOR_SWATCHES):
            cx = x + (idx % 2) * ((SIDEBAR_WIDTH - 2 * PADDING) / 2)
            cy = y - (idx // 2) * (BUTTON_HEIGHT + PADDING)
            rect = (cx, cy, (SIDEBAR_WIDTH - 2 * PADDING) / 2 - PADDING, BUTTON_HEIGHT)
            self.buttons.append(("color", color, rect))

    def on_draw(self):
        self.clear()
        for tool in self.used_tools.values():
            tool.draw_traces(self.traces)
        left = self.sidebar_x
        right = WIDTH
        top = HEIGHT
        bottom = 0
        sidebar = [(left, bottom), (right, bottom), (right, top), (left, top)]
        arcade.draw_polygon_filled(sidebar, arcade.color.LIGHT_GRAY)
        arcade.draw_text("Herramientas", self.sidebar_x + PADDING, HEIGHT - PADDING - 16, arcade.color.BLACK, 14)
        for kind, val, rect in self.buttons:
            x, y, w, h = rect
            pts = _rect_points(x, y, w, h)
            arcade.draw_polygon_outline(pts, arcade.color.BLACK, 2)
            if kind == "tool":
                label = val
                if val == self.tool.name:
                    arcade.draw_polygon_filled(pts, arcade.color.LIGHT_BLUE)
                arcade.draw_text(label, x + 8, y + h / 2 - 8, arcade.color.BLACK, 12)
            else:
                inner = _rect_points(x + 2, y + 2, w - 4, h - 4)
                arcade.draw_polygon_filled(inner, val)
                if val == self.color:
                    arcade.draw_polygon_outline(pts, arcade.color.BLACK, 3)
        if self.tool.name == "ERASER" and self.mouse_x is not None and self.mouse_y is not None:
            try:
                arcade.draw_circle_outline(self.mouse_x, self.mouse_y, 20, arcade.color.BLACK, 2)
            except Exception:
                pass
        arcade.draw_text("Presiona O para guardar", self.sidebar_x + PADDING, 32, arcade.color.DARK_SLATE_GRAY, 12)
        arcade.draw_text("Presiona L para cargar", self.sidebar_x + PADDING, 8, arcade.color.DARK_SLATE_GRAY, 12)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        self.mouse_x = x
        self.mouse_y = y
        if x >= self.sidebar_x:
            for kind, val, rect in self.buttons:
                rx, ry, rw, rh = rect
                if rx <= x <= rx + rw and ry <= y <= ry + rh:
                    if kind == "tool":
                        if val == "PENCIL":
                            self.tool = PencilTool()
                        elif val == "MARKER":
                            self.tool = MarkerTool()
                        elif val == "SPRAY":
                            self.tool = SprayTool()
                        elif val == "ERASER":
                            self.tool = EraserTool()
                        self.used_tools[self.tool.name] = self.tool
                    else:
                        self.color = val
                    return
            return
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.tool.name == "SPRAY":
                spray_points = self.tool.make_spray_points(x, y)
                self.traces.append({"tool": self.tool.name, "color": self.color, "trace": spray_points})
                self.used_tools[self.tool.name] = self.tool
            elif self.tool.name == "ERASER":
                self.erase_at(x, y, radius=20)
            else:
                self.traces.append({"tool": self.tool.name, "color": self.color, "trace": [(x, y)]})
                self.used_tools[self.tool.name] = self.tool

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        self.mouse_x = x
        self.mouse_y = y
        if x >= self.sidebar_x:
            return
        if not self.traces:
            if self.tool.name == "ERASER":
                self.erase_at(x, y, radius=20)
            return
        if self.tool.name == "ERASER":
            self.erase_at(x, y, radius=20)
            return
        last = self.traces[-1]
        if self.tool.name == "SPRAY":
            spray_points = self.tool.make_spray_points(x, y)
            if last["tool"] == "SPRAY":
                last["trace"].extend(spray_points)
            else:
                self.traces.append({"tool": "SPRAY", "color": self.color, "trace": spray_points})
        elif last["tool"] != self.tool.name:
            self.traces.append({"tool": self.tool.name, "color": self.color, "trace": [(x, y)]})
        else:
            last["trace"].append((x, y))

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        self.mouse_x = x
        self.mouse_y = y

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.KEY_1:
            self.tool = PencilTool()
        elif symbol == arcade.key.KEY_2:
            self.tool = MarkerTool()
        elif symbol == arcade.key.KEY_3:
            self.tool = SprayTool()
        elif symbol == arcade.key.KEY_4:
            self.tool = EraserTool()
        elif symbol in COLOR_SHORTCUTS:
            self.color = COLOR_SHORTCUTS[symbol]
        elif symbol == arcade.key.O:
            self.save_traces()
        elif symbol == arcade.key.L:
            self.load_traces()
        self.used_tools[self.tool.name] = self.tool

    def save_traces(self):
        try:
            root = tk.Tk()
            root.withdraw()
            filename = filedialog.asksaveasfilename(
                title="Guardar dibujo",
                defaultextension=".json",
                filetypes=[("Archivos JSON", "*.json")]
            )
            if not filename:
                return
            serializable = []
            for t in self.traces:
                color = t["color"]
                if isinstance(color, tuple):
                    color = list(color)
                serializable.append({
                    "tool": t["tool"],
                    "color": color,
                    "trace": [[int(p[0]), int(p[1])] for p in t["trace"]]
                })
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(serializable, f, indent=2)
        except Exception as e:
            print("Error guardando dibujo:", e)

    def load_traces(self):
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.askopenfilename(
            title="Seleccionar dibujo",
            filetypes=[("Archivos JSON", "*.json")]
        )
        if not filename:
            return
        try:
            with open(filename, "r", encoding="utf-8") as f:
                raw = json.load(f)
            self.traces = [
                {
                    "tool": t["tool"],
                    "color": tuple(t["color"]) if isinstance(t.get("color"), list) else t.get("color"),
                    "trace": [tuple(p) for p in t.get("trace", [])]
                } for t in raw
            ]
        except Exception as e:
            print("Error cargando dibujo:", e)

    def erase_at(self, x: int, y: int, radius: int = 20):
        r = radius
        if hasattr(self, "tool") and getattr(self.tool, "name", "") == "MARKER":
            r = int(radius * 1.8)
        rx2 = r * r
        remaining = []
        for t in self.traces:
            pts = t.get("trace", [])
            segments = []
            current = []
            for px, py in pts:
                dx = px - x
                dy = py - y
                if dx * dx + dy * dy > rx2:
                    current.append((px, py))
                else:
                    if len(current) >= 2:
                        segments.append(current)
                    elif len(current) == 1:
                        segments.append(current)
                    current = []
            if len(current) >= 2:
                segments.append(current)
            elif len(current) == 1:
                segments.append(current)
            for seg in segments:
                remaining.append({"tool": t["tool"], "color": t["color"], "trace": seg})
        self.traces = remaining

if __name__ == "__main__":
    window = arcade.Window(WIDTH, HEIGHT, TITLE)
    if len(sys.argv) > 1:
        app = Paint(sys.argv[1])
    else:
        app = Paint()
    window.show_view(app)
    arcade.run()
