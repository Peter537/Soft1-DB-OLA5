# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Run the Streamlit app
CMD ["streamlit", "run", "./streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]