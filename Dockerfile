FROM python:3.12 as builder

WORKDIR /app

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /root/.cache/pypoetry/virtualenvs /root/.cache/pypoetry/virtualenvs
COPY --from=builder /app /app

ENV PATH="/root/.cache/pypoetry/virtualenvs/app/bin:$PATH"

EXPOSE 8000

CMD EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]