"""MF PipoNodes — Random category nodes."""

import random


class MF_DiceRoller:
    """
    A ComfyUI node that simulates dice rolling with various dice types.
    Outputs both integer and string representations of the roll result.
    """

    DESCRIPTION = (
        "Rolls a dice and outputs the result.\n\n"
        "• D4, D6, D8, D10, D12, D20, D100: Standard dice\n"
        "• DCustom: Use custom_faces to set any number of sides"
    )

    CATEGORY = "MF_PipoNodes/Random"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "dice": (
                    ["D4", "D6", "D8", "D10", "D12", "D20", "D100", "DCustom"],
                    {"default": "D6"},
                ),
            },
            "optional": {
                "custom_faces": (
                    "INT",
                    {"default": 6, "min": 1, "max": 999999, "step": 1},
                ),
            },
        }

    RETURN_TYPES = (
        "INT",
        "STRING",
    )
    RETURN_NAMES = (
        "int",
        "string",
    )
    FUNCTION = "roll_dice"
    OUTPUT_NODE = True

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

    def roll_dice(self, dice, custom_faces=6):
        """Roll the specified dice and return the result."""
        if dice == "DCustom":
            max_value = custom_faces
        else:
            max_value = int(dice[1:])
        result = random.randint(1, max_value)

        dice_label = f"D{max_value}" if dice == "DCustom" else dice
        print(f"🎲 Rolled {dice_label}: {result}")

        text_output = f"🎲 {result}"

        return {
            "ui": {
                "text": [text_output],
            },
            "result": (
                result,
                str(result),
            ),
        }


NODE_CLASS_MAPPINGS = {
    "MF_DiceRoller": MF_DiceRoller,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MF_DiceRoller": "MF Dice Roller",
}
