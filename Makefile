LATEX ?= lualatex
PYTHON3 ?= python3
VIEWPDF ?= mupdf # tool for viewing pdf files

.PHONY: all clean view

all: resume.pdf resume.txt

clean:
	\rm -f resume.pdf resume.tex resume.txt

view: resume.pdf
	$(VIEWPDF) resume.pdf

resume.pdf: resume.tex resume_preamble.tex
	$(LATEX) resume.tex

resume.tex: resume.json generate.py
	$(PYTHON3) generate.py -o resume.tex

resume.txt: resume.json generate.py
	$(PYTHON3) generate.py -po resume.txt
