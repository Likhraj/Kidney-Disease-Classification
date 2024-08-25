# Use the official Python image from the Docker Hub
FROM python:3.10.12

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install localtunnel globally using npm
RUN apt-get update && apt-get install -y nodejs npm
RUN npm install -g localtunnel

# Expose the port that Streamlit runs on
EXPOSE 8501

# Run the command to start Streamlit and localtunnel
CMD wget -q -O - ipv4.icanhazip.com && streamlit run app.py & npx localtunnel --port 8501
