# TRE Makefile
# v0.1.0

# external tools
VIRTUALENV=virtualenv

# opts
PIP_INSTALL_OPTS=-q --allow-external gnuplot-py --allow-unverified gnuplot-py

# files/dirs
SRC=src
VENV=venv
TESTS=tests
LIBS_FILE=requirements.txt

PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
COVERAGE=$(VENV)/coverage

COVERAGE_EXCLUDE=$(TESTS)/**,**/__init__.py,venv/**,$(SRC)/tre/vendor/**

.DEFAULT: tests
.PHONY: deps tests coverage

tests: deps
	$(PYTHON) $(TESTS)/test.py

coverage: deps
	$(COVERAGE) run --omit='$(COVERAGE_EXCLUDE)' $(TESTS)/test.py
	$(COVERAGE) report -m

$(VENV):
	$(VIRTUALENV) $@

deps: $(VENV)
	$(PIP) install $(PIP_INSTALL_OPTS) -r $(LIBS_FILE)
	$(PIP) install $(PIP_INSTALL_OPTS) 'gnuplot-py==1.8'

clean:
	find . -name '*~' -delete
	for ext in toc aux log out blg;do \
		find . -name "*.$$ext" -delete; done

rapport.pdf: report/rapport.tex
	pdflatex report/rapport.tex
	pdflatex report/rapport.tex
