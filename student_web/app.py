from flask import Flask, render_template, request, redirect, url_for, flash
from storage import load_data, StorageError
from cabinet import (
    get_schedule,
    add_grade,
    get_grades_by_subject,
    calculate_average_grade,
    delete_grade,
    add_homework,
    filter_homework,
    toggle_homework_status,
    delete_homework,
)

app = Flask(__name__)
app.secret_key = "student_cabinet_secret_key"


@app.route("/")
def index():
    try:
        data, sys_msg = load_data()
        if sys_msg:
            flash(sys_msg, "info")
    except StorageError as err:
        return f"<h1>Критическая ошибка хранилища</h1><p>{err}</p>", 500

    day_filter = request.args.get("day", "")
    subj_filter = request.args.get("subject", "")
    hw_filter = request.args.get("hw_status", "")

    schedule = get_schedule(data, day_filter)
    grades = get_grades_by_subject(data, subj_filter)
    avg_grade = calculate_average_grade(data, subj_filter)
    overall_avg = calculate_average_grade(data)
    homework = filter_homework(data, hw_filter)
    active_hw_count = len(filter_homework(data, "В работе"))

    return render_template(
        "index.html",
        schedule=schedule,
        grades=grades,
        avg_grade=avg_grade,
        overall_avg=overall_avg,
        homework=homework,
        active_hw_count=active_hw_count,
        day_filter=day_filter,
        subj_filter=subj_filter,
        hw_filter=hw_filter,
    )


@app.route("/grades/add", methods=["POST"])
def route_add_grade():
    data, _ = load_data()
    ok, msg = add_grade(
        data,
        request.form.get("subject"),
        request.form.get("score"),
        request.form.get("date"),
        request.form.get("work_type"),
    )
    flash(msg, "success" if ok else "error")
    return redirect(url_for("index"))


@app.route("/grades/delete/<int:grade_id>", methods=["POST"])
def route_delete_grade(grade_id):
    data, _ = load_data()
    ok, msg = delete_grade(data, grade_id)
    flash(msg, "success" if ok else "error")
    return redirect(url_for("index"))


@app.route("/homework/add", methods=["POST"])
def route_add_homework():
    data, _ = load_data()
    ok, msg = add_homework(
        data,
        request.form.get("subject"),
        request.form.get("task"),
        request.form.get("deadline"),
    )
    flash(msg, "success" if ok else "error")
    return redirect(url_for("index"))


@app.route("/homework/toggle/<int:hw_id>", methods=["POST"])
def route_toggle_homework(hw_id):
    data, _ = load_data()
    ok, msg = toggle_homework_status(data, hw_id)
    flash(msg, "success" if ok else "error")
    return redirect(url_for("index"))


@app.route("/homework/delete/<int:hw_id>", methods=["POST"])
def route_delete_homework(hw_id):
    data, _ = load_data()
    ok, msg = delete_homework(data, hw_id)
    flash(msg, "success" if ok else "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
