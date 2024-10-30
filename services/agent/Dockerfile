FROM python:3.11.10

# Configure Poetry
ENV POETRY_VERSION=1.8.4


RUN apt update -y 
RUN pip3 install poetry==${POETRY_VERSION} 
RUN poetry --version

COPY ./app app/

# Install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry env use system
RUN poetry install

CMD ["poetry", "run", "fastapi", "run", "app/main.py"]