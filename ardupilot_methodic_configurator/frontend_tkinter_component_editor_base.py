#!/usr/bin/env python3

"""
Component editor GUI that is not data dependent.

This file is part of Ardupilot methodic configurator. https://github.com/ArduPilot/MethodicConfigurator

SPDX-FileCopyrightText: 2024-2025 Amilcar do Carmo Lucas <amilcar.lucas@iav.de>

SPDX-License-Identifier: GPL-3.0-or-later
"""

import tkinter as tk
from argparse import ArgumentParser, Namespace

# from logging import debug as logging_debug
from logging import basicConfig as logging_basicConfig
from logging import getLevelName as logging_getLevelName
from logging import info as logging_info
from sys import exit as sys_exit
from tkinter import Menu, messagebox, simpledialog, ttk
from typing import Union

from ardupilot_methodic_configurator import _, __version__
from ardupilot_methodic_configurator.backend_filesystem import LocalFilesystem
from ardupilot_methodic_configurator.backend_filesystem_vehicle_components import VehicleComponents
from ardupilot_methodic_configurator.common_arguments import add_common_arguments
from ardupilot_methodic_configurator.frontend_tkinter_base import (
    BaseWindow,
    RichText,
    ScrollFrame,
    UsagePopupWindow,
    show_error_message,
    show_tooltip,
)


def argument_parser() -> Namespace:
    """
    Parses command-line arguments for the script.

    This function sets up an argument parser to handle the command-line arguments for the script.

    Returns:
    argparse.Namespace: An object containing the parsed arguments.

    """
    # pylint: disable=duplicate-code
    parser = ArgumentParser(
        description=_(
            "A GUI for editing JSON files that contain vehicle component configurations. "
            "Not to be used directly, but through the main ArduPilot methodic configurator script."
        )
    )
    parser = LocalFilesystem.add_argparse_arguments(parser)
    parser = ComponentEditorWindowBase.add_argparse_arguments(parser)
    return add_common_arguments(parser).parse_args()
    # pylint: enable=duplicate-code


