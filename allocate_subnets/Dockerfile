FROM python:3.10-slim

WORKDIR /app

# Install additional development tools
RUN apt-get update && apt-get install -y \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

COPY . .

#ENTRYPOINT ["/bin/bash"]
CMD ["python", "main.py"]
