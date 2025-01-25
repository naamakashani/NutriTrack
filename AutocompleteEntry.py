import tkinter as tk
from tkinter import ttk


class AutocompleteEntry(ttk.Entry):
    def __init__(self, master, food_list, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.food_list = sorted(food_list, key=str.lower)
        self.var = self["textvariable"] = tk.StringVar()
        self.var.trace_add("write", self.show_suggestions)
        self.suggestion_listbox = None

    def show_suggestions(self, *args):
        user_input = self.var.get().lower()
        if not user_input:
            self.destroy_suggestion_listbox()
            return

        #matches = [food for food in self.food_list if user_input in food.lower()]
        # Filter matches and sort by length first, then alphabetically
        matches = sorted(
            [food for food in self.food_list if user_input in food.lower()],
            key=lambda x: (len(x), x.lower())
        )
        if not matches:
            self.destroy_suggestion_listbox()
            return

        if not self.suggestion_listbox:
            self.suggestion_listbox = tk.Listbox(self.master, height=5)
            self.suggestion_listbox.bind("<<ListboxSelect>>", self.select_suggestion)
            self.suggestion_listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())

        self.suggestion_listbox.delete(0, tk.END)
        for match in matches:
            self.suggestion_listbox.insert(tk.END, match)

    def destroy_suggestion_listbox(self):
        if self.suggestion_listbox:
            self.suggestion_listbox.destroy()
            self.suggestion_listbox = None

    def select_suggestion(self, event):
        if self.suggestion_listbox:
            selected = self.suggestion_listbox.get(tk.ACTIVE)
            self.var.set(selected)
            self.destroy_suggestion_listbox()
