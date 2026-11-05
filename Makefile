PY = .venv/bin/python
export MPLBACKEND = Agg
export MPLCONFIGDIR = /tmp/atlas-matplotlib
export XDG_CACHE_HOME = /tmp/atlas-cache
.PHONY: setup reproduce test experiment pdf serve
setup:
	uv venv --python python3.12 .venv
	uv pip sync --python $(PY) --require-hashes requirements.lock
reproduce:
	$(PY) scripts/curate.py
	$(PY) scripts/validate.py
	$(PY) scripts/analyze.py
	$(PY) scripts/build_report.py
	$(PY) scripts/check_links.py
experiment:
	$(PY) scripts/run_experiment.py
test:
	$(PY) -m pytest -q
pdf:
	$(PY) scripts/build_report.py
serve:
	python3 -m http.server 8000 --directory site
