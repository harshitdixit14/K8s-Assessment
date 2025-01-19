from flask import Flask, request, render_template_string
import os

app = Flask(__name__)
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
    payload = request.json
    if payload and "message" in payload:
        current_message = payload["message"]
        return {"status": "success", "message": "Your message has been saved."}, 200
    return {"status": "failure", "message": "Message not found in the request."}, 400
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
