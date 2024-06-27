# Use the official lightweight Python image.
FROM python:3.9-slim

# Set the working directory in the container.
WORKDIR /app

# Copy the current directory contents into the container at /app.
COPY . /app

# Install any needed packages specified in requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container.
EXPOSE $PORT

# Run Streamlit when the container launches.
CMD streamlit run app.py --server.port $PORT --server.address 0.0.0.0
