FROM python:3.12-slim as builder

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY . .

FROM python:3.12-slim

WORKDIR /habit-tracker

COPY --from=builder /root/.cache/pypoetry/virtualenvs /root/.cache/pypoetry/virtualenvs
COPY --from=builder /app /app

ENV PATH="/root/.cache/pypoetry/virtualenvs/app/bin:$PATH"

EXPOSE 8000

CMD EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]