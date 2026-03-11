FROM python:3.12-slim

ENV PIP_NO_CACHE_DIR=1 \
    ANSIBLE_HOST_KEY_CHECKING=False \
    ANSIBLE_RETRY_FILES_ENABLED=False

WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    git \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.yml ./

RUN python -m pip install --upgrade pip \
    && python -m pip install ansible-core \
    && if [ -f requirements.txt ]; then python -m pip install -r requirements.txt; fi \
    && if [ -f requirements.yml ]; then ansible-galaxy collection install -r requirements.yml; fi

COPY . .

CMD ["bash"]
