"""MF PipoNodes — Visualization nodes (Graph Plotter)."""

import os
import json

# State files live in the package root (one level up from nodes/)
_PACKAGE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_GRAPH_STATE_FILE = os.path.join(_PACKAGE_ROOT, "graph_plotter_state.json")


def _read_graph_state():
    """Read graph plotter state from file. Returns dict."""
    if os.path.exists(_GRAPH_STATE_FILE):
        try:
            with open(_GRAPH_STATE_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ [MF_GraphPlotter] Could not read state: {e}")
    return {}


def _write_graph_state(state):
    """Write graph plotter state to file."""
    try:
        with open(_GRAPH_STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"❌ [MF_GraphPlotter] Error writing state: {e}")


class MF_GraphPlotter:
    """
    A ComfyUI node that plots X,Y integer data points on a graph.
    Stores history across executions and displays interactive chart.
    """

    DESCRIPTION = (
        "Plots Y values over time as a line graph.\n"
        "X auto-increments with each execution.\n\n"
        "• Reset Graph: Clears all data points\n"
        "• Save Graph: Exports chart as JPEG image"
    )

    CATEGORY = "MF_PipoNodes/Analysis"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Y": (
                    "INT",
                    {"default": 0, "min": -999999, "max": 999999, "forceInput": True},
                ),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "plot_graph"
    OUTPUT_NODE = True

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # Always execute to update graph
        return float("nan")

    def plot_graph(self, Y, unique_id=None):
        """
        Add data point and update graph. X auto-increments per execution.
        Always reads fresh state from disk.
        """
        # Read current state from file
        state = _read_graph_state()

        # Get or create node entry
        node_id = str(unique_id) if unique_id else "default"
        if node_id not in state:
            state[node_id] = {"x_data": [], "y_data": []}

        node_data = state[node_id]

        # Auto-increment X (step number = current point count + 1)
        X = len(node_data["x_data"]) + 1

        # Add new data point
        node_data["x_data"].append(X)
        node_data["y_data"].append(Y)

        # Write updated state back to file
        _write_graph_state(state)

        # Prepare data for frontend
        graph_data = {
            "x_values": node_data["x_data"],
            "y_values": node_data["y_data"],
            "node_id": node_id,
            "point_count": len(node_data["x_data"]),
        }

        print(f"📊 [MF_GraphPlotter] Step {X}: Y={Y}")

        return {
            "ui": {
                "graph_data": [graph_data],
            },
            "result": (),
        }

    @classmethod
    def reset_node_data(cls, node_id):
        """Reset graph data for a specific node. Uses same file functions as plot_graph."""
        state = _read_graph_state()

        state[node_id] = {"x_data": [], "y_data": []}

        _write_graph_state(state)
        print(f"🔄 [MF_GraphPlotter] Reset node {node_id} (file: {_GRAPH_STATE_FILE})")


NODE_CLASS_MAPPINGS = {
    "MF_GraphPlotter": MF_GraphPlotter,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MF_GraphPlotter": "MF Graph Plotter",
}
