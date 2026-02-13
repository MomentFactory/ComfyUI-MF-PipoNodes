"""MF PipoNodes — Text processing nodes."""


def _normalize_text_lines(text):
    """Normalize line endings and split text into lines."""
    return text.replace("\r\n", "\n").replace("\r", "\n").split("\n")


class MF_LineCounter:
    """
    A ComfyUI node that counts the number of lines in a multiline string input
    and outputs both integer and string representations of the count.
    """

    DESCRIPTION = "Counts the number of lines in a text input."

    CATEGORY = "MF_PipoNodes/Utilities"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": (
                    "STRING",
                    {"multiline": True, "default": "Line 1\nLine 2\nLine 3"},
                ),
            }
        }

    RETURN_TYPES = ("INT", "STRING")
    RETURN_NAMES = ("line_count_int", "line_count_str")
    FUNCTION = "count_lines"

    def count_lines(self, text):
        """Count the number of lines in the input text."""
        if not text.strip():
            return (0, "0")

        lines = _normalize_text_lines(text)
        line_count = len(lines)

        return (line_count, str(line_count))


class MF_LineSelect:
    """
    A node that selects a specific line from a text input based on the provided index.
    Every line break is counted, including empty lines.
    """

    DESCRIPTION = "Selects a specific line from text by index (0-based)."

    CATEGORY = "MF_PipoNodes/Utilities"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "line_index": ("INT", {"default": 0, "min": 0, "max": 1000, "step": 1}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("selected_line",)
    FUNCTION = "select_line"

    def select_line(self, text, line_index):
        """Select a specific line from the input text based on index."""
        lines = _normalize_text_lines(text)

        if line_index < 0 or line_index >= len(lines):
            error_msg = f"⚠️ Line index {line_index} out of range (0-{len(lines) - 1})"
            print(f"[MF_LineSelect] {error_msg}")
            return (error_msg,)

        return (lines[line_index],)


NODE_CLASS_MAPPINGS = {
    "MF_LineCounter": MF_LineCounter,
    "MF_LineSelect": MF_LineSelect,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MF_LineCounter": "MF Line Counter",
    "MF_LineSelect": "MF Line Select",
}
