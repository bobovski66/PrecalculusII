# MATH& 142 — Precalculus II

Original, student-centered course materials for a ten-week Precalculus II course.

## Course structure

Each module uses five components: **Reading, Demos, Weekly Lab, Applications, Weekly Quiz**. The readings are original LaTeX lecture notes, not assigned OpenStax chapters. OpenStax *Precalculus 2e* is a curricular reference.

## Notes

- `notes/preamble.tex` — shared typographic conventions and environments.
- `notes/master.tex` — compiles the complete course reader.
- `notes/week01.tex` ... `notes/week10.tex` — individual chapter source files.
- `notes/standalone.tex` — compiles the first chapter as a standalone weekly handout (change the input path for subsequent weeks).
- `pdfs/PrecalcII_Week01.pdf` — initial compiled handout.

## Build

From `notes/`, run `pdflatex -jobname=PrecalcII_Week01 standalone.tex` twice for the first chapter or `pdflatex master.tex` twice for the collected book. Move individual PDFs into `pdfs/` before deployment.

## Deployment

Publish GitHub Pages from the `main` branch root. Unpublished resources are marked *Coming soon* rather than linked to missing files. Browser-local completion tracking counts only published resources.