FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only the requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies once during the build process
RUN pip install --no-cache-dir -r requirements.txt


# Keep the container alive
CMD ["tail", "-f", "/dev/null"]