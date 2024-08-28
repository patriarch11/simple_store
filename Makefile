.SILENT:
.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*?##"; printf "Usage:\n  make \033[36m<target>\033[0m\n"; cmd=""; desc=""} \
	{if ($$0 ~ /^##/) { \
		if (desc != "") desc = desc" "; \
		desc = desc substr($$0, 3) \
	} \
	else if ($$0 ~ /^[a-zA-Z_][a-zA-Z0-9_-]*:/) { \
		if (desc != "") { \
		sub(/:.*/, "", $$1); \
		gsub(/^[ \t]+|[ \t]+$$/, "", desc); \
		printf "  \033[36m%-20s\033[0m %s\n", $$1, desc; \
	desc = ""; \
	} \
	}}' $(MAKEFILE_LIST)

PORT ?= 8000
HOST ?= 127.0.0.1

## Run server
run:
	. ./.env && uvicorn src.main:app --reload --port $(PORT) --host $(HOST)

## Create or update migrations
migrate:
	alembic revision --autogenerate -m "$(m)"

## Apply migrations to DB
migrate-up:
	alembic upgrade head
