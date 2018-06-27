LATEX ?= lualatex
PYTHON3 ?= python3
VIEWPDF ?= mupdf # tool for viewing pdf files

.PHONY: all clean view view-references

all: references.pdf resume.pdf resume.txt

clean:
	\rm -f references.pdf references.tex references.txt \
	       resume.pdf resume.tex resume.txt

view: resume.pdf
	$(VIEWPDF) resume.pdf

view-references: references.pdf
	$(VIEWPDF) references.pdf

references.pdf: references.tex common_preamble.tex
	$(LATEX) references.tex

references.tex: references.json generate.py
	$(PYTHON3) generate.py -ro references.tex

references.txt: references.json generate.py
	$(PYTHON3) generate.py -rpo references.txt

resume.pdf: resume.tex common_preamble.tex
	$(LATEX) resume.tex

resume.tex: resume.json generate.py
	$(PYTHON3) generate.py -o resume.tex

resume.txt: resume.json generate.py
	$(PYTHON3) generate.py -po resume.txt
