# Use an official Python runtime as a parent image
FROM python:3.10


# Copy the requirements file first to leverage Docker cache
COPY .  /app/

# Set the working directory in the container
WORKDIR /app


# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt


# Ensure start_app.sh is executable
#RUN chmod +x /app/start_app.sh

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Set the start_app.sh script as the entry point
#ENTRYPOINT ["/app/start_app.sh"]

CMD ["uvicorn", "app:app_test", "--host", "0.0.0.0", "--port", "8000"]