PDF := TVKTDGH-KHMT.pdf

.PHONY: pdf clean
pdf:            ## Build the PDF locally
	typst compile --root . typst/paper.typ $(PDF)

clean:          ## Remove built PDF
	rm -f $(PDF)
