"""
MF PipoNodes - ComfyUI Custom Nodes
Collection of utility nodes and workflow management tools
Author: Pierre Biet | Moment Factory | 2025
Version: 2.0.0
"""

from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

# Import server module to register API routes (reset buttons, etc.)
try:
    from .server import routes  # noqa: F401
except Exception as e:
    print(f"[MF_PipoNodes] Warning: Could not load server endpoints: {e}")
    print("[MF_PipoNodes] Reset buttons may not work, but nodes will function.")

WEB_DIRECTORY = "./web"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

print(f"[MF_PipoNodes] Loaded {len(NODE_CLASS_MAPPINGS)} nodes.")
