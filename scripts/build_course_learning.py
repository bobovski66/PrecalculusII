"""Generate readings and guided labs from reviewed source content."""
from pathlib import Path
import html
import json
import re
import subprocess
from lab_content import LABS

ROOT=Path(__file__).resolve().parents[1]
TITLES={
1:"Angles, Radians, and the Unit Circle",2:"The Six Trigonometric Functions",
3:"Periodic Functions and Their Graphs",4:"Inverse Trigonometry and Identities",
5:"Trigonometric Equations and Applications",6:"Vectors and Geometric Applications",
7:"Polar Coordinates and Complex Numbers",8:"Parametric Equations and Conic Sections",
9:"Sequences and Series",10:"Synthesis: Motion and Patterns"}
DEMOS={1:"unit_circle",2:"six_trig_functions",3:"sinusoid_explorer",4:"inverse_trig",
5:"trig_equations",6:"vector_explorer",7:"polar_complex",8:"conic_explorer",
9:"sequence_explorer",10:"motion_synthesis"}

def reading_path(n):
    return f"../readings/module{n:02}_reading.html" if n==1 or n>=5 else f"../pdfs/PrecalcII_Week{n:02}.pdf"

def head(title, script=""):
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{html.escape(title)} | MATH&amp; 142</title>'
        '<link rel="stylesheet" href="../assets/learning.css">'
        r"""<script>window.MathJax={tex:{inlineMath:[['\\(','\\)']],displayMath:[['\\[','\\]']]},svg:{fontCache:'none'},options:{skipHtmlTags:['script','noscript','style','textarea','pre','code']}};</script>"""
        '<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>'
        +script+'</head><body><a class="skip" href="#main">Skip to content</a>')

def masthead(n,title):
    return (f'<header class="masthead"><a href="../index.html">← Precalculus II</a>'
        f'<p class="eyebrow">MATH&amp; 142 · Module {n} · Dr. Lee</p><h1>{html.escape(title)}</h1>'
        f'<nav class="module-nav" aria-label="Module {n} resources">'
        f'<a href="{reading_path(n)}">Reading</a>'
        f'<a href="../pdfs/PrecalcII_Week{n:02}.pdf">Reading PDF</a>'
        f'<a href="../demos/{DEMOS[n]}.html">Explorer</a>'
        f'<a href="../labs/week{n:02}_lab.html">Guided lab</a>'
        f'<a href="../applications/week{n:02}_applications.html">Applications</a>'
        f'<a href="../quizzes/week{n:02}_quiz.html">Practice quiz</a></nav></header>')

def footer():
    return ('<footer>MATH&amp; 142 · Centralia College · Dr. Lee<br>'
        '<a href="../index.html">Course home</a> · '
        '<a href="../pdfs/PrecalculusII_Complete_Reader.pdf">Complete course reader</a></footer></body></html>')

def pandoc(source, to):
    return subprocess.run(["pandoc","--from","markdown+tex_math_single_backslash+fenced_divs",
        "--to",to,"--wrap=none"]+(["--mathjax"] if to=="html5" else []),input=source,text=True,capture_output=True,check=True).stdout

def readings():
    for n in range(5,11):
        source=(ROOT/f"content/module{n:02}.md").read_text()
        body=pandoc(source,"html5")
        headings=re.findall(r'<h2 id="([^"]+)">(.+?)</h2>',body)
        nav='<nav aria-label="Reading sections">'+''.join(f'<a href="#{i}">{t}</a>' for i,t in headings)+'</nav>'
        page=head(TITLES[n])+masthead(n,TITLES[n])+f'<div class="layout"><aside class="rail"><h2>In this reading</h2>{nav}</aside><main id="main">'+body+'</main></div>'+footer()
        (ROOT/f"readings/module{n:02}_reading.html").write_text(page)
        texsource=source.replace(".svg)",".pdf)")
        texsource=re.sub(r'\]\(\.\./demos/([^)]*)\)',r'](https://bobovski66.github.io/PrecalculusII/demos/\1)',texsource)
        tex=pandoc(texsource,"latex")
        tex=tex.replace(r"\includegraphics{",r"\includegraphics[width=\linewidth,height=.42\textheight,keepaspectratio]{")
        tex=tex.replace(r"\begin{figure}",r"\begin{figure}[htbp]")
        tex=re.sub(r'\\(hypertarget|label)\{([^}]+)\}',lambda m: "\\"+m[1]+"{m"+str(n)+"-"+m[2]+"}",tex)
        tex=tex.replace(r"\hypertarget{m"+str(n)+"-review-exercises}",r"\Needspace{20\baselineskip}"+"\n"+r"\hypertarget{m"+str(n)+"-review-exercises}")
        (ROOT/f"notes/week{n:02}.tex").write_text(
            f"% Generated from content/module{n:02}.md by scripts/build_course_learning.py\n"+
            r"\section{"+TITLES[n]+"}\n"+tex+"\n\\clearpage\n")

