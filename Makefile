LATEX ?= lualatex
VIEWPDF ?= mupdf # tool for viewing pdf files

.PHONY: all clean view

all: resume.pdf

clean:
	\rm -f resume.pdf

view: resume.pdf
	$(VIEWPDF) $<

resume.pdf: heading.tex resume.tex resume_preamble.tex
	$(LATEX) resume.tex
