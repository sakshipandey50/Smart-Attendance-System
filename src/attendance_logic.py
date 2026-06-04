from datetime import datetime
from db_connection import connect_db


def mark_attendance(name):
    conn = connect_db()
    cursor = conn.cursor()

    today = datetime.now().date()
    current_time = datetime.now().strftime("%H:%M:%S")

    # Check duplicate
    cursor.execute("SELECT * FROM attendance WHERE name=%s AND date=%s", (name, today))
    result = cursor.fetchone()

    if result:
        print(f"{name} already marked today.")
        conn.close()
        return False

    # Insert attendance
    cursor.execute(
        "INSERT INTO attendance (name, date, time) VALUES (%s, %s, %s)",
        (name, today, current_time),
    )
    conn.commit()
    conn.close()

    print(f"{name} attendance marked successfully.")
    return True
