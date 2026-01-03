FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY .python-version ./
COPY src ./

CMD ["uv", "run", "--", "fastapi", "run", "main.py"]
