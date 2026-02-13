"""MF PipoNodes — Sequencing nodes (Shot Helper, Story Driver)."""

import random

# Simple in-memory step counter. No files. Resets on ComfyUI restart.
_steps = {}


class MF_ShotHelper:
    """
    A ComfyUI node that generates sequence and shot numbers based on a driving primitive
    and beat points. Sequences increment at each beat, and shot counters reset per sequence.
    """

    DESCRIPTION = (
        "Generates sequence and shot numbers from a step counter and beat points.\n\n"
        "Beats syntax (step numbers where new sequences start):\n"
        "• Comma-separated: 3,8,15\n"
        "• One per line: 3\\n8\\n15\n"
        "• Array format: [3,8,15]\n\n"
        "Output: seq01_shot01, seq01_shot02, ... seq02_shot01, etc."
    )

    CATEGORY = "MF_PipoNodes/Sequencing"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "step": ("INT", {"default": 0, "forceInput": True}),
                "beats": ("STRING", {"default": "", "multiline": True}),
            }
        }

    RETURN_TYPES = ("INT", "STRING", "INT", "STRING", "STRING")
    RETURN_NAMES = ("sequence_int", "sequence_str", "shot_int", "shot_str", "shot_name")
    FUNCTION = "calculate_sequence_shot"

    def calculate_sequence_shot(self, step, beats):
        """
        Calculate sequence and shot numbers based on current step and beat points.

        Args:
            step: Current step number (driving primitive)
            beats: Beat points in various formats:
                   - Comma-separated: "3,8,15"
                   - Newline-separated: "3\\n8\\n15"
                   - Array format: "[3,8,15]"

        Returns:
            tuple: (sequence_int, sequence_str, shot_int, shot_str, shot_name)
                   shot_name format: "seq01_shot01"
        """
        # Parse beats string into sorted list of integers
        beat_list = []
        if beats.strip():
            try:
                # Remove array brackets if present
                beats_clean = beats.strip()
                if beats_clean.startswith("[") and beats_clean.endswith("]"):
                    beats_clean = beats_clean[1:-1]

                # Replace newlines with commas for unified parsing
                beats_clean = beats_clean.replace("\n", ",")

                # Split by comma and parse integers
                beat_list = sorted(
                    [int(b.strip()) for b in beats_clean.split(",") if b.strip()]
                )
            except ValueError:
                print(
                    f"⚠️ [MF_ShotHelper] Invalid beats format '{beats}'. Using empty beats."
                )
                beat_list = []

        # Determine which sequence we're in
        sequence_num = 1
        shot_start = 0

        for beat in beat_list:
            if step >= beat:
                sequence_num += 1
                shot_start = beat
            else:
                break

        # Calculate shot number within the current sequence
        shot_num = step - shot_start + 1

        # Generate formatted outputs
        sequence_str = str(sequence_num)
        shot_str = str(shot_num)
        shot_name = f"seq{sequence_num:02d}_shot{shot_num:02d}"

        print(f"🎬 [MF_StorySequence] Step {step}: {shot_name}")

        return (sequence_num, sequence_str, shot_num, shot_str, shot_name)


class MF_StoryDriver:
    """
    A ComfyUI node that tracks story progression steps and manages seeds.
    Step increments each execution. Reset sets it back to 0.
    Seed is a separate input field the user controls directly.
    """

    DESCRIPTION = (
        "Tracks story progression with auto-incrementing step counter.\n"
        "Use with MF Story Sequence to manage sequences and shots.\n\n"
        "• step: Increments each execution (0, 1, 2, ...)\n"
        "• storySeed: Your seed value (randomized on node creation)\n"
        "• Reset button: Sets step back to 0"
    )

    CATEGORY = "MF_PipoNodes/Sequencing"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "projectName": ("STRING", {"default": "MyProject", "multiline": False}),
                "storySeed": (
                    "INT",
                    {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF},
                ),
                "randomize_seed_on_reset": ("BOOLEAN", {"default": True}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
            },
        }

    RETURN_TYPES = ("INT", "STRING", "STRING", "STRING", "INT")
    RETURN_NAMES = ("step_int", "step_str", "projectName", "saveFolder", "storySeed")
    FUNCTION = "execute"
    OUTPUT_NODE = True

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

    def execute(self, projectName, storySeed, randomize_seed_on_reset, unique_id=None):
        """Execute: read step, return it, increment for next time."""
        # Get current step (starts at 0)
        current_step = _steps.get(projectName, 0)

        # Store incremented value for next execution
        _steps[projectName] = current_step + 1

        # Prepare outputs
        project_name_output = projectName.replace(" ", "_")
        save_folder = f"{project_name_output}_{storySeed}"
        status_text = f"Step: {current_step} | Seed: {storySeed}"

        print(f"🎬 [MF_StoryDriver] {projectName}: Step {current_step}, Seed {storySeed}")

        return {
            "ui": {
                "status_display": [status_text],
            },
            "result": (
                current_step,
                str(current_step),
                project_name_output,
                save_folder,
                storySeed,
            ),
        }

    @classmethod
    def reset_project(cls, project_name):
        """Reset step to 0. That's it."""
        _steps[project_name] = 0
        print(f"🔄 [MF_StoryDriver] Reset '{project_name}' → step=0")


NODE_CLASS_MAPPINGS = {
    "MF_ShotHelper": MF_ShotHelper,
    "MF_StoryDriver": MF_StoryDriver,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MF_ShotHelper": "MF Story Sequence",
    "MF_StoryDriver": "MF Story Driver",
}
