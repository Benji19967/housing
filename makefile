include ../build_tools/poetry.mk

PORT ?= 8989

run:
	env/bin/python housing/main.py

start:
# env/bin/uvicorn main:app --app-dir housing --reload --host 0.0.0.0 --port ${PORT}
	env/bin/hypercorn housing.main:app --reload --bind 0.0.0.0:${PORT}

health_check:
	curl 0.0.0.0:${PORT}/v1/health_check
