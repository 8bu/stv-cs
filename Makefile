PDF := TVKTDGH-KHMT.pdf
PYTHON ?= python3

.PHONY: pdf sync check test clean
pdf:            ## Build the PDF locally
	typst compile --root . typst/paper.typ $(PDF)

sync:           ## Regenerate the glossary block in the spec from glossary/glossary.csv
	$(PYTHON) tools/validate.py sync

check:          ## Validate glossary, generated block freshness and QT references
	$(PYTHON) tools/validate.py check

test:           ## Run validator unit tests
	$(PYTHON) -m unittest discover -s tests -v

clean:          ## Remove built PDF
	rm -f $(PDF)
