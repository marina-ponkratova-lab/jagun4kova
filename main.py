# Weather Diary — пошаговая инструкция по созданию приложения

## 1. Структура проекта

Создайте папку `weather_diary` и разместите в ней:
- файл `main.py` — основной код приложения;
- файл `diary.json` — для хранения данных;
- файл `.gitignore` — чтобы не отслеживать временные файлы;
- файл `README.md` — описание проекта.

## 2. Основной код (`main.py`)

```python
import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

DIARY_FILE = 'diary.json'

def load_data():
    try:
        with open(DIARY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(data):
    with open(DIARY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def validate_input():
    date = entry_date.get()
    temperature = entry_temperature.get()
    description = entry_description.get()

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД")
        return False

    if not temperature.replace('.', '', 1).isdigit():
        messagebox.showerror("Ошибка", "Температура должна быть числом")
        return False

    if not description.strip():
        messagebox.showerror("Ошибка", "Описание не должно быть пустым")
        return False

    return True

def add_entry():
    if validate_input():
        new_entry = {
            "date": entry_date.get(),
            "temperature": float(entry_temperature.get()),
            "description": entry_description.get(),
            "precipitation": bool(var_precipitation.get())
        }
        diary_entries.append(new_entry)
        save_data(diary_entries)
        refresh_table()
        clear_fields()

def refresh_table(filter_date=None, min_temp=None):
    for item in table.get_children():
        table.delete(item)
    for entry in diary_entries:
        if filter_date and entry["date"] != filter_date:
            continue
        if min_temp is not None and entry["temperature"] < min_temp:
            continue
        table.insert("", "end", values=(
            entry["date"],
            entry["temperature"],
            entry["description"],
            "Да" if entry["precipitation"] else "Нет"
        ))

def apply_filters():
    filter_date = entry_filter_date.get() if entry_filter_date.get() else None
    min_temp = float(entry_min_temp.get()) if entry_min_temp.get() else None
    refresh_table(filter_date, min_temp)

def clear_fields():
    entry_date.delete(0, tk.END)
    entry_temperature.delete(0, tk.END)
    entry_description.delete(0, tk.END)
    var_precipitation.set(False)

diary_entries = load_data()

root = tk.Tk()
root.title("Weather Diary")
root.geometry("800x500")

# Вкладка добавления записи
tab_control = ttk.Notebook(root)
tab_main = ttk.Frame(tab_control)
tab_filter = ttk.Frame(tab_control)
tab_control.add(tab_main, text="Добавить запись")
tab_control.add(tab_filter, text="Фильтр")
tab_control.pack(expand=1, fill="both")

# Вкладка "Добавить запись"
tk.Label(tab_main, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_date = tk.Entry(tab_main)
entry_date.grid(row=0, column=1, padx=5, pady=5)

tk.Label(tab_main, text="Температура:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_temperature = tk.Entry(tab_main)
entry_temperature.grid(row=1, column=1, padx=5, pady=5)

tk.Label(tab_main, text="Описание погоды:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_description = tk.Entry(tab_main)
entry_description.grid(row=2, column=1, padx=5, pady=5)

var_precipitation = tk.BooleanVar(value=False)
tk.Checkbutton(tab_main, text="Осадки", variable=var_precipitation).grid(row=3, column=0, columnspan=2, pady=5)

tk.Button(tab_main, text="Добавить запись", command=add_entry).grid(row=4, column=0, columnspan=2, pady=10)

# Таблица записей
table = ttk.Treeview(tab_main, columns=("Дата", "Температура", "Описание", "Осадки"), show="headings")
for col in ("Дата", "Температура", "Описание", "Осадки"):
    table.heading(col, text=col)
table.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
scrollbar = ttk.Scrollbar(tab_main, orient="vertical", command=table.yview)
scrollbar.grid(row=5, column=2, sticky="ns")
table.configure(yscrollcommand=scrollbar.set)

# Вкладка "Фильтр"
tk.Label(tab_filter, text="Фильтр по дате:").grid(row=0, column=0, padx=5, pady=5)
entry_filter_date = tk.Entry(tab_filter)
entry_filter_date.grid(row=0, column=1, padx=5, pady=5)

tk.Label(tab_filter, text="Минимальная температура:").grid(row=1, column=0, padx=5, pady=5)
entry_min_temp = tk.Entry(tab_filter)
entry_min_temp.grid(row=1, column=1, padx=5, pady=5)

tk.Button(tab_filter, text="Применить фильтры", command=apply_filters).grid(row=2, column=0, columnspan=2, pady=10)

refresh_table()
root.mainloop()
```

## 3. Файл `.gitignore`

```
__pycache__/
*.pyc
*.log
*.swp
*.bak
```
*(Если хотите хранить данные в Git — уберите `diary.json` из .gitignore)*
