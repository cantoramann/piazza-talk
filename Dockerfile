# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Additionally, install the pre-release version of weaviate-client
RUN pip install --pre -U "weaviate-client==4.*"

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define environment variable (optional)
ENV NAME World

# Run app.py when the container launches
CMD ["streamlit", "run", "pkg/app.py"]
