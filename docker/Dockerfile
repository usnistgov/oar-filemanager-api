# Start from the official Python base image.
FROM python:3.9-slim

# Set the current working directory to /code.
WORKDIR /dev/filemanager

# copy content to /code directory
COPY ./ ./

# Install the package dependencies in the requirements file.
# The --no-cache-dir option tells pip to not save the downloaded packages locally.
RUN ls /dev/filemanager
RUN pip install --no-cache-dir --upgrade -r /dev/filemanager/python/requirements.txt


RUN chmod +x /code/scripts/run.sh

# Run the run.sh script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Uvicorn
ENTRYPOINT ["/dev/filemanager/run.sh"]