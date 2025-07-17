import tkinter as tk
from tkinter import ttk, messagebox
from db import init_db, get_connection

class TabbedFrame(ttk.Frame):
    def __init__(self, parent, tab_names, on_tab_change=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.grid(row=0, column=0, sticky='nsew')
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky='nsew')
        self.tabs = {}
        self.on_tab_change = on_tab_change

        for name in tab_names:
            self.add_tab(name)

        self.notebook.bind("<<NotebookTabChanged>>", self._tab_changed)

    def add_tab(self, name):
        frame = ttk.Frame(self.notebook)
        frame.grid(row=0, column=0, sticky='nsew')
        self.notebook.add(frame, text=name)
        self.tabs[name] = frame

    def _tab_changed(self, event):
        if self.on_tab_change:
            selected = self.notebook.tab(self.notebook.select(), "text")
            self.on_tab_change(selected)

def get_credit_card_names():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM credit_cards")
    names = [row[0] for row in cursor.fetchall()]
    conn.close()
    return names

def add_card_to_db(name, bank, balance, apr, min_payment, notes):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO credit_cards (name, bank, balance, apr, min_payment, user_notes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, bank, balance, apr, min_payment, notes))
    conn.commit()
    conn.close()

def show_add_card_form(parent, refresh_callback):
    for widget in parent.winfo_children():
        widget.destroy()  # clear existing widgets

    tk.Label(parent, text="Card Name").grid(row=0, column=0, sticky='w')
    name_entry = tk.Entry(parent)
    name_entry.grid(row=0, column=1)

    tk.Label(parent, text="Bank").grid(row=1, column=0, sticky='w')
    bank_entry = tk.Entry(parent)
    bank_entry.grid(row=1, column=1)

    tk.Label(parent, text="Balance").grid(row=2, column=0, sticky='w')
    balance_entry = tk.Entry(parent)
    balance_entry.grid(row=2, column=1)

    tk.Label(parent, text="APR (%)").grid(row=3, column=0, sticky='w')
    apr_entry = tk.Entry(parent)
    apr_entry.grid(row=3, column=1)

    tk.Label(parent, text="Minimum Payment").grid(row=4, column=0, sticky='w')
    min_payment_entry = tk.Entry(parent)
    min_payment_entry.grid(row=4, column=1)

    tk.Label(parent, text="Notes").grid(row=5, column=0, sticky='w')
    notes_entry = tk.Entry(parent)
    notes_entry.grid(row=5, column=1)

    def save_card():
        try:
            add_card_to_db(
                name_entry.get(),
                bank_entry.get(),
                float(balance_entry.get()),
                float(apr_entry.get()),
                float(min_payment_entry.get()),
                notes_entry.get()
            )
            messagebox.showinfo("Success", "Card added!")
            refresh_callback()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add card: {e}")

    save_btn = tk.Button(parent, text="Save Card", command=save_card)
    save_btn.grid(row=6, column=0, columnspan=2, pady=10)

def create_main_window():
    root = tk.Tk()
    root.title("Personal Finance Manager")
    root.geometry("1200x800")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    init_db()

    level1_names = ['Finances', 'Houses', 'Plots']
    level1 = TabbedFrame(root, level1_names)

    # Finances → Level 2 tabs
    finances_frame = level1.tabs['Finances']
    finances_frame.rowconfigure(0, weight=1)
    finances_frame.columnconfigure(0, weight=1)

    def refresh_credit_card_tabs():
        # clear and rebuild Level 3 tabs
        cc_frame = finances_tabs.tabs['Credit Cards']
        for widget in cc_frame.winfo_children():
            widget.destroy()
        card_names = get_credit_card_names() + ['Add Card']
        new_cc_tabs = TabbedFrame(cc_frame, card_names, on_tab_change=on_credit_card_tab_change)

    finances_tabs = TabbedFrame(finances_frame, ['Credit Cards', 'Loans', 'Liquid Accounts', 'Retirement Accounts'])

    def on_credit_card_tab_change(selected_tab):
        if selected_tab == 'Add Card':
            show_add_card_form(cc_tabs.tabs['Add Card'], refresh_credit_card_tabs)

    # Credit Cards → Level 3 tabs
    cc_frame = finances_tabs.tabs['Credit Cards']
    cc_frame.rowconfigure(0, weight=1)
    cc_frame.columnconfigure(0, weight=1)
    card_names = get_credit_card_names() + ['Add Card']
    cc_tabs = TabbedFrame(cc_frame, card_names, on_tab_change=on_credit_card_tab_change)

    root.mainloop()

if __name__ == "__main__":
    create_main_window()
