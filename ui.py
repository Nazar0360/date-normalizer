from pyperclip import copy, paste
from date_functions import *
import customtkinter as ctk
from datetime import date
import re
import os

class DateNormalizeTool(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("date-normalizer")
        self.resizable(False, False)
        script_directory = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_directory, 'icon.ico')
        self.iconbitmap(icon_path)

        self.entry_names = ["Year", "Month", "Day", "Hour", "Minute", "Second"]
        self.input_entries = {}
        self.normalized_entries = {}
        self._clear_error_color = None
    
    def _validate_input(self, new_value, allow_negative=True, allow_fractions=True):
        if allow_fractions:
            regex = r'^[+-]?\d*\.?\d*$'
        else:
            regex = r'^[+-]?\d*$'
        if not allow_negative:
            regex = regex.replace("-", "")

        if re.match(regex, new_value) or new_value == "":
            return True
        return False
    
    def _get_entry(self, entry_name: str, is_normalized=False):
        if is_normalized:
            return self.normalized_entries.get(entry_name, None)
        return self.input_entries.get(entry_name, None)
    
    def get_date(self, is_normalized=False):
        date = []
        for name in self.entry_names:
            entry = self._get_entry(name, is_normalized)
            default_value = 1 if name in ["Year", "Month", "Day"] else 0
            value = entry._textvariable.get()
            if entry is not None:
                value = str2int(value, default_value) if name in ["Year", "Month"] else str2float(value, default_value)
            else:
                value = default_value
            date.append(value)
        return (*date, )
    
    def set_date(self, year, month, day, hour=0, minute=0, second=0, is_normalized=False):
        for name, value in zip(self.entry_names, [year, month, day, hour, minute, second]):
            entry = self._get_entry(name, is_normalized)
            if entry is not None:
                value = int(value) if round(value, 3) == value // 1 else value
                entry._textvariable.set(f"{value:0>2}" if  name != "Year" else f"{value:0>4}")
    
    def insert_now(self):
        now = datetime.now()
        self.set_date(now.year, now.month, now.day, now.hour, now.minute, now.second)
    
    def insert_today(self):
        today = date.today()
        self.set_date(today.year, today.month, today.day)
    
    def copy_normalized_date(self, date_format="%Y.%m.%d %H:%M:%S"):
        copy(date2str(*self.get_date(is_normalized=True), date_format=date_format))
    
    def paste_date(self, date_format="%Y.%m.%d %H:%M:%S"):
        date = paste().strip()
        try:
            date = str2date(date, date_format)
            check_date(*date)
        except Exception as e:
            print(e)
        self.set_date(*date)
    
    def _highlight_error(self, widgets, is_error=True):
        for widget in widgets:
            if isinstance(widget, ctk.CTkEntry):
                widget.configure(border_color="red" if is_error else "")
            elif isinstance(widget, ctk.CTkButton):
                widget.configure(fg_color="red" if is_error else "")
                widget.configure(hover="red" if is_error else "")

    
    def _update_normalized_date(self):
        date = self.get_date(is_normalized=False)
        try:
            normalized_date = normalize_date(*date)
        except ValueError as e:
            self._highlight_error(self.input_entries.values(), is_error=True)
            print(e)
            return
        except OverflowError as e:
            self._highlight_error(self.input_entries.values(), is_error=True)
            print(e)
            return
        self._highlight_error(self.input_entries.values(), is_error=False)
        self.set_date(*normalized_date, is_normalized=True)
    
    def create_widgets(self):
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(padx=10, pady=10)
        ctk.CTkLabel(button_frame, text="Insert:").pack(side=ctk.LEFT, padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Now", command=self.insert_now).pack(side=ctk.LEFT, padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Today", command=self.insert_today).pack(side=ctk.LEFT, padx=10, pady=5)

        vcmd = self.register(self._validate_input)
        vcmd_nn_nf = self.register(lambda new_value: self._validate_input(new_value, allow_negative=False, allow_fractions=False))

        for is_normalized in [False, True]:
            label = ctk.CTkLabel(self, text="Input Date:" if not is_normalized else "Normalized Date:", font=ctk.CTkFont(size=15))
            label.pack(side=ctk.TOP, pady=5)
            
            date_frame = ctk.CTkFrame(self)
            date_frame.pack(padx=10, pady=10)

            if not is_normalized:
                paste_button_frame = ctk.CTkFrame(self)
                paste_button_frame.pack(padx=10, pady=10)
                paste_button_label = ctk.CTkLabel(paste_button_frame, text="Paste Date:")
                paste_button_label.pack(side=ctk.LEFT, padx=10, pady=5)
                command_0 = lambda: self.paste_date(date_format="%Y.%m.%d")
                paste_button_0 = ctk.CTkButton(paste_button_frame, text="YYYY.MM.DD", command=command_0)
                paste_button_0.pack(side=ctk.LEFT, padx=10, pady=5)
                command_1 = lambda: self.paste_date(date_format="%d.%m.%Y")
                paste_button_1 = ctk.CTkButton(paste_button_frame, text="DD.MM.YYYY", command=command_1)
                paste_button_1.pack(side=ctk.LEFT, padx=10, pady=5)
                command_2 = lambda: self.paste_date(date_format="%Y.%m.%d %H:%M:%S")
                paste_button_0 = ctk.CTkButton(paste_button_frame, text="YYYY.MM.DD hh:mm:ss", command=command_2)
                paste_button_0.pack(side=ctk.LEFT, padx=10, pady=5)
                command_3 = lambda: self.paste_date(date_format="%d.%m.%Y %H:%M:%S")
                paste_button_1 = ctk.CTkButton(paste_button_frame, text="DD.MM.YYYY hh:mm:ss", command=command_3)
                paste_button_1.pack(side=ctk.LEFT, padx=10, pady=5)
            else:
                copy_button_frame = ctk.CTkFrame(self)
                copy_button_frame.pack(padx=10, pady=10)
                copy_button_label = ctk.CTkLabel(copy_button_frame, text="Copy Date:")
                copy_button_label.pack(side=ctk.LEFT, padx=10, pady=5)
                command_0 = lambda: self.copy_normalized_date(date_format="%Y.%m.%d")
                copy_button_0 = ctk.CTkButton(copy_button_frame, text="YYYY.MM.DD", command=command_0)
                copy_button_0.pack(side=ctk.LEFT, padx=10, pady=5)
                command_1 = lambda: self.copy_normalized_date(date_format="%d.%m.%Y")
                copy_button_1 = ctk.CTkButton(copy_button_frame, text="DD.MM.YYYY", command=command_1)
                copy_button_1.pack(side=ctk.LEFT, padx=10, pady=5)
                command_2 = lambda: self.copy_normalized_date(date_format="%Y.%m.%d %H:%M:%S")
                copy_button_0 = ctk.CTkButton(copy_button_frame, text="YYYY.MM.DD hh:mm:ss", command=command_2)
                copy_button_0.pack(side=ctk.LEFT, padx=10, pady=5)
                command_3 = lambda: self.copy_normalized_date(date_format="%d.%m.%Y %H:%M:%S")
                copy_button_1 = ctk.CTkButton(copy_button_frame, text="DD.MM.YYYY hh:mm:ss", command=command_3)
                copy_button_1.pack(side=ctk.LEFT, padx=10, pady=5)

            for name in self.entry_names:
                var = ctk.StringVar()
                entry = ctk.CTkEntry(date_frame, placeholder_text=name, width=90, textvariable=var)
                if is_normalized:
                    self.normalized_entries[name] = entry
                    entry.configure(state="readonly")
                else:
                    self.input_entries[name] = entry
                    var.trace_add("write", lambda *args: self._update_normalized_date())
                    if name in ["Year", "Month"]:
                        entry.configure(validate="key", validatecommand=(vcmd_nn_nf, '%P'))
                    else:
                        entry.configure(validate="key", validatecommand=(vcmd, '%P'))
                entry.pack(side=ctk.LEFT, padx=10, pady=5)
                if name in ["Year", "Month"]:
                    ctk.CTkLabel(date_frame, text=".").pack(side=ctk.LEFT)
                elif name == "Day":
                    ctk.CTkLabel(date_frame, text=" ").pack(side=ctk.LEFT)
                elif name in ["Hour", "Minute"]:
                    ctk.CTkLabel(date_frame, text=":").pack(side=ctk.LEFT)
        
        self.insert_today()
    
    def run(self):
        self.create_widgets()
        self.mainloop()

if __name__ == "__main__":
    app = DateNormalizeTool()
    app.run()