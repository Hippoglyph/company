FROM ubuntu:latest

# Update package lists and install Python 3 and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3 as the default python version
RUN ln -s /usr/bin/python3 /usr/bin/python

# Verify installations
RUN python --version && pip3 --version

# Set the working directory in the container
WORKDIR /app

# Command to run when the container starts
CMD ["bash"]