FROM python:3.10-slim as python
ENV PYTHONUNBUFFERED=true
WORKDIR /app

FROM python as poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -
COPY pyproject.toml poetry.lock  ./
RUN poetry install --no-dev --no-interaction --no-ansi -vvv
COPY argstore ./argstore/

FROM python as runtime
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=poetry /app /app
EXPOSE 8000
CMD [ "bash", "-c", "uvicorn argstore.app:app --host 0.0.0.0 --port 8000" ]
