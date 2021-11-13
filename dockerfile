FROM python:3.6
# Set application working directory
WORKDIR /purbee_backend
# Install requirements
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
# Install application
# Run application
CMD python /backend_source/app.py