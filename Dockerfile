FROM python:3.9.18

# Set the working directory to /opt/
WORKDIR /app

# Copy the requirements.txt and the entire questionpro_flask directory into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose port 8000 for Gunicorn
EXPOSE 8000

# Copy the content of the local src directory to the working directory
COPY . .

# Specify the command to run on container start
CMD [ "python", "run.py" ]

# Start Gunicorn to run the Flask app
# CMD ["gunicorn3", "-b", "0.0.0.0:8000", "questionpro_flask.app:app", "--workers=5"]
