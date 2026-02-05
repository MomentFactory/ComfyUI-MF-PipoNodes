"""MF PipoNodes — Node package. Merges all sub-module registrations."""

from .random import NODE_CLASS_MAPPINGS as _random_cls, NODE_DISPLAY_NAME_MAPPINGS as _random_disp
from .text import NODE_CLASS_MAPPINGS as _text_cls, NODE_DISPLAY_NAME_MAPPINGS as _text_disp
from .logging import NODE_CLASS_MAPPINGS as _log_cls, NODE_DISPLAY_NAME_MAPPINGS as _log_disp
from .math import NODE_CLASS_MAPPINGS as _math_cls, NODE_DISPLAY_NAME_MAPPINGS as _math_disp
from .sequencing import NODE_CLASS_MAPPINGS as _seq_cls, NODE_DISPLAY_NAME_MAPPINGS as _seq_disp
from .visualization import NODE_CLASS_MAPPINGS as _viz_cls, NODE_DISPLAY_NAME_MAPPINGS as _viz_disp
from .data import NODE_CLASS_MAPPINGS as _data_cls, NODE_DISPLAY_NAME_MAPPINGS as _data_disp

NODE_CLASS_MAPPINGS = {
    **_random_cls,
    **_text_cls,
    **_log_cls,
    **_math_cls,
    **_seq_cls,
    **_viz_cls,
    **_data_cls,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    **_random_disp,
    **_text_disp,
    **_log_disp,
    **_math_disp,
    **_seq_disp,
    **_viz_disp,
    **_data_disp,
}

# Re-export stateful classes so server/routes.py can import them
from .sequencing import MF_StoryDriver
from .visualization import MF_GraphPlotter
