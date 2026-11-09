# MATH& 142 — Precalculus II

A ten-module course connecting trigonometry, vectors, polar and complex coordinates, curves, sequences, and motion.

## Course materials

Every module includes a reading, interactive explorers, a guided lab, applications, and a practice quiz. All ten modules have illustrated web readings as well as PDFs. The course home links all resources and the complete reader.

All ten labs use the shared workspace in `assets/guided-lab.js` and `assets/learning.css`. Each of seven problems has two response fields, a hint, and an explanation available after an attempt. Numerical checks supplement written reasoning. Prepare Submission shows the current answers in the same tab, with Print / Save PDF, Download HTML, and Return to Lab controls. Submission files are uploaded to Canvas by the student.

Existing lab storage keys are preserved. Earlier whole-question responses appear in a separate saved-response area and are included in submissions alongside the new part-by-part work. Quiz questions retain their original indices; two transfer questions were appended to each of Modules 2–10. The Module 2–4 application pages also provide guided response fields and submission controls.

## Editable sources

- `content/module02.md` through `content/module10.md`: shared web and print chapter content.
- `scripts/lab_content.py`: all guided lab prompts, hints, checks, and solutions.
- `scripts/build_learning_figures.py`: 24 mathematically scaled SVG/PDF figure pairs for Modules 5–10.
- `scripts/build_trig_foundations_figures.py`: 15 additional SVG/PDF pairs for Modules 2–4.
- `scripts/build_foundation_demos.py`: coordinate-ratio, wave-transformation, and principal-angle explorers.
- `scripts/application_content.py`: guided applications for Modules 2–4.
- `scripts/extend_course_practice.py`: additional questions for the later quizzes.
- `scripts/module1_content.py`: the Module 1 reading source.
- `notes/week02.tex` through `notes/week10.tex`: generated print chapters from the shared Markdown readings.
- `notes/master.tex`: collected course reader.

## Rebuild and verify

From the repository root:

```sh
python scripts/build_learning_figures.py
python scripts/build_trig_foundations_figures.py
python scripts/build_course_learning.py
python scripts/build_foundation_demos.py
python scripts/extend_course_practice.py
python scripts/verify_course_learning.py
```

The figure generator needs Matplotlib and NumPy. Reading generation needs Pandoc. The verification script uses Python's standard library and Node.js to check local links, lab structure, JavaScript syntax, and independent mathematical calculations. It also runs in the PDF publishing workflow.

Compile individual readings with `latexmk -pdf module05.tex` (or the desired module) from `notes/`. Compile `master.tex` for the complete reader, and `standalone.tex` for Module 1. PDF generation needs the packages listed in the shared preambles. Publish the resulting files under the established names in `pdfs/`.

The original Module 1 generators remain available. Rebuilding its pages retains the newer shared labs. Its earlier contract snapshots and one-module validation scripts document the October revision; use `verify_course_learning.py` for the current course, whose later chapters and labs intentionally extend those snapshots.

## Publication

GitHub Pages serves the root of `main`. The Actions workflow validates the course and recompiles the weekly PDFs, combined reader, and examinations when notes or figure PDFs change. Browser-local dashboard progress tracks the same five resources per module.
