from storage import save_data


def get_schedule(data, day=None):
    schedule = data.get("schedule", [])
    if not day or not day.strip():
        return schedule
    target = day.strip().lower()
    return [item for item in schedule if item["day"].strip().lower() == target]


def add_grade(data, subject, score, date_str, work_type, filepath=None):
    if not subject or not subject.strip():
        return False, "Укажите название предмета."
    if not date_str or not date_str.strip():
        return False, "Укажите дату."
    if not work_type or not work_type.strip():
        return False, "Укажите тип работы."

    try:
        score_int = int(score)
    except (ValueError, TypeError):
        return False, "Оценка должна быть числом от 2 до 5."

    if score_int < 2 or score_int > 5:
        return False, "Допустимая оценка — только от 2 до 5."

    next_id = max([g["id"] for g in data["grades"]], default=0) + 1
    data["grades"].append({
        "id": next_id,
        "subject": subject.strip(),
        "score": score_int,
        "date": date_str.strip(),
        "work_type": work_type.strip(),
    })
    save_data(data, filepath) if filepath else save_data(data)
    return True, f"Оценка {score_int} по предмету «{subject.strip()}» добавлена."


def get_grades_by_subject(data, subject=None):
    grades = data.get("grades", [])
    if not subject or not subject.strip():
        return grades
    target = subject.strip().lower()
    return [g for g in grades if target in g["subject"].lower()]


def calculate_average_grade(data, subject=None):
    grades = get_grades_by_subject(data, subject)
    if not grades:
        return 0.0
    return round(sum(g["score"] for g in grades) / len(grades), 2)


def delete_grade(data, grade_id, filepath=None):
    try:
        target_id = int(grade_id)
    except (ValueError, TypeError):
        return False, "Некорректный ID оценки."

    for item in data["grades"]:
        if item["id"] == target_id:
            data["grades"].remove(item)
            save_data(data, filepath) if filepath else save_data(data)
            return True, "Оценка удалена."
    return False, "Оценка не найдена."


def add_homework(data, subject, task, deadline, filepath=None):
    if not subject or not subject.strip():
        return False, "Укажите предмет."
    if not task or not task.strip():
        return False, "Введите текст домашнего задания."
    if not deadline or not deadline.strip():
        return False, "Укажите дедлайн."

    next_id = max([h["id"] for h in data["homework"]], default=0) + 1
    data["homework"].append({
        "id": next_id,
        "subject": subject.strip(),
        "task": task.strip(),
        "deadline": deadline.strip(),
        "status": "В работе",
    })
    save_data(data, filepath) if filepath else save_data(data)
    return True, "Домашнее задание добавлено."


def filter_homework(data, status=None):
    hw = data.get("homework", [])
    if not status or not status.strip():
        return hw
    return [h for h in hw if h["status"].lower() == status.strip().lower()]


def toggle_homework_status(data, hw_id, filepath=None):
    try:
        target_id = int(hw_id)
    except (ValueError, TypeError):
        return False, "Некорректный ID задания."

    for item in data["homework"]:
        if item["id"] == target_id:
            item["status"] = "Выполнено" if item["status"] == "В работе" else "В работе"
            save_data(data, filepath) if filepath else save_data(data)
            return True, f"Статус задания изменён на «{item['status']}»."
    return False, "Задание не найдено."


def delete_homework(data, hw_id, filepath=None):
    try:
        target_id = int(hw_id)
    except (ValueError, TypeError):
        return False, "Некорректный ID задания."

    for item in data["homework"]:
        if item["id"] == target_id:
            data["homework"].remove(item)
            save_data(data, filepath) if filepath else save_data(data)
            return True, "Домашнее задание удалено."
    return False, "Задание не найдено."
