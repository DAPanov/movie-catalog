# FastAPI Movie catalog

[![Python checks 🐍](https://github.com/DAPanov/movie-catalog/actions/workflows/python-checks.yaml/badge.svg)](https://github.com/DAPanov/movie-catalog/actions/workflows/python-checks.yaml)

## Develop

Check GitHub Actions after any push.

### Setup:

 - Mark movie-catalog folder as source root

### Install dependencies

Install all packages:
```shell
uv sync
```

### Configure pre-commit

Install pre-commit hook:
```shell
pre-commit install
```

### Run

Go to workdir:
```shell
cd movie-catalog

```

Run dev server:
```shell
fastapi dev
```

## Snippets
```shell
python -c 'import secrets;print(secrets.token_urlsafe(16))'
```
