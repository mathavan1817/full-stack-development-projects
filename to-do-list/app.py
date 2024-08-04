from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
import pymysql.cursors

app = Flask(__name__)
app.secret_key = '1234'

@app.route("/")
def index():
    data = retrieve_all_information_from_database()
    return render_template('result.html', tasks=data)

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        tname = request.form.get('task-name')
        due = request.form.get('due-date')
        assign = request.form.get('assign')
        status = request.form.get('status')

        try:
            store(tname, due, assign, status)
            flash('Task registered successfully!')
        except Exception as e:
            flash(f'An error occurred: {str(e)}')

    data = retrieve_all_information_from_database()
    return render_template('result.html', tasks=data)

@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        tname = request.form.get('task-name')
        due = request.form.get('due-date')
        assign = request.form.get('assign')
        status = request.form.get('status')

        try:
            update_task(id, tname, due, assign, status)
            flash('Task updated successfully!')
        except Exception as e:
            flash(f'An error occurred: {str(e)}')

        return redirect(url_for('index'))

    task = retrieve_task_by_id(id)
    return render_template('edit.html', task=task)

@app.route("/delete/<int:id>")
def delete(id):
    try:
        delete_task(id)
        flash('Task deleted successfully!')
    except Exception as e:
        flash(f'An error occurred: {str(e)}')

    return redirect(url_for('index'))

def store(tname, due, assign, status):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='task_management',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO tasks (tname, due, assign, status) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (tname, due, assign, status))
        connection.commit()
    finally:
        connection.close()

def update_task(id, tname, due, assign, status):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='task_management',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE tasks SET tname=%s, due=%s, assign=%s, status=%s WHERE id=%s"
            cursor.execute(sql, (tname, due, assign, status, id))
        connection.commit()
    finally:
        connection.close()

def delete_task(id):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='task_management',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM tasks WHERE id=%s"
            cursor.execute(sql, (id,))
        connection.commit()
    finally:
        connection.close()

def retrieve_all_information_from_database():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='task_management',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM tasks"
            cursor.execute(sql)
            return cursor.fetchall()
    finally:
        connection.close()

def retrieve_task_by_id(id):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='task_management',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM tasks WHERE id=%s"
            cursor.execute(sql, (id,))
            return cursor.fetchone()
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
