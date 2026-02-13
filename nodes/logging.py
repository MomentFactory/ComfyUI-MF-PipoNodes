"""MF PipoNodes — Logging nodes."""

import os
import datetime
import folder_paths


def _get_log_file_path(save_log_path, log_file_name, output_dir):
    """Helper to normalize log file path and name."""
    if save_log_path is None or save_log_path.strip() == "":
        save_log_path = output_dir

    if log_file_name is None or log_file_name.strip() == "":
        log_file_name = "logfile"

    if not log_file_name.lower().endswith(".txt"):
        log_file_name += ".txt"

    return os.path.join(save_log_path, log_file_name)


class MF_LogFile:
    """
    A ComfyUI node that writes timestamped log entries to a text file.
    """

    DESCRIPTION = "Appends text entries to a log file.\nOptional timestamp prefix for each entry."

    CATEGORY = "MF_PipoNodes/Logging"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "log_entry": ("STRING", {"multiline": True}),
            },
            "optional": {
                "save_log_path": (
                    "STRING",
                    {"default": folder_paths.get_output_directory()},
                ),
                "log_file_name": ("STRING", {"default": "logfile"}),
                "enable_timestamp": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("log_content",)
    FUNCTION = "write_log"
    OUTPUT_NODE = True

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

    def write_log(self, log_entry, save_log_path=None, log_file_name="logfile", enable_timestamp=True):
        """Write a log entry to file, optionally with timestamp."""
        try:
            log_file_path = _get_log_file_path(
                save_log_path, log_file_name, folder_paths.get_output_directory()
            )
            os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

            # Format entry with or without timestamp
            if enable_timestamp:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                formatted_entry = f"[{timestamp}] {log_entry}\n\n"
            else:
                formatted_entry = f"{log_entry}\n\n"

            # Write new entry (append mode to preserve log history)
            with open(log_file_path, "a", encoding="utf-8") as f:
                f.write(formatted_entry)

            # Read entire log for display
            with open(log_file_path, "r", encoding="utf-8") as f:
                log_content = f.read()

            print(f"📝 [MF_LogFile] Wrote entry to {log_file_path}")

            return {
                "ui": {
                    "log_display": [log_content],
                },
                "result": (log_content,),
            }

        except Exception as e:
            error_message = f"❌ Error writing log: {str(e)}"
            print(f"[MF_LogFile] {error_message}")
            return {
                "ui": {
                    "log_display": [error_message],
                },
                "result": (error_message,),
            }


class MF_LogReader:
    """
    A ComfyUI node that reads and displays log file content with live updates.
    """

    DESCRIPTION = "Reads and displays the contents of a log file."

    CATEGORY = "MF_PipoNodes/Logging"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "log_file_path": (
                    "STRING",
                    {"default": folder_paths.get_output_directory()},
                ),
                "log_file_name": ("STRING", {"default": "logfile"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("log_content",)
    FUNCTION = "read_log"
    OUTPUT_NODE = True

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

    def read_log(self, log_file_path=None, log_file_name=None):
        """Read log file content and display it in the node."""
        full_path = _get_log_file_path(log_file_path, log_file_name, folder_paths.get_output_directory())

        try:
            if os.path.exists(full_path):
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()

                print(
                    f"📖 [MF_LogReader] Read {len(content)} characters from {os.path.basename(full_path)}"
                )

                return {
                    "ui": {
                        "log_display": [content],
                    },
                    "result": (content,),
                }
            else:
                error_msg = f"⚠️ Log file not found: {full_path}"
                print(f"[MF_LogReader] {error_msg}")
                return {
                    "ui": {
                        "log_display": [error_msg],
                    },
                    "result": (error_msg,),
                }
        except Exception as e:
            error_message = f"❌ Error reading log file: {str(e)}"
            print(f"[MF_LogReader] {error_message}")
            return {
                "ui": {
                    "log_display": [error_message],
                },
                "result": (error_message,),
            }


NODE_CLASS_MAPPINGS = {
    "MF_LogFile": MF_LogFile,
    "MF_LogReader": MF_LogReader,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MF_LogFile": "MF Save Log File",
    "MF_LogReader": "MF Load Log File",
}
