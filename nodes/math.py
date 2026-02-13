"""MF PipoNodes — Math operation nodes."""


class MF_ModuloAdvanced:
    """
    A ComfyUI node that applies modulo operation, computes cycle count,
    and displays both results directly in the node.
    Cycle count is computed as input_number // modulo_value (stateless).
    """

    DESCRIPTION = "Computes modulo (remainder) and cycle count.\nOutputs: result = input mod value, cycle = input ÷ value (integer division)."

    CATEGORY = "MF_PipoNodes/Math"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_number": (
                    "INT",
                    {"default": 0, "min": -999999, "max": 999999, "step": 1},
                ),
                "modulo_value": (
                    "INT",
                    {"default": 10, "min": 1, "max": 999999, "step": 1},
                ),
            },
        }

    RETURN_TYPES = ("INT", "STRING", "INT", "STRING")
    RETURN_NAMES = (
        "modulo_result_int",
        "modulo_result_string",
        "cycle_count_int",
        "cycle_count_string",
    )
    FUNCTION = "apply_modulo_advanced"
    OUTPUT_NODE = True

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

    def apply_modulo_advanced(self, input_number, modulo_value):
        """Apply modulo operation and compute cycle count (stateless)."""
        modulo_result = input_number % modulo_value
        cycle_count = input_number // modulo_value

        text_output = f"🔢 {input_number} mod {modulo_value} = {modulo_result}\n🔄 Cycle: {cycle_count}"

        print(
            f"[MF_Modulo] {input_number} mod {modulo_value} = {modulo_result}, Cycle: {cycle_count}"
        )

        return {
            "ui": {
                "text": [text_output],
            },
            "result": (
                modulo_result,
                str(modulo_result),
                cycle_count,
                str(cycle_count),
            ),
        }


NODE_CLASS_MAPPINGS = {
    "MF_ModuloAdvanced": MF_ModuloAdvanced,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MF_ModuloAdvanced": "MF Modulo",
}
