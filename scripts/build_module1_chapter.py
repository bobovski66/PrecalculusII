"""Convert the shared reading to LaTeX; preserve the original practice prompts."""
from pathlib import Path
from html import unescape
import re,json
from lxml import html
from module1_content import SECTIONS,FORMULAS,TRY_SOLUTIONS,REVIEW_SOLUTIONS
ROOT=Path(__file__).resolve().parents[1]
C=json.loads((ROOT/'scripts/module1_original_contracts.json').read_text())
def plain(s):
    mapping={'&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}','\\':r'\textbackslash{}'}
    s=s.replace('√3',r'@@SQRTTHREE@@').replace('√2',r'@@SQRTTWO@@')
    for a,b in [('“','"'),('”','"'),('‘',"'"),('’',"'"),('—','---'),('–','--'),('−','-'),('°',r'@@DEG@@'),('π',r'@@PI@@'),('θ',r'@@THETA@@')]:s=s.replace(a,b)
    s=''.join(mapping.get(c,c) for c in s)
    return s.replace('@@SQRTTHREE@@',r'\(\sqrt3\)').replace('@@SQRTTWO@@',r'\(\sqrt2\)').replace('@@DEG@@',r'\(^{\circ}\)').replace('@@PI@@',r'\(\pi\)').replace('@@THETA@@',r'\(\theta\)')
def text(s):
    if not s:return ''
    parts=re.split(r'(\\\(.*?\\\)|\\\[.*?\\\])',unescape(s),flags=re.S)
    return ''.join(p if p.startswith(('\\(','\\[')) else plain(p) for p in parts)
def children(el):return text(el.text)+''.join(node(c)+text(c.tail) for c in el)
def node(el):
    tag=el.tag
    if not isinstance(tag,str):return ''
    if tag=='figure':
        img=el.find('img');name=Path(img.get('src')).stem;cap=children(el.find('figcaption'))
        height='2.9in' if name in ['one-radian','unit-circle-coordinates','quadrant-signs'] else '2.5in'
        return '\n\\begin{center}\\begin{minipage}{\\linewidth}\\centering\n'+f'\\includegraphics[width=\\linewidth,height={height},keepaspectratio]{{../assets/module1/{name}.pdf}}\n'+r'\captionsetup{type=figure,labelformat=empty,font=small}\caption*{'+cap+'}\n\\end{minipage}\\end{center}\n'
    if tag in ['div','aside'] and any(x in el.get('class','').split() for x in ['example','note']):
        title=el.find('h3');env='moneexample' if 'example' in el.get('class','') else 'moneaside'
        return '\n\\begin{'+env+'}{'+children(title)+'}\n'+text(title.tail)+''.join(node(c)+text(c.tail) for c in el if c is not title)+'\n\\end{'+env+'}\n'
    if tag=='p':return '\n'+children(el)+'\n\n'
    if tag in ['h2','h3']:return '\n\\subsubsection*{'+children(el)+'}\n'
    if tag in ['em','i']:return r'\emph{'+children(el)+'}'
    if tag in ['strong','b']:return r'\textbf{'+children(el)+'}'
    if tag=='code':return r'\texttt{'+children(el)+'}'
    if tag=='a':return r'\href{'+el.get('href','').replace('%',r'\%')+'}{'+children(el)+'}'
    if tag=='table':
        rows=el.xpath('.//tr');n=len(rows[0]);out='\n\\begin{center}\\small\\renewcommand{\\arraystretch}{1.35}\\begin{tabularx}{\\linewidth}{'+'Z'*n+'}\\toprule\n'
        for j,row in enumerate(rows):out+=' & '.join((r'\textbf{'+children(c)+'}' if c.tag=='th' else children(c)) for c in row)+r' \\'+'\n'+(r'\midrule'+'\n' if j==0 else '')
        return out+'\\bottomrule\\end{tabularx}\\end{center}\n'
    if tag in ['ul','ol']:return '\n\\begin{'+('itemize' if tag=='ul' else 'enumerate')+'}\n'+children(el)+'\n\\end{'+('itemize' if tag=='ul' else 'enumerate')+'}\n'
    if tag=='li':return '\\item '+children(el)+'\n'
    return children(el)
