FROM python:3.9-alpine3.13 
LABEL mantainer="MisterPellino"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000


ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true"  ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \ 
    rm -rf /tmp && \    
    adduser \ 
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user


# Dockerfile Explanation:
# 
# This Dockerfile sets up a container with Python 3.9 and Alpine Linux 3.13.
#
# - `ENV PYTHONBUFFERED 1`: Ensures that Python output is not buffered, improving performance by printing directly to the terminal.
#
# - `COPY ./requirements.txt /tmp/requirements.txt`: Copies the local requirements.txt file to a temporary location (/tmp) inside the container.
#
# - `COPY ./app /app`: Copies the Django application code from the local directory into the /app directory of the container.
#
# - `WORKDIR /app`: Sets the working directory within the container to /app.
#
# - `EXPOSE 8000`: Exposes port 8000 on the container, allowing external communication to the Django application.
#
# - `RUN python -m venv /py`: Creates a Python virtual environment named 'py' in the root (/) directory of the container.
#   - `/py/bin/pip install --upgrade pip`: Upgrades pip within the virtual environment.
#   - `/py/bin/pip install -r /tmp/requirements.txt`: Installs Python dependencies from requirements.txt into the virtual environment.
#   - `rm -rf /tmp`: Removes the temporary directory (/tmp) to clean up unnecessary files.
#   - `adduser --disabled-password --no-create-home django-user`: Adds a non-root user named 'django-user' to run the Django application for security purposes.
#
# - `ENV PATH="/py/bin:$PATH"`: Adds the /py/bin directory to the PATH environment variable, ensuring Python and installed packages are executable.
#
# - `USER django-user`: Switches to the 'django-user' to run the container as a non-root user, enhancing security by minimizing privileges.

# End of Dockerfile