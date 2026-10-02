"""Графический интерфейс приложения «Менеджер задач» (Tkinter).

Точка входа: запустите `python gui.py` после активации виртуального окружения.
"""

import tkinter as tk
from tkinter import messagebox

from classes import Task, TaskManager


class TaskManagerApp:
    """Окно приложения: форма ввода, кнопки и список задач."""

    def __init__(self, root):
        self.manager = TaskManager()
        self.root = root
        self.root.title("Менеджер задач")
        self.root.resizable(False, False)
        self.setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_ui(self):
        # --- Поля ввода ---
        tk.Label(self.root, text="Название:").grid(row=0, column=0, sticky="e", padx=6, pady=4)
        self.title_entry = tk.Entry(self.root, width=45)
        self.title_entry.grid(row=0, column=1, padx=6, pady=4)

        tk.Label(self.root, text="Описание:").grid(row=1, column=0, sticky="ne", padx=6, pady=4)
        self.desc_text = tk.Text(self.root, height=3, width=42)
        self.desc_text.grid(row=1, column=1, padx=6, pady=4)

        tk.Label(self.root, text="Срок (ГГГГ-ММ-ДД):").grid(row=2, column=0, sticky="e", padx=6, pady=4)
        self.date_entry = tk.Entry(self.root, width=45)
        self.date_entry.grid(row=2, column=1, padx=6, pady=4)

        # --- Кнопки ---
        tk.Button(self.root, text="Добавить", width=20, command=self.add_task).grid(
            row=3, column=0, padx=6, pady=6
        )
        tk.Button(self.root, text="Удалить", width=20, command=self.delete_task).grid(
            row=3, column=1, sticky="w", padx=6, pady=6
        )

        # --- Список задач ---
        tk.Label(self.root, text="Список задач:").grid(row=4, column=0, sticky="w", padx=6)
        self.tasks_listbox = tk.Listbox(self.root, width=60, height=10)
        self.tasks_listbox.grid(row=5, column=0, columnspan=2, padx=6, pady=(0, 4), sticky="we")

        self.status_label = tk.Label(self.root, text="", anchor="w", fg="gray")
        self.status_label.grid(row=6, column=0, columnspan=2, sticky="we", padx=6, pady=(0, 6))

        self.update_listbox()

    def add_task(self):
        """Добавляет новую задачу после проверки полей и формата даты."""
        title = self.title_entry.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()
        due_date = self.date_entry.get().strip()

        if not (title and description and due_date):
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return

        task = Task(title, description, due_date)
        if not task.has_valid_date():
            messagebox.showwarning(
                "Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД, например 2025-12-31"
            )
            return

        self.manager.add_task(task)
        self.update_listbox()
        self.clear_inputs()
        self.set_status(f'Задача "{title}" добавлена')

    def delete_task(self):
        """Удаляет выбранную в списке задачу."""
        selected = self.tasks_listbox.curselection()
        if not selected:
            messagebox.showinfo("Удаление", "Сначала выберите задачу в списке.")
            return

        index = selected[0]
        task = self.manager.tasks[index]
        if messagebox.askyesno("Удаление", f'Удалить задачу "{task.title}"?'):
            self.manager.delete_task(index)
            self.update_listbox()
            self.set_status(f'Задача "{task.title}" удалена')

    def update_listbox(self):
        """Перерисовывает список задач из менеджера."""
        self.tasks_listbox.delete(0, tk.END)
        for task in self.manager.tasks:
            self.tasks_listbox.insert(tk.END, f"{task.title} (до {task.due_date})")
        self.set_status(f"Всего задач: {len(self.manager.tasks)}")

    def clear_inputs(self):
        """Очищает поля ввода."""
        self.title_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.date_entry.delete(0, tk.END)
        self.title_entry.focus_set()

    def set_status(self, text):
        """Показывает сообщение в строке состояния."""
        self.status_label.config(text=text)

    def on_close(self):
        """При закрытии окна принудительно сохраняет задачи."""
        self.manager.save_to_file()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