class ComponentEditorWindowBase(BaseWindow):
    """
    A class for editing JSON files in the ArduPilot methodic configurator.

    This class provides a graphical user interface for editing JSON files that
    contain vehicle component configurations. It inherits from the BaseWindow
    class, which provides basic window functionality.
    """

    def __init__(self, version: str, local_filesystem: LocalFilesystem) -> None:
        super().__init__()
        self.local_filesystem = local_filesystem

        self.root.title(_("Amilcar Lucas's - ArduPilot methodic configurator ") + version + _(" - Vehicle Component Editor"))
        self.root.geometry("880x600")  # Set the window width

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.data = local_filesystem.load_vehicle_components_json_data(local_filesystem.vehicle_dir)
        if len(self.data) < 1:
            # Schedule the window to be destroyed after the mainloop has started
            self.root.after(100, self.root.destroy)  # Adjust the delay as needed
            return

        self.entry_widgets: dict[tuple, Union[ttk.Entry, ttk.Combobox]] = {}

        intro_frame = ttk.Frame(self.main_frame)
        intro_frame.pack(side=tk.TOP, fill="x", expand=False)

        style = ttk.Style()
        style.configure("bigger.TLabel", font=("TkDefaultFont", 14))
        style.configure("comb_input_invalid.TCombobox", fieldbackground="red")
        style.configure("comb_input_valid.TCombobox", fieldbackground="white")
        style.configure("entry_input_invalid.TEntry", fieldbackground="red")
        style.configure("entry_input_valid.TEntry", fieldbackground="white")

        explanation_text = _("Please configure all vehicle component properties in this window.\n")
        explanation_text += _("Scroll down and make sure you do not miss a property.\n")
        explanation_text += _("Saving the result will write to the vehicle_components.json file.")
        explanation_label = ttk.Label(intro_frame, text=explanation_text, wraplength=800, justify=tk.LEFT)
        explanation_label.configure(style="bigger.TLabel")
        explanation_label.pack(side=tk.LEFT, padx=(10, 10), pady=(10, 0), anchor=tk.NW)

        # Load the vehicle image and scale it down to image_height pixels in height
        if local_filesystem.vehicle_image_exists():
            image_label = self.put_image_in_label(intro_frame, local_filesystem.vehicle_image_filepath(), 100)
            image_label.pack(side=tk.RIGHT, anchor=tk.NE, padx=(4, 4), pady=(4, 0))
            show_tooltip(image_label, _("Replace the vehicle.jpg file in the vehicle directory to change the vehicle image."))
        else:
            image_label = ttk.Label(intro_frame, text=_("Add a 'vehicle.jpg' image file to the vehicle directory."))
            image_label.pack(side=tk.RIGHT, anchor=tk.NE, padx=(4, 4), pady=(4, 0))

        self.scroll_frame = ScrollFrame(self.main_frame)
        self.scroll_frame.pack(side="top", fill="both", expand=True)

        self.update_json_data()

        save_frame = ttk.Frame(self.main_frame)
        save_frame.pack(side=tk.TOP, fill="x", expand=False)
        self.save_button = ttk.Button(
            save_frame, text=_("Save data and start configuration"), command=self.validate_and_save_component_json
        )
        show_tooltip(self.save_button, _("Save component data and start parameter value configuration and tuning."))
        self.save_button.pack(pady=7)
        if UsagePopupWindow.should_display("component_editor"):
            self.root.after(10, self.__display_component_editor_usage_instructions(self.root))  # type: ignore[arg-type]

        self.template_controls = {"buttons": {}, "current_menu": None, "manager": VehicleComponents()}

    @staticmethod
    def __display_component_editor_usage_instructions(parent: tk.Toplevel) -> None:
        usage_popup_window = BaseWindow(parent)
        style = ttk.Style()

        instructions_text = RichText(
            usage_popup_window.main_frame, wrap=tk.WORD, height=5, bd=0, background=style.lookup("TLabel", "background")
        )
        instructions_text.insert(tk.END, _("1. Describe all vehicle component properties in the window below\n"))
        instructions_text.insert(tk.END, _("2. Scroll all the way down and make sure to edit all properties\n"))
        instructions_text.insert(tk.END, _("3. Do not be lazy, collect the required information and enter it\n"))
        instructions_text.insert(tk.END, _("4. Press the "))
        instructions_text.insert(tk.END, _("Save data and start configuration"), "italic")
        instructions_text.insert(tk.END, _(" only after all information is correct"))
        instructions_text.config(state=tk.DISABLED)

        UsagePopupWindow.display(
            parent,
            usage_popup_window,
            _("How to use the component editor window"),
            "component_editor",
            "690x200",
            instructions_text,
        )

    def update_json_data(self) -> None:  # should be overwritten in child classes
        if "Format version" not in self.data:
            self.data["Format version"] = 1

    def _set_component_value_and_update_ui(self, path: tuple, value: str) -> None:
        data_path = self.data["Components"]
        for key in path[:-1]:
            data_path = data_path[key]
        data_path[path[-1]] = value
        entry = self.entry_widgets[path]
        entry.delete(0, tk.END)
        entry.insert(0, value)
        entry.config(state="disabled")

    def populate_frames(self) -> None:
        """Populates the ScrollFrame with widgets based on the JSON data."""
        if "Components" in self.data:
            for key, value in self.data["Components"].items():
                self.__add_widget(self.scroll_frame.view_port, key, value, [])

    def __add_widget(self, parent: tk.Widget, key: str, value: dict, path: list) -> None:
        """
        Adds a widget to the parent widget with the given key and value.

        Args:
            parent (tkinter.Widget): The parent widget to which the LabelFrame/Entry will be added.
            key (str): The key for the LabelFrame/Entry.
            value (dict): The value associated with the key.
            path (list): The path to the current key in the JSON data.

        """
        if isinstance(value, dict):  # JSON non-leaf elements, add LabelFrame widget
            frame = ttk.LabelFrame(parent, text=_(key))
            is_toplevel = parent == self.scroll_frame.view_port
            pady = 5 if is_toplevel else 3
            frame.pack(
                fill=tk.X, side=tk.TOP if is_toplevel else tk.LEFT, pady=pady, padx=5, anchor=tk.NW if is_toplevel else tk.N
            )
            if is_toplevel and key in self.data.get("Components", {}):
                self._add_template_controls(frame, key)

            for sub_key, sub_value in value.items():
                # recursively add child elements
                self.__add_widget(frame, sub_key, sub_value, [*path, key])
        else:  # JSON leaf elements, add Entry widget
            entry_frame = ttk.Frame(parent)
            entry_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))

            label = ttk.Label(entry_frame, text=_(key))
            label.pack(side=tk.LEFT)

            entry = self.add_entry_or_combobox(value, entry_frame, (*path, key))
            entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

            # Store the entry widget in the entry_widgets dictionary for later retrieval
            self.entry_widgets[(*path, key)] = entry

    def _add_template_controls(self, parent_frame: ttk.LabelFrame, component_name: str) -> None:
        """Add template dropdown and save buttons for a component."""
        label_frame = ttk.Frame(parent_frame)
        label_frame.pack(side=tk.TOP, fill=tk.X)

        label = ttk.Label(label_frame, text=_("Template:"))
        label.pack(side=tk.LEFT, padx=(5, 5))

        # Create and add the dropdown button
        dropdown_button = ttk.Button(
            label_frame, text="▼", width=2, command=lambda k=component_name: self.show_template_options(k)
        )
        show_tooltip(dropdown_button, _("Select a template for this component"))
        dropdown_button.pack(side=tk.LEFT)

        # Create and add the save template button
        save_button = ttk.Button(
            label_frame, text="+", width=2, command=lambda k=component_name: self.save_component_as_template(k)
        )
        show_tooltip(save_button, _("Save current configuration as template"))
        save_button.pack(side=tk.LEFT, padx=(5, 0))

        # Store the dropdown button reference
        self.template_controls["buttons"][component_name] = dropdown_button

    def save_component_as_template(self, component_name: str) -> None:
        """Save the current component configuration as a template."""
        component_data = self.data["Components"].get(component_name, {})
        if not component_data:
            messagebox.showerror(_("Error"), _("No data for component: ") + component_name)
            return
        template_name = simpledialog.askstring(_("Save Template"), _("Enter a name for this template:"), parent=self.root)
        if not template_name:
            return

        templates = self.template_controls["manager"].load_component_templates()
        if component_name not in templates:
            templates[component_name] = []

        new_template = {"name": template_name, "data": component_data}

        for i, template in enumerate(templates[component_name]):
            if template.get("name") == template_name:
                confirm = messagebox.askyesno(_("Template exists"), _("A template with this name already exists. Overwrite?"))
                if confirm:
                    templates[component_name][i] = new_template
                    self.template_controls["manager"].save_component_templates(templates)
                    messagebox.showinfo(_("Template Saved"), _("Template has been updated"))
                return

        templates[component_name].append(new_template)
        self.template_controls["manager"].save_component_templates(templates)
        messagebox.showinfo(_("Template Saved"), _("Template has been saved"))

    def create_template_dropdown_button(self, parent: ttk.Frame, component_name: str) -> ttk.Button:
        """Creates a dropdown button for component templates."""
        button = ttk.Button(parent, text="▼", width=2, command=lambda: self.show_template_options(component_name))
        show_tooltip(button, _("Select a template for this component"))
        return button

    def show_template_options(self, component_name: str) -> None:
        """Shows a dropdown menu with template options for the component."""
        if hasattr(self, "current_dropdown_menu") and self.template_controls["current_menu"]:
            self.template_controls["current_menu"].unpost()

        button = self.template_controls["buttons"].get(component_name)
        if not button:
            return

        templates = self.template_controls["manager"].load_component_templates()
        component_templates = templates.get(component_name, [])

        menu = Menu(self.root, tearoff=0)

        if component_templates:
            for template in component_templates:
                template_name = template.get("name", "Template")
                menu.add_command(
                    label=template_name, command=lambda t=template, c=component_name: self.apply_component_template(c, t)
                )
        else:
            menu.add_command(label=_("No templates available"), state="disabled")

        x = button.winfo_rootx()
        y = button.winfo_rooty() + button.winfo_height()
        menu.post(x, y)

        self.template_controls["current_menu"] = menu

        def close_menu(_: tk.Event) -> None:
            if hasattr(self, "current_dropdown_menu") and self.template_controls["current_menu"]:
                self.template_controls["current_menu"].unpost()
                self.template_controls["current_menu"] = None
                self.root.unbind("<Button-1>", close_handler_id)

        close_handler_id = self.root.bind("<Button-1>", close_menu, add="+")

    def apply_component_template(self, component_name: str, template: dict) -> None:
        """Apply a template to a component."""
        if "data" not in template:
            return

        template_data = template["data"]
        self.data["Components"][component_name] = template_data

        for path, entry in self.entry_widgets.items():
            if len(path) >= 1 and path[0] == component_name:
                value = template_data
                try:
                    for key in path[1:]:
                        value = value[key]
                    entry.delete(0, tk.END)
                    entry.insert(0, str(value))
                except (KeyError, TypeError):
                    pass

        template_name = template.get("name", "Template")
        messagebox.showinfo(_("Template Applied"), _("{} has been applied to {}").format(template_name, component_name))

    def validate_and_save_component_json(self) -> None:
        """Saves the edited JSON data back to the file."""
        confirm_message = _(
            "ArduPilot Methodic Configurator only operates correctly if all component properties are correct."
            " ArduPilot parameter values depend on the components used and their connections.\n\n"
            " Have you used the scrollbar on the right side of the window and "
            "entered the correct values for all components?"
        )
        user_confirmation = messagebox.askyesno(_("Confirm that all component properties are correct"), confirm_message)

        if not user_confirmation:
            # User chose 'No', so return and do not save data
            return

        self.save_component_json()

    def save_component_json(self) -> None:
        # User confirmed, proceed with saving the data
        for path, entry in self.entry_widgets.items():
            value: Union[str, int, float] = entry.get()
            # Navigate through the nested dictionaries using the elements of the path
            current_data = self.data["Components"]
            for key in path[:-1]:
                current_data = current_data[key]

            if path[-1] != "Version":
                try:
                    value = int(value)
                except ValueError:
                    try:
                        value = float(value)
                    except ValueError:
                        value = str(value).strip()

            # Update the value in the data dictionary
            current_data[path[-1]] = value

        # Save the updated data back to the JSON file
        failed, msg = self.local_filesystem.save_vehicle_components_json_data(self.data, self.local_filesystem.vehicle_dir)
        if failed:
            show_error_message(_("Error"), _("Failed to save data to file.") + "\n" + msg)
        else:
            logging_info(_("Vehicle component data saved successfully."))
        self.root.destroy()

    def on_closing(self) -> None:
        """Handle window closing event."""
        answer = messagebox.askyesnocancel(_("Save Changes?"), _("Do you want to save the changes before closing?"))

        if answer is None:  # Cancel was clicked
            return

        if answer:
            self.save_component_json()
        else:
            self.root.destroy()
        sys_exit(0)

    # This function will be overwritten in child classes
    def add_entry_or_combobox(
        self, value: float, entry_frame: ttk.Frame, _path: tuple[str, str, str]
    ) -> Union[ttk.Entry, ttk.Combobox]:
        entry = ttk.Entry(entry_frame)
        entry.insert(0, str(value))
        return entry

    @staticmethod
    def add_argparse_arguments(parser: ArgumentParser) -> ArgumentParser:
        parser.add_argument(
            "--skip-component-editor",
            action="store_true",
            help=_(
                "Skip the component editor window. Only use this if all components have been configured. "
                "Default is %(default)s"
            ),
        )
        return parser


if __name__ == "__main__":
    args = argument_parser()

    logging_basicConfig(level=logging_getLevelName(args.loglevel), format="%(asctime)s - %(levelname)s - %(message)s")

    filesystem = LocalFilesystem(args.vehicle_dir, args.vehicle_type, "", args.allow_editing_template_files)
    app = ComponentEditorWindowBase(__version__, filesystem)
    app.root.mainloop()