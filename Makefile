# ==========================================================================
# Prajñāpāramitāhṛdaya (Heart Sūtra) — Critical Edition
# ==========================================================================
#
# Targets:
#   make all              Build all editions (collation + PDFs)
#   make collation        Run collation and synoptic alignment (JSON output)
#   make editions         Build all PDF editions
#   make tibetan          Build Tibetan critical edition PDF
#   make sanskrit         Build Sanskrit critical edition PDF
#   make chinese          Build Chinese critical edition PDF
#   make parallel         Build parallel/synoptic edition PDF
#   make combined         Build combined critical edition PDF
#   make stemma           Build stemma diagram PDF
#   make validate         Run data validation
#   make test             Run test suite
#   make clean            Remove generated files
# ==========================================================================

PYTHON     = PYTHONPATH=src python3
XELATEX    = xelatex -interaction=nonstopmode
LATEXDIR   = output/latex
DATADIR    = data
COLLATION  = data/collation/variant_table.json

# ---------- Top-level targets ----------

.PHONY: all collation editions validate test clean \
        tibetan sanskrit chinese parallel combined stemma \
        tei check-stale

all: collation tei editions

# ---------- Data processing ----------

collation: $(COLLATION)

$(COLLATION): $(shell find $(DATADIR) -name '*.json' 2>/dev/null)
	$(PYTHON) -m hrdaya.collate > $@

synoptic:
	$(PYTHON) -m hrdaya.synoptic json > output/synoptic.json

tei: output/tei/heart_sutra_edition.xml

output/tei/heart_sutra_edition.xml: $(shell find $(DATADIR) -name '*.json' 2>/dev/null)
	$(PYTHON) -c "from pathlib import Path; from hrdaya.tei_export import export_tei; export_tei(output_path=Path('output/tei/heart_sutra_edition.xml'), data_dir=Path('data'))"

validate:
	$(PYTHON) -m hrdaya.validate

check-stale:
	$(PYTHON) scripts/check_latex_staleness.py

test:
	PYTHONPATH=src python3 -m pytest tests/

# ---------- PDF editions ----------

editions: tibetan sanskrit chinese parallel combined stemma

tibetan: $(LATEXDIR)/tibetan_critical.pdf

sanskrit: $(LATEXDIR)/sanskrit_critical.pdf

chinese: $(LATEXDIR)/chinese_critical.pdf

parallel: $(LATEXDIR)/parallel_complete.pdf

combined: $(LATEXDIR)/heart_sutra_critical.pdf

stemma: $(LATEXDIR)/stemma_diagram.pdf

# ---------- LaTeX compilation rules ----------

$(LATEXDIR)/%.pdf: $(LATEXDIR)/%.tex
	cd $(LATEXDIR) && $(XELATEX) $*.tex
	cd $(LATEXDIR) && $(XELATEX) $*.tex
	@echo "Built: $@"

# ---------- Clean ----------

clean:
	cd $(LATEXDIR) && rm -f *.aux *.log *.out *.pdf
	rm -f output/synoptic.json
