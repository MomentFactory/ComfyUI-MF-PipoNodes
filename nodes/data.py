"""MF PipoNodes — Data I/O and utility nodes."""

import os
import json
import csv
import xml.etree.ElementTree as ET

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False
    print("[MF_PipoNodes] Warning: pyyaml not installed. YAML format disabled in Save/Read Data.")


class MF_SaveData:
    """
    A node that saves string data to various file formats
    """

    DESCRIPTION = "Saves string data to file.\nSupports JSON, CSV, XML, and YAML formats."

    @staticmethod
    def _clean_markdown_fences(data):
        """Remove markdown code fences if present"""
        if isinstance(data, str):
            data = data.strip()
            # Remove opening code fence (```json, ```xml, etc.)
            if data.startswith("```"):
                lines = data.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]  # Remove first line
                # Remove closing code fence
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]  # Remove last line
                data = "\n".join(lines)
        return data

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "data": ("STRING", {"forceInput": True}),
                "output_path": ("STRING", {"default": "output"}),
                "filename": ("STRING", {"default": "data"}),
                "format": (["json", "xml", "csv", "yaml"],),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("filepath",)
    FUNCTION = "save_data"
    CATEGORY = "MF_PipoNodes/Data"
    OUTPUT_NODE = True

    def save_data(self, data, output_path, filename, format):
        try:
            # Clean data - remove markdown code fences if present
            data = self._clean_markdown_fences(data)

            # Create output directory if it doesn't exist
            os.makedirs(output_path, exist_ok=True)

            # Build full filepath
            filepath = os.path.join(output_path, f"{filename}.{format}")

            # Save based on format
            if format == "json":
                self._save_json(data, filepath)
            elif format == "xml":
                self._save_xml(data, filepath)
            elif format == "csv":
                self._save_csv(data, filepath)
            elif format == "yaml":
                self._save_yaml(data, filepath)

            print(f"[MF Save Data] Saved to: {filepath}")
            return (filepath,)

        except Exception as e:
            print(f"[MF Save Data] Error: {str(e)}")
            return (f"Error: {str(e)}",)

    def _save_json(self, data, filepath):
        """Save as JSON"""
        try:
            # Try to parse if it's already JSON
            parsed = json.loads(data)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(parsed, f, indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            # If not valid JSON, just write the string as-is
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(data)

    def _save_xml(self, data, filepath):
        """Save as XML"""
        try:
            # Try to parse if it's already XML
            root = ET.fromstring(data)
            tree = ET.ElementTree(root)
            ET.indent(tree, space="  ")
            tree.write(filepath, encoding="utf-8", xml_declaration=True)
        except ET.ParseError:
            # If not valid XML, create a simple structure
            root = ET.Element("data")
            root.text = data
            tree = ET.ElementTree(root)
            ET.indent(tree, space="  ")
            tree.write(filepath, encoding="utf-8", xml_declaration=True)

    def _save_csv(self, data, filepath):
        """Save as CSV"""
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # Try to parse as JSON array first
            try:
                parsed = json.loads(data)
                if isinstance(parsed, list):
                    # If it's a list of dicts, write as proper CSV
                    if parsed and isinstance(parsed[0], dict):
                        writer.writerow(parsed[0].keys())
                        for row in parsed:
                            writer.writerow(row.values())
                    else:
                        # List of values
                        for item in parsed:
                            writer.writerow([item])
                else:
                    # Single value
                    writer.writerow([data])
            except Exception:
                # Just write as single row
                writer.writerow([data])

    def _save_yaml(self, data, filepath):
        """Save as YAML"""
        if not HAS_YAML:
            raise RuntimeError("pyyaml is not installed. Run: pip install pyyaml")
        try:
            # Try to parse as JSON first
            parsed = json.loads(data)
            with open(filepath, "w", encoding="utf-8") as f:
                yaml.dump(parsed, f, default_flow_style=False, allow_unicode=True)
        except json.JSONDecodeError:
            # Save as simple string
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(data)


class MF_ReadData:
    """
    A node that reads data from various file formats and outputs as string
    """

    DESCRIPTION = "Loads data from file and outputs as string.\nAuto-detects JSON, CSV, XML, and YAML formats."

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_path": ("STRING", {"default": "output"}),
                "filename": ("STRING", {"default": "data.json"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("data",)
    FUNCTION = "read_data"
    CATEGORY = "MF_PipoNodes/Data"

    def read_data(self, file_path, filename):
        try:
            # Build full filepath
            filepath = os.path.join(file_path, filename)

            if not os.path.exists(filepath):
                error_msg = f"File not found: {filepath}"
                print(f"[MF Read Data] {error_msg}")
                return (error_msg,)

            # Detect format from extension
            _, ext = os.path.splitext(filename)
            ext = ext.lower().lstrip(".")

            # Read based on format
            if ext == "json":
                data = self._read_json(filepath)
            elif ext == "xml":
                data = self._read_xml(filepath)
            elif ext == "csv":
                data = self._read_csv(filepath)
            elif ext in ["yaml", "yml"]:
                data = self._read_yaml(filepath)
            else:
                # Default: read as plain text
                with open(filepath, "r", encoding="utf-8") as f:
                    data = f.read()

            print(f"[MF Read Data] Read from: {filepath}")
            return (data,)

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"[MF Read Data] {error_msg}")
            return (error_msg,)

    def _read_json(self, filepath):
        """Read JSON and return as formatted string"""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return json.dumps(data, indent=2, ensure_ascii=False)

    def _read_xml(self, filepath):
        """Read XML and return as string"""
        tree = ET.parse(filepath)
        root = tree.getroot()
        ET.indent(root, space="  ")
        return ET.tostring(root, encoding="unicode")

    def _read_csv(self, filepath):
        """Read CSV and return as JSON string"""
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            data = list(reader)
            # If no headers detected, read as simple list
            if not data:
                f.seek(0)
                reader = csv.reader(f)
                data = [row for row in reader]
            return json.dumps(data, indent=2, ensure_ascii=False)

    def _read_yaml(self, filepath):
        """Read YAML and return as JSON string"""
        if not HAS_YAML:
            raise RuntimeError("pyyaml is not installed. Run: pip install pyyaml")
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return json.dumps(data, indent=2, ensure_ascii=False)


class MF_ShowData:
    """
    A node that displays string data in a text box in the UI
    """

    DESCRIPTION = "Displays string data in a text box within the node."

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "data": ("STRING", {"forceInput": True}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("data",)
    FUNCTION = "show_data"
    CATEGORY = "MF_PipoNodes/Data"
    OUTPUT_NODE = True

    @staticmethod
    def _clean_data(data):
        """Remove markdown code fences if present"""
        if isinstance(data, str):
            data = data.strip()
            # Remove opening code fence (```json, ```python, etc.)
            if data.startswith("```"):
                lines = data.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]  # Remove first line
                # Remove closing code fence
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]  # Remove last line
                data = "\n".join(lines)
        return data

    def show_data(self, data, unique_id=None):
        """Display the data in a text widget and pass it through"""
        # Clean the data (remove markdown code fences if present)
        cleaned_data = self._clean_data(data)

        # Print to console
        print("=" * 50)
        print("[MF Show Data]")
        print("=" * 50)
        print(cleaned_data)
        print("=" * 50)

        # Return cleaned data with UI display
        return {"ui": {"text": (cleaned_data,)}, "result": (cleaned_data,)}


class MF_CustomDropdownMenu:
    """
    A node with a customizable dropdown menu.
    The dropdown options can be edited via an EDIT button in the UI.
    Options are stored per-node and persist in the workflow file.
    Default options: low, medium, high, ultra (like video game graphics settings)
    """

    DESCRIPTION = "Dropdown menu with customizable options.\nClick EDIT to modify the list of choices."

    CATEGORY = "MF_PipoNodes/Utilities"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # Changed to STRING to accept any value
                # The dropdown is created and managed by JavaScript
                "selection": ("STRING", {"default": "medium"}),
                # CRITICAL: Must be in "required" or "optional" to serialize!
                # Using multiline=False and forceInput=False keeps it as a widget
                # JavaScript will hide it visually while keeping it serializable
                "dropdown_options": (
                    "STRING",
                    {
                        "default": "low\nmedium\nhigh\nultra",
                        "multiline": False,
                    },
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("selected_value",)
    FUNCTION = "execute"

    def execute(self, selection, dropdown_options="low\nmedium\nhigh\nultra"):
        """
        Returns the selected dropdown value as a string.

        Args:
            selection: The currently selected option from the dropdown
            dropdown_options: Hidden field containing all options (for workflow persistence)

        Returns:
            Tuple containing the selected string value
        """
        return (selection,)


NODE_CLASS_MAPPINGS = {
    "MF_SaveData": MF_SaveData,
    "MF_ReadData": MF_ReadData,
    "MF_ShowData": MF_ShowData,
    "MF_CustomDropdownMenu": MF_CustomDropdownMenu,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MF_SaveData": "MF Save Data (json/csv/xml/yaml)",
    "MF_ReadData": "MF Load Data (json/csv/xml/yaml)",
    "MF_ShowData": "MF Show Data",
    "MF_CustomDropdownMenu": "MF Dropdown Menu",
}
