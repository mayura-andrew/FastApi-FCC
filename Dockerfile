# Use the official Python 3.9.7 image as the base image
FROM python:3.9.7

# Set the working directory inside the container to /usr/src/app
WORKDIR /usr/src/app

# Copy the requirements.txt file from your host machine to the container
COPY requirements.txt ./

# Install the Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the files from your host machine to the container's working directory
COPY . .

# Define the command to run when the container starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
