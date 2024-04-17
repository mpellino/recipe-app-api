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
    # install the postgresql client package we need inside the alpine image in order tfor psycorp to be able to connect
    apk add --update --no-cache postgresql-client && \ 
    # the virtual option sets a virtual dependency packages in this folder name and we can use to remove the packages later on
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    # we remove the packages that we installed before. keeps the docker file lightwiegh and clean
    apk del .tmp-build-deps && \
    adduser \ 
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user


# Dockerfile Explanation:

# This Dockerfile sets up a container with Python 3.9 and Alpine Linux 3.13.
# FROM python:3.9-alpine3.13 

# The LABEL instruction adds metadata to an image. A LABEL is a key-value pair.
# LABEL mantainer="MisterPellino"

# The ENV instruction sets the environment variable PYTHONUNBUFFERED to 1. 
# This ensures that Python output is sent straight to terminal without being first buffered, 
# which is useful for logging purposes.
# ENV PYTHONUNBUFFERED 1

# The COPY instruction copies new files from source and adds them to the filesystem of the container at the path.
# Here, it copies the requirements.txt and requirements.dev.txt files to a temporary location (/tmp) inside the container.
# COPY ./requirements.txt /tmp/requirements.txt
# COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# The COPY instruction is also used to copy the Django application code from the local directory into the /app directory of the container.
# COPY ./app /app

# The WORKDIR instruction sets the working directory for any RUN, CMD, ENTRYPOINT, COPY and ADD instructions that follow in the Dockerfile.
# Here, it sets the working directory within the container to /app.
# WORKDIR /app

# The EXPOSE instruction informs Docker that the container listens on the specified network ports at runtime.
# Here, it exposes port 8000 on the container, allowing external communication to the Django application.
# EXPOSE 8000

# The ARG instruction defines a variable that users can pass at build-time to the builder with the docker build command.
# Here, it sets a build argument DEV to false.
# ARG DEV=false

# The RUN instruction will execute any commands in a new layer on top of the current image and commit the results.
# Here, it creates a Python virtual environment named 'py' in the root (/) directory of the container.
# It then upgrades pip within the virtual environment.
# It installs the PostgreSQL client package needed for psycopg to connect.
# It sets a virtual dependency packages in this folder name and we can use to remove the packages later on.
# It installs Python dependencies from requirements.txt into the virtual environment.
# If DEV is set to true, it installs the dev dependencies from requirements.dev.txt.
# It removes the temporary directory (/tmp) to clean up unnecessary files.
# It removes the packages that were installed before to keep the Docker image lightweight and clean.
# It adds a non-root user named 'django-user' to run the Django application for security purposes.
# RUN python -m venv /py && \
#     /py/bin/pip install --upgrade pip && \
#     apk add --update --no-cache postgresql-client && \ 
#     apk add --update --no-cache --virtual .tmp-built-dept \
#         build-base postgresql-dev musl-dev && \
#     /py/bin/pip install -r /tmp/requirements.txt && \
#     if [ $DEV = "true" ]; \
#         then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
#     fi && \
#     rm -rf /tmp && \
#     apk del .tmp-build-deps && \
#     adduser --disabled-password --no-create-home django-user

# The ENV instruction sets the environment variable PATH to include /py/bin.
# This ensures Python and installed packages executable.
# ENV PATH="/py/bin:$PATH"

# The USER instruction sets the user name (or UID) and optionally the user group (or GID) to use when running the image and for any RUN, CMD and ENTRYPOINT instructions that follow it in the Dockerfile.
# Here, it switches to the 'django-user' to run the container as a non-root user, enhancing security by minimizing privileges.
# USER django-user

# End of Dockerfile