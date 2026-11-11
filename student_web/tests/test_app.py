import pytest
from storage import load_data, StorageError
from cabinet import (
    get_schedule,
    add_grade,
    calculate_average_grade,
    delete_grade,
    add_homework,
    filter_homework,
    toggle_homework_status,
)


@pytest.fixture
def sample_data():
    return {
        "schedule": [
            {"day": "Понедельник", "pair": 1, "time": "09:00-10:30", "subject": "Веб-разработка", "cabinet": "305", "teacher": "Иванов И.И."},
        ],
        "grades": [
            {"id": 1, "subject": "Веб-разработка", "score": 5, "date": "2026-10-10", "work_type": "Практика"},
            {"id": 2, "subject": "Веб-разработка", "score": 4, "date": "2026-10-12", "work_type": "Тест"},
        ],
        "homework": [
            {"id": 1, "subject": "Веб-разработка", "task": "Сделать сайт", "deadline": "2026-11-20", "status": "В работе"},
        ],
    }


def test_01_schedule_filter(sample_data):
    assert len(get_schedule(sample_data, "понедельник")) == 1
    assert len(get_schedule(sample_data, "пятница")) == 0


def test_02_add_grade_valid(sample_data, tmp_path):
    db = tmp_path / "db.json"
    ok, _ = add_grade(sample_data, "Базы данных", 5, "2026-11-01", "Тест", filepath=str(db))
    assert ok is True
    assert len(sample_data["grades"]) == 3


def test_03_add_grade_invalid_range(sample_data, tmp_path):
    db = tmp_path / "db.json"
    ok, _ = add_grade(sample_data, "Базы данных", 7, "2026-11-01", "Тест", filepath=str(db))
    assert ok is False


def test_04_add_grade_empty_field(sample_data, tmp_path):
    db = tmp_path / "db.json"
    ok, _ = add_grade(sample_data, "", 4, "2026-11-01", "Тест", filepath=str(db))
    assert ok is False


def test_05_average_grade(sample_data):
    assert calculate_average_grade(sample_data, "Веб-разработка") == 4.5


def test_06_delete_grade(sample_data, tmp_path):
    db = tmp_path / "db.json"
    ok, _ = delete_grade(sample_data, 1, filepath=str(db))
    assert ok is True
    assert len(sample_data["grades"]) == 1


def test_07_add_homework(sample_data, tmp_path):
    db = tmp_path / "db.json"
    ok, _ = add_homework(sample_data, "Python", "Написать тесты", "2026-11-25", filepath=str(db))
    assert ok is True
    assert len(sample_data["homework"]) == 2


def test_08_filter_homework(sample_data):
    assert len(filter_homework(sample_data, "В работе")) == 1
    assert len(filter_homework(sample_data, "Выполнено")) == 0


def test_09_toggle_homework_status(sample_data, tmp_path):
    db = tmp_path / "db.json"
    ok, _ = toggle_homework_status(sample_data, 1, filepath=str(db))
    assert ok is True
    assert sample_data["homework"][0]["status"] == "Выполнено"



def test_10_storage_broken_json(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{broken", encoding="utf-8")
    with pytest.raises(StorageError):
        load_data(str(bad))
