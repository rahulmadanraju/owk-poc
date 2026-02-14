# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the required directories
COPY data ./data
COPY owk_poc ./owk_poc

# Set PYTHONPATH to the working directory
ENV PYTHONPATH=/app

# Expose port 8501 for Streamlit
EXPOSE 8501

# Run app.py when the container launches
CMD ["streamlit", "run", "owk_poc/app.py", "--server.address=0.0.0.0"]
