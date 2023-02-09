# Official Python 3.11.1 image
FROM python:3.11.1

# Set WORKDIR
WORKDIR /code

# Install curl
RUN apt-get update && apt-get install -y curl

RUN apt-get install -y ffmpeg

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3
ENV PATH="${PATH}:/root/.local/bin"

# copy poetry.lock pyproject.toml files
COPY ./poetry.lock ./pyproject.toml ./

# installing dependencies
RUN poetry install

# copy project
COPY ./app /code/app

RUN chmod 777 /code/app

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]