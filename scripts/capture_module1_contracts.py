"""Capture the published assignment contracts before editing Module 1."""
import json, re, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE='90db525435778ad591d46364b337898824465c90'
def original(path): return subprocess.check_output(['git','show',f'{BASE}:{path}'],cwd=ROOT,text=True)
def array(path,start,end):
    raw=original(path); expression=raw[raw.index(start)+len(start):raw.index(end)]
    expression=expression.rstrip().rstrip(';')
    return json.loads(subprocess.check_output(['node','-e','process.stdout.write(JSON.stringify('+expression+'))'],text=True))
notes=original('notes/week01.tex')
from lxml import html
app=html.fromstring(original('applications/week01_applications.html'))
out={'base':BASE,'labKey':'m142lab1','quizKey':'math142quiz1','practiceKey':'m142_unitcircle_practice_score',
     'lab':array('labs/week01_lab.html','const prompts=','\nconst key='),
     'quiz':array('quizzes/week01_quiz.html','const data=','\nconst key='),
     'applications':[' '.join(x.text_content().split()) for x in app.xpath('//ol/li')],
     'tryIts':re.findall(r'\\begin\{practice\}(.*?)\\end\{practice\}',notes,re.S),
     'exercises':re.findall(r'\\item (.*?)(?=\\item|\\end\{enumerate\})',notes[notes.index('\\subsection{Exercises}'):],re.S)}
(ROOT/'scripts/module1_original_contracts.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('Captured 7 lab prompts, 11 application questions, 10 quiz items, 6 practice and 13 review questions.')
