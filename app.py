from flask import Flask, request, render_template_string
import os
import mysql
app = Flask(__name__)
server_counter = 1
current_message = "Waiting for a message..."

db_config = {
    "host": "mysql-service", 
    "user": "root",
    "password": "rootpassword",
    "database": "counter_db"
}

def insert_to_db(message, counter):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message TEXT NOT NULL,
                counter INT NOT NULL
            )
        """)
        sql_query = "INSERT INTO messages (message, counter) VALUES (%s, %s)"
        cursor.execute(sql_query, (message, counter))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return False

@app.route("/", methods=["GET"])
def display_message():
    pod_name = os.getenv('HOSTNAME', 'Unknown Pod')
    page_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Message Board</title>
    </head>
    <body>
        <h1>Pod Info and Received Message</h1>
        <h2>Pod Name: {{ pod_name }}</h2>
        <h3>Server Counter: {{ counter }}</h3>
        <p><strong>Message:</strong> {{ message }}</p>
    </body>
    </html>
    """
    return render_template_string(
        page_content, 
        pod_name=pod_name, 
        message=current_message, 
        counter=server_counter
    )

@app.route("/submit", methods=["POST"])
def handle_message():
    global current_message, server_counter
    payload = request.json
    if payload and "message" in payload and "counter" in payload:
        current_message = payload["message"]
        server_counter = payload["counter"]
        if insert_to_db(current_message, server_counter):
            return {"status": "success", "message": "Data saved successfully."}, 200
        else:
            return {"status": "error", "message": "Failed to save data to the database."}, 500
    return {"status": "failure", "message": "Invalid request payload."}, 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
