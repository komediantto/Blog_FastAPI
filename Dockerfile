FROM python:3

WORKDIR /blog

COPY poetry.lock pyproject.toml /blog/

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

ENV PYTHONPATH=/BotForwarding:${PYTHONPATH}

COPY . /blog/

RUN chmod +x run.sh

ENTRYPOINT [ "./run.sh" ]