FROM python:3.9

# Set the working directory
WORKDIR /app

# Install Python dependencies
RUN pip install flask flask-cors

# Copy application files
COPY app.py .

# Command to run the application
CMD ["python", "app.py"]
