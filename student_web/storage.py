import json
import os


class StorageError(Exception):
    """Ошибка чтения или структуры файла базы данных."""


DEFAULT_FILE = os.path.join("data", "student_data.json")

INITIAL_DATA = {
    "schedule": [
        {"day": "Понедельник", "pair": 1, "time": "09:00-10:30", "subject": "Веб-разработка", "cabinet": "305", "teacher": "Иванов И.И."},
        {"day": "Понедельник", "pair": 2, "time": "10:40-12:10", "subject": "Базы данных", "cabinet": "210", "teacher": "Петрова А.С."},
        {"day": "Вторник", "pair": 1, "time": "09:00-10:30", "subject": "Программирование на Python", "cabinet": "305", "teacher": "Иванов И.И."},
        {"day": "Среда", "pair": 2, "time": "10:40-12:10", "subject": "Высшая математика", "cabinet": "401", "teacher": "Сидоров В.П."},
        {"day": "Четверг", "pair": 1, "time": "09:00-10:30", "subject": "Операционные системы", "cabinet": "308", "teacher": "Кузнецов Д.А."},
    ],
    "grades": [
        {"id": 1, "subject": "Веб-разработка", "score": 5, "date": "2026-10-12", "work_type": "Практика"},
        {"id": 2, "subject": "Базы данных", "score": 4, "date": "2026-10-15", "work_type": "Контрольная"},
        {"id": 3, "subject": "Программирование на Python", "score": 5, "date": "2026-10-18", "work_type": "Лабораторная"},
        {"id": 4, "subject": "Высшая математика", "score": 4, "date": "2026-10-20", "work_type": "Тест"},
    ],
    "homework": [
        {"id": 1, "subject": "Веб-разработка", "task": "Сверстать страницу личного кабинета", "deadline": "2026-11-15", "status": "В работе"},
        {"id": 2, "subject": "Базы данных", "task": "Спроектировать ER-диаграмму", "deadline": "2026-11-12", "status": "Выполнено"},
        {"id": 3, "subject": "Программирование на Python", "task": "Покрыть логику тестами pytest", "deadline": "2026-11-18", "status": "В работе"},
    ],
}


def load_data(filepath=DEFAULT_FILE):
    folder = os.path.dirname(filepath)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        save_data(INITIAL_DATA, filepath)
        return json.loads(json.dumps(INITIAL_DATA)), "Создано новое хранилище со стартовыми данными."

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict) or not all(k in data for k in ("schedule", "grades", "homework")):
                raise StorageError("Нарушена структура JSON.")
            return data, ""
    except json.JSONDecodeError as exc:
        raise StorageError(f"Файл базы данных повреждён: {exc}") from exc


def save_data(data, filepath=DEFAULT_FILE):
    folder = os.path.dirname(filepath)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
