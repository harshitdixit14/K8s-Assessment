from flask import Flask, request, render_template_string
import os
import mysql.connector

app = Flask(__name__)

db_connection = mysql.connector.connect(
    host=os.getenv("DB_HOST", "mysql-service"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", "rootpassword"), 
    database=os.getenv("DB_NAME", "counter_db")
)

server_counter = 1
current_message = "Waiting for a message..."

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
    global current_message
    global server_counter
    payload = request.json
    if payload and "message" in payload and "counter" in payload:
        current_message = payload["message"]
        counter_value = payload["counter"]

        # Save to the database
        try:
            cursor = db_connection.cursor()
            query = "INSERT INTO counter_messages (counter, message) VALUES (%s, %s)"
            cursor.execute(query, (counter_value, current_message))
            db_connection.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return {"status": "failure", "message": "Database error."}, 500

        return {"status": "success", "message": "Your message has been saved."}, 200

    return {"status": "failure", "message": "Message or counter not found in the request."}, 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
