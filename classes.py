"""Классы предметной области приложения «Менеджер задач».

Task описывает отдельную задачу, TaskManager управляет списком задач
и отвечает за сохранение/загрузку задач в JSON-файл.
"""

import json
from datetime import datetime


class Task:
    """Отдельная задача: название, описание и срок выполнения."""

    def __init__(self, title, description, due_date):
        self.title = title
        self.description = description
        self.due_date = due_date  # строка в формате ГГГГ-ММ-ДД

    @property
    def due_date_as_date(self):
        """Срок выполнения как объект date (None, если дата некорректна)."""
        try:
            return datetime.strptime(self.due_date, "%Y-%m-%d").date()
        except (TypeError, ValueError):
            return None

    def has_valid_date(self):
        """True, если срок выполнения задан в правильном формате ГГГГ-ММ-ДД."""
        return self.due_date_as_date is not None

    def to_dict(self):
        """Сериализует задачу в словарь для сохранения в JSON."""
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
        }

    @classmethod
    def from_dict(cls, data):
        """Создаёт задачу из словаря, прочитанного из JSON."""
        return cls(data["title"], data["description"], data["due_date"])

    def __str__(self):
        return f"{self.title} (до {self.due_date})"


class TaskManager:
    """Управляет списком задач и файловыми операциями (JSON)."""

    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_from_file()

    def add_task(self, task):
        """Добавляет задачу в список и сразу сохраняет файл."""
        self.tasks.append(task)
        self.save_to_file()

    def delete_task(self, index):
        """Удаляет задачу по индексу (если он корректен) и сохраняет файл."""
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_to_file()

    def save_to_file(self):
        """Сохраняет все задачи в JSON-файл."""
        data = [task.to_dict() for task in self.tasks]
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_from_file(self):
        """Загружает задачи из JSON-файла; если файла нет — пустой список."""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.tasks = [Task.from_dict(item) for item in data]
        except FileNotFoundError:
            self.tasks = []
        except (json.JSONDecodeError, KeyError, TypeError):
            # Повреждённый или неожиданный файл: начинаем с пустого списка,
            # чтобы приложение продолжало работать.
            self.tasks = []
