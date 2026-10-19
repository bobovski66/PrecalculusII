# MATH& 142 — Precalculus II

Original, student-centered course materials for a ten-week Precalculus II course.

## Course structure

Each module uses five components: **Reading, Demos, Weekly Lab, Applications, Weekly Quiz**. The readings are original LaTeX lecture notes, not assigned OpenStax chapters. OpenStax *Precalculus 2e* is a curricular reference.

## Notes

- `notes/preamble.tex` — shared typographic conventions and environments.
- `notes/master.tex` — compiles the complete course reader.
- `notes/week01.tex` ... `notes/week10.tex` — individual chapter source files.
- `notes/standalone.tex` — compiles the first chapter as a standalone weekly handout (change the input path for subsequent weeks).
- `pdfs/PrecalcII_Week01.pdf` — illustrated Module 1 reading with worked examples and solutions.

## Module 1

`readings/module01_reading.html` develops coordinates, signed rotation, radian measure, arc length, speed, exact values, reference angles, periodicity, and a Ferris-wheel model. The seven module pages share `assets/module1/module1.css` and `module1.js`. Eighteen diagrams have paired SVG and PDF versions for the web and print.

The original seven lab prompts, eleven application questions, ten quiz items, six chapter practice prompts, and thirteen review exercises are retained. Existing browser storage keys for the lab, quiz mastery, practice scores, and course dashboard remain compatible. Applications now support saved responses and printable/downloadable submissions. These files must still be uploaded to Canvas by the student.

Rebuild the Module 1 content and verify it from the repository root:

```sh
python scripts/build_module1_figures.py
python scripts/build_module1_pages.py
python scripts/build_module1_chapter.py
python scripts/verify_module1.py
node scripts/test_module1.js
python scripts/check_module1_pdf.py --out /tmp/precalc-module1-check --install
```

The generators require Python with Matplotlib, NumPy, and lxml; the PDF checker also uses PyMuPDF and Pillow. PDF compilation requires pdfLaTeX with the packages loaded in `notes/preamble.tex` and `notes/module1_setup.tex`. The runtime checks use Node.js and Python's standard library; no browser or network is required. The checker compiles until the table of contents stabilizes, verifies chapter page numbers, checks glyphs and text bounds, renders every page, and confirms that the remaining chapter sources are unchanged.

`scripts/module1_content.py` is the shared source for the web reading and printed chapter. `scripts/module1_original_contracts.json` records the original question text and storage keys. The question-contract check intentionally compares the other modules with the original base revision; update its baseline deliberately when beginning a later module overhaul.

## Build

From `notes/`, run `pdflatex -jobname=PrecalcII_Week01 standalone.tex` for the first chapter or `pdflatex master.tex` for the collected book. Repeat until references and the table of contents stabilize (the expanded collected reader may require three passes). Move individual PDFs into `pdfs/` before deployment, or use the checker above to install the two updated PDFs. GitHub Actions rebuilds the course PDFs when notes or Module 1 diagram PDFs change.

## Deployment

Publish GitHub Pages from the `main` branch root. Unpublished resources are marked *Coming soon* rather than linked to missing files. Browser-local completion tracking counts only published resources.