def labs():
    for n,data in LABS.items():
        title="Lab: "+data["title"]
        page=head(title,'<script defer src="../assets/guided-lab.js"></script>')+masthead(n,title)
        page+='<div class="layout"><aside class="rail"><h2>Your work</h2><div class="actions">'
        page+='<button id="prepare-submission">Prepare Submission</button><button class="secondary" id="next-problem">Next problem</button><button class="secondary" id="clear-work">Clear answers</button></div>'
        page+='<progress id="progress" value="0" max="100" aria-label="Lab progress"></progress><p id="progress-label" class="small" aria-live="polite"></p><nav aria-label="Lab problems">'
        page+=''.join(f'<a href="#problem-{i+1}">{i+1}. {p["title"]}</a>' for i,p in enumerate(data["problems"]))+'</nav></aside>'
        page+='<main id="main"><div id="lab-workspace"><section class="panel"><p class="intro">'+data["intro"]+'</p>'
        page+='<p>Work through the parts in order. Type calculations and reasoning in each answer space; fractions and ordinary math notation are welcome. Hints can help you begin. After you try a problem, open its solution to compare.</p>'
        page+='<p>Enter your name, then choose <strong>Prepare Submission</strong> when you are ready to turn it in. The submission view lets you print a PDF, download your completed HTML, or return to your answers.</p>'
        page+='<div class="identity"><label for="student">Student name<input id="student" type="text" autocomplete="name"></label><label for="date">Date<input id="date" type="date"></label></div><p class="small" id="save-status" role="status">Answers save in this browser as you type.</p></section>'
        for i,p in enumerate(data["problems"]):
            page+=f'<section class="panel problem" id="problem-{i+1}"><h2>{i+1}. {p["title"]}</h2><div class="problem-context"><p>{p["context"]}</p></div>'
            page+='<details class="hint"><summary>A hint to get started</summary><p>'+p["hint"]+'</p></details>'
            for j,prompt in enumerate(p["parts"]):
                field=f'{data["prefix"]}{i}_part{j+1}'
                page+=f'<div class="part"><label for="{field}">({chr(97+j)}) {prompt}</label><textarea data-response id="{field}" rows="4" aria-label="Problem {i+1}, part {chr(97+j)}: your work"></textarea>'
                if j in p["checks"]:
                    label,answer,tol=p["checks"][j];checkfield=field+"_check"
                    page+=f'<div class="check-row"><label for="{checkfield}">{html.escape(label)}</label><input id="{checkfield}" type="text" inputmode="decimal" data-answer="{answer:.14g}" data-tolerance="{tol}" aria-describedby="{checkfield}-feedback"><button type="button" data-check="{checkfield}">Check value</button><span class="feedback" id="{checkfield}-feedback" role="status"></span></div>'
                page+='</div>'
            page+='<details class="solution locked"><summary>Compare your solution after an attempt</summary><div class="solution-body">'+p["solution"]+'</div><p class="attempt-message small" role="status"></p></details></section>'
        page+='</div></main></div>'
        payload=dict(module=n,title=title,key=data["key"],prefix=data["prefix"],problems=[dict(title=p["title"]) for p in data["problems"]])
        page+='<script type="application/json" id="lab-data">'+json.dumps(payload).replace("</","<\\/")+'</script>'+footer()
        (ROOT/f"labs/week{n:02}_lab.html").write_text(page)

if __name__=="__main__":
    readings()
    labs()
    print("Generated six illustrated readings and ten guided labs.")
