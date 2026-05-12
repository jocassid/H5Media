
DOT_FILES = $(wildcard docs/*.dot)
SVG_FILES = $(DOT_FILES:.dot=.svg)

.PHONY: docs

docs: $(SVG_FILES)

docs/%.svg: docs/%.dot
	dot -Tsvg $< -o $@