def convert(fragment):return children(html.fragment_fromstring(fragment,create_parent='div'))
def build():
    setup=r'''\input{glyphtounicode}
\pdfgentounicode=1
\usepackage{tabularx,booktabs,needspace,caption,tcolorbox}
\newcolumntype{Z}{>{\raggedright\arraybackslash}X}
\definecolor{moneblue}{HTML}{28678B}
\definecolor{monegreen}{HTML}{26865D}
\definecolor{monegold}{HTML}{B97424}
\newtcolorbox{moneexample}[1]{colback=moneblue!5,colframe=moneblue!65,title=#1,colbacktitle=moneblue!12,coltitle=black,fonttitle=\bfseries,boxrule=.5pt,arc=2pt,left=10pt,right=10pt,top=8pt,bottom=8pt,before skip=14pt,after skip=14pt}
\newtcolorbox{moneaside}[1]{colback=monegold!7,colframe=monegold!65,title=#1,colbacktitle=monegold!14,coltitle=black,fonttitle=\bfseries,boxrule=.5pt,arc=2pt,left=10pt,right=10pt,top=8pt,bottom=8pt,before skip=14pt,after skip=14pt}
\newtcolorbox{monecheck}[1]{colback=monegreen!5,colframe=monegreen!65,title=#1,colbacktitle=monegreen!12,coltitle=black,fonttitle=\bfseries,boxrule=.5pt,arc=2pt,left=10pt,right=10pt,top=8pt,bottom=8pt,before skip=14pt,after skip=14pt}
'''
    (ROOT/'notes/module1_setup.tex').write_text(setup)
    (ROOT/'notes/standalone.tex').write_text(r'''\documentclass[12pt]{article}
\input{preamble}
\input{module1_setup}
\geometry{margin=1in}
\fancyhead[L]{MATH\& 142 -- Module 1}
\begin{document}
\input{week01}
\end{document}
''')
    master=ROOT/'notes/master.tex';s=master.read_text()
    if '\\input{module1_setup}' not in s:master.write_text(s.replace('\\input{preamble}','\\input{preamble}\n\\input{module1_setup}'))
    out=r'''\section{Angles, Radians, and the Unit Circle}
\begingroup
\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}\setlength{\emergencystretch}{1em}
\clubpenalty=10000\widowpenalty=10000
A turning wheel connects angle, distance, speed, and position. This chapter develops those connections from a coordinate sketch to a model of a rider's height over time. Work through each example with pencil and paper. Pause at each check before reading its explanation at the end of the chapter.

\textbf{Learning objectives.} Describe signed rotations; convert between degrees and radians; distinguish arc length, displacement, angular velocity, and tangential speed; derive exact unit-circle coordinates; and connect circular motion with periodic graphs and a height model.

\href{https://bobovski66.github.io/PrecalculusII/readings/module01_reading.html}{Online reading and interactive activities}
\par\smallskip
{\small Further reading: OpenStax, \emph{Precalculus 2e},
\href{https://openstax.org/books/precalculus-2e/pages/5-1-angles}{5.1 Angles} and
\href{https://openstax.org/books/precalculus-2e/pages/5-2-unit-circle-sine-and-cosine-functions}{5.2 Unit Circle: Sine and Cosine Functions}.}

'''
    for i,sec in enumerate(SECTIONS,1):out+='\n\\subsection{'+text(sec['title'])+'}\n'+convert(sec['body'])+'\n\\begin{monecheck}{Check '+str(i)+'}\n'+text(sec['question'])+'\n\\end{monecheck}\n'
    out+='\n\\clearpage\n\\subsection{Choose a relationship}\n'+convert(FORMULAS)
    out+='\n\\subsection{Practice with explanation}\nAttempt each problem before consulting the explanations.\n'
    for q in C['tryIts']:out+='\n\\begin{practice}'+q+'\\end{practice}\n'
    out+='\n\\clearpage\n\\subsection{Review exercises}\n\\begin{enumerate}\n'+''.join('\\item '+q for q in C['exercises'])+'\\end{enumerate}\n'
    out+='\n\\clearpage\n\\subsection{Explanations for the checks}\n\\begin{enumerate}\n'+''.join('\\item '+text(s['answer'])+'\n' for s in SECTIONS)+'\\end{enumerate}\n'
    out+='\n\\subsection{Practice solutions}\n\\begin{enumerate}\n'+''.join('\\item '+text(a)+'\n' for a in TRY_SOLUTIONS)+'\\end{enumerate}\n'
    out+='\n\\subsection{Review solutions}\n\\begin{enumerate}\n'+''.join('\\item '+text(a)+'\n' for a in REVIEW_SOLUTIONS)+'\\end{enumerate}\n'
    out+=r'''\endgroup
\clearpage
'''
    (ROOT/'notes/week01.tex').write_text(out)
    print('Built Module 1 LaTeX from the shared reading; retained all 19 practice/review prompts.')
if __name__=='__main__':build()
