# Use the official Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Flask app code
COPY app.py /app/

# Install required Python packages
RUN pip install --upgrade pip

RUN pip install flask
RUN pip install flask mysql-connector-python


# Expose the application's port
EXPOSE 5000

# Define the default command to run the app
CMD ["python", "app.py"]
