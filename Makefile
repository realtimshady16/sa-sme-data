PY ?= uv run --with pandas --with openpyxl --with numpy python

.PHONY: help brief numbers crosstabs series qlfs treasury ene check

help:
	@echo "make numbers    - informal sector counts, turnover, employment (SESE 2023)"
	@echo "make crosstabs  - who employs people, by age / motive / turnover"
	@echo "make series     - the 2009-2023 informal-sector series"
	@echo "make qlfs       - QLFS employer counts (2026 Q3)"
	@echo "make treasury   - company register, size distribution, VAT survival cohort"
	@echo "make ene        - programme-level spending from the vulekamali pivot"
	@echo "make check      - every script at least parses"

numbers:
	$(PY) scripts/sese_microdata.py

crosstabs:
	$(PY) scripts/sese_crosstabs.py

series:
	$(PY) scripts/sese_series.py

qlfs:
	$(PY) scripts/qlfs_employers.py

treasury:
	$(PY) scripts/treasury_numbers.py

ene:
	$(PY) scripts/ene_pivot.py

check:
	@for f in scripts/*.py; do python3 -c "import ast,sys; ast.parse(open('$$f').read())" && echo "ok $$f"; done
