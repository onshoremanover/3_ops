# Use the official Python image
FROM python:3.12-slim

# Set environment variables to prevent Python from buffering logs
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /app

# Copy requirements to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY interactive_route_map.py .

# Expose the port Streamlit will run on
EXPOSE 8501

# Set the Streamlit command as the entry point
ENTRYPOINT ["streamlit", "run"]

# Pass the script to Streamlit
CMD ["interactive_route_map.py"]

