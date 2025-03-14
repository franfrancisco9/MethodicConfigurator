"""
Manages vehicle components at the filesystem level.

This file is part of Ardupilot methodic configurator. https://github.com/ArduPilot/MethodicConfigurator

SPDX-FileCopyrightText: 2024-2025 Amilcar do Carmo Lucas <amilcar.lucas@iav.de>

SPDX-License-Identifier: GPL-3.0-or-later
"""

from json import JSONDecodeError
from json import dump as json_dump
from json import load as json_load

# from logging import info as logging_info
# from logging import warning as logging_warning
# from sys import exit as sys_exit
from logging import debug as logging_debug
from logging import error as logging_error
from os import makedirs as os_makedirs
from os import path as os_path
from os import walk as os_walk
from re import match as re_match
from typing import Any, Union

from jsonschema import ValidationError, validate

from ardupilot_methodic_configurator import _
from ardupilot_methodic_configurator.backend_filesystem_program_settings import ProgramSettings
from ardupilot_methodic_configurator.middleware_template_overview import TemplateOverview


class VehicleComponents:
    """
    This class provides methods to load and save
    vehicle components configurations from a JSON file.
    """

    def __init__(self) -> None:
        self.vehicle_components_json_filename = "vehicle_components.json"
        self.vehicle_components_schema_filename = "vehicle_components_schema.json"
        self.vehicle_components: Union[None, dict[Any, Any]] = None
        self.schema: Union[None, dict[Any, Any]] = None

    def load_schema(self) -> dict:
        """
        Load the JSON schema for vehicle components.

        :return: The schema as a dictionary
        """
        if self.schema is not None:
            return self.schema

        # Determine the location of the schema file
        schema_path = os_path.join(os_path.dirname(__file__), self.vehicle_components_schema_filename)

        try:
            with open(schema_path, encoding="utf-8") as file:
                self.schema = json_load(file)
            return self.schema
        except FileNotFoundError:
            logging_error(_("Schema file '%s' not found."), schema_path)
        except JSONDecodeError:
            logging_error(_("Error decoding JSON schema from file '%s'."), schema_path)
        return {}

    def load_component_templates(self) -> dict[str, list[dict]]:
        """
        Load component templates from the templates directory.

        :return: The templates as a dictionary
        """
        templates_filename = "vehicle_components_template.json"
        templates_dir = ProgramSettings.get_templates_base_dir()
        filepath = os_path.join(templates_dir, templates_filename)

        templates = {}
        try:
            with open(filepath, encoding="utf-8") as file:
                templates = json_load(file)
        except FileNotFoundError:
            logging_error(_("Templates file '%s' not found."), filepath)
        except JSONDecodeError:
            logging_error(_("Error decoding JSON templates from file '%s'."), filepath)
        return templates

    def save_component_templates(self, templates: dict) -> tuple[bool, str]:
        """
        Save component templates to the templates directory.

        :param templates: The templates to save
        :return: A tuple of (error_occurred, error_message)

        """
        templates_filename = "vehicle_components_template.json"
        templates_dir = ProgramSettings.get_templates_base_dir()
        filepath = os_path.join(templates_dir, templates_filename)

        try:
            os_makedirs(templates_dir, exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as file:
                json_dump(templates, file, indent=4)
        except FileNotFoundError:
            msg = _("Failed to save templates to file '{}': {}").format(filepath, _("File not found"))
            logging_error(msg)
            return True, msg
        return False, ""

    def validate_vehicle_components(self, data: dict) -> tuple[bool, str]:
        """
        Validate vehicle components data against the schema.

        :param data: The vehicle components data to validate
        :return: A tuple of (is_valid, error_message)
        """
        schema = self.load_schema()
        if not schema:
            return False, _("Could not load validation schema")

        try:
            validate(instance=data, schema=schema)
            return True, ""
        except ValidationError as e:
            return False, f"{_('Validation error')}: {e.message}"

    def load_vehicle_components_json_data(self, vehicle_dir: str) -> dict[Any, Any]:
        data: dict[Any, Any] = {}
        filepath = os_path.join(vehicle_dir, self.vehicle_components_json_filename)
        try:
            with open(filepath, encoding="utf-8") as file:
                data = json_load(file)

            # Validate the loaded data against the schema
            is_valid, error_message = self.validate_vehicle_components(data)
            if not is_valid:
                logging_error(_("Invalid vehicle components file '%s': %s"), filepath, error_message)
                # We still return the data even if invalid for debugging purposes
        except FileNotFoundError:
            # Normal users do not need this information
            logging_debug(_("File '%s' not found in %s."), self.vehicle_components_json_filename, vehicle_dir)
        except JSONDecodeError:
            logging_error(_("Error decoding JSON data from file '%s'."), filepath)
        self.vehicle_components = data
        return data

    def save_vehicle_components_json_data(self, data: dict, vehicle_dir: str) -> tuple[bool, str]:  # noqa: PLR0911 # pylint: disable=too-many-return-statements
        """
        Save the vehicle components data to a JSON file.

        :param data: The vehicle components data to save
        :param vehicle_dir: The directory to save the file in
        :return: A tuple of (error_occurred, error_message)
        """
        # Validate before saving
        # commented out until https://github.com/ArduPilot/MethodicConfigurator/pull/237 gets merged
        # is_valid, error_message = self.validate_vehicle_components(data)
        # if not is_valid:
        #     msg = _("Cannot save invalid vehicle components data: {}").format(error_message)
        #     logging_error(msg)
        #     return True, msg

        filepath = os_path.join(vehicle_dir, self.vehicle_components_json_filename)
        try:
            with open(filepath, "w", encoding="utf-8", newline="\n") as file:
                json_dump(data, file, indent=4)
        except FileNotFoundError:
            msg = _("Directory '{}' not found").format(vehicle_dir)
            logging_error(msg)
            return True, msg
        except PermissionError:
            msg = _("Permission denied when writing to file '{}'").format(filepath)
            logging_error(msg)
            return True, msg
        except IsADirectoryError:
            msg = _("Path '{}' is a directory, not a file").format(filepath)
            logging_error(msg)
            return True, msg
        except OSError as e:
            msg = _("OS error when writing to file '{}': {}").format(filepath, str(e))
            logging_error(msg)
            return True, msg
        except TypeError as e:
            msg = _("Type error when serializing data to JSON: {}").format(str(e))
            logging_error(msg)
            return True, msg
        except ValueError as e:
            msg = _("Value error when serializing data to JSON: {}").format(str(e))
            logging_error(msg)
            return True, msg
        except Exception as e:  # pylint: disable=broad-exception-caught
            # Still have a fallback for truly unexpected errors
            msg = _("Unexpected error saving data to file '{}': {}").format(filepath, str(e))
            logging_error(msg)
            return True, msg

        return False, ""

    def get_fc_fw_type_from_vehicle_components_json(self) -> str:
        if self.vehicle_components and "Components" in self.vehicle_components:
            components = self.vehicle_components["Components"]
        else:
            components = None
        if components:
            fw_type: str = components.get("Flight Controller", {}).get("Firmware", {}).get("Type", "")
            if fw_type in self.supported_vehicles():
                return fw_type
            error_msg = _("Firmware type {fw_type} in {self.vehicle_components_json_filename} is not supported")
            logging_error(error_msg.format(**locals()))
        return ""

    def get_fc_fw_version_from_vehicle_components_json(self) -> str:
        if self.vehicle_components and "Components" in self.vehicle_components:
            components = self.vehicle_components["Components"]
        else:
            components = None
        if components:
            version_str: str = components.get("Flight Controller", {}).get("Firmware", {}).get("Version", "")
            version_str = version_str.lstrip().split(" ")[0] if version_str else ""
            if re_match(r"^\d+\.\d+\.\d+$", version_str):
                return version_str
            error_msg = _("FW version string {version_str} on {self.vehicle_components_json_filename} is invalid")
            logging_error(error_msg.format(**locals()))
        return ""

    @staticmethod
    def supported_vehicles() -> tuple[str, ...]:
        return ("AP_Periph", "AntennaTracker", "ArduCopter", "ArduPlane", "ArduSub", "Blimp", "Heli", "Rover", "SITL")

    @staticmethod
    def get_vehicle_components_overviews() -> dict[str, TemplateOverview]:
        """
        Finds all subdirectories of the templates base directory containing a
        "vehicle_components.json" file, creates a dictionary where the keys are
        the subdirectory names (relative to templates base directory) and the
        values are instances of TemplateOverview.

        :return: A dictionary mapping subdirectory paths to TemplateOverview instances.
        """
        vehicle_components_dict = {}
        file_to_find = VehicleComponents().vehicle_components_json_filename
        template_default_dir = ProgramSettings.get_templates_base_dir()
        for root, _dirs, files in os_walk(template_default_dir):
            if file_to_find in files:
                relative_path = os_path.relpath(root, template_default_dir)
                vehicle_components = VehicleComponents()
                comp_data = vehicle_components.load_vehicle_components_json_data(root)
                if comp_data:
                    comp_data = comp_data.get("Components", {})
                    vehicle_components_overview = TemplateOverview(comp_data)
                    vehicle_components_dict[relative_path] = vehicle_components_overview

        return vehicle_components_dict

    @staticmethod
    def get_vehicle_image_filepath(relative_template_path: str) -> str:
        template_default_dir = ProgramSettings.get_templates_base_dir()
        return os_path.join(template_default_dir, relative_template_path, "vehicle.jpg")

    def wipe_component_info(self) -> None:
        """
        Wipe the vehicle components data by clearing all data from the vehicle_components dictionary.

        This resets the internal state without affecting any files.
        Preserves the complete structure of the dictionary including all branches and leaves,
        but sets leaf values to empty values based on their type.
        """
        if self.vehicle_components is not None:
            self._recursively_clear_dict(self.vehicle_components)

    def _recursively_clear_dict(self, data: Union[dict, list, float, bool, str]) -> None:
        """
        Recursively clear leaf values in a nested dictionary while preserving structure.

        :param data: Dictionary to clear
        """
        if not isinstance(data, dict):
            return

        for key, value in data.items():
            if isinstance(value, dict):
                # If it's a dictionary, recurse deeper
                self._recursively_clear_dict(value)
            elif isinstance(value, list):
                # If it's a list, preserve it but empty it
                data[key] = []
            elif isinstance(value, (int, float)):
                # For numerical values, set to 0
                data[key] = 0 if isinstance(value, int) else 0.0
            elif isinstance(value, bool):
                # For boolean values, set to False
                data[key] = False
            else:
                # For strings and other types, set to empty string or None
                data[key] = "" if isinstance(value, str) else None
