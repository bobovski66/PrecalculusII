"""Compile to stable contents, check PDF text/bounds, and render every page."""
from pathlib import Path
import argparse,subprocess,shutil,tempfile,json,re
import fitz
from PIL import Image,ImageOps,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
def sheet(paths,dest,cols=3):
    thumbs=[]
    for p in paths:
        im=Image.open(p).convert('RGB');im.thumbnail((330,455));canvas=Image.new('RGB',(350,485),'#e1e7eb');canvas.paste(im,((350-im.width)//2,10));ImageDraw.Draw(canvas).text((12,465),p.stem,fill='black');thumbs.append(canvas)
    canvas=Image.new('RGB',(350*cols,485*((len(thumbs)+cols-1)//cols)),'white')
    for i,im in enumerate(thumbs):canvas.paste(im,((i%cols)*350,(i//cols)*485))
    canvas.save(dest)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--install',action='store_true');args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True);report={}
    for stem,dest in [('standalone','PrecalcII_Week01.pdf'),('master','PrecalculusII_Complete_Reader.pdf')]:
        work=args.out/stem;work.mkdir(exist_ok=True);previous=None
        for iteration in range(5):
            r=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',f'-output-directory={work.resolve()}',stem+'.tex'],cwd=ROOT/'notes',capture_output=True,text=True)
            (work/'compile-output.txt').write_text(r.stdout+r.stderr)
            if r.returncode:raise RuntimeError(r.stdout[-7000:])
            state=tuple((work/(stem+'.'+suffix)).read_bytes() if (work/(stem+'.'+suffix)).exists() else b'' for suffix in ['aux','toc','out'])
            if iteration>=1 and state==previous and 'Rerun to get' not in r.stdout:break
            previous=state
        else:raise RuntimeError('PDF pagination did not stabilize.')
        pdf=work/(stem+'.pdf');doc=fitz.open(pdf);bounds=[];missing=[];pages=[]
        for n,p in enumerate(doc):
            for block in p.get_text('dict')['blocks']:
                for line in block.get('lines',[]):
                    for span in line['spans']:
                        if '\ufffd' in span['text']:missing.append([n+1,span['text']])
                        x0,y0,x1,y1=span['bbox']
                        if x0<25 or x1>p.rect.width-25 or y0<15 or y1>p.rect.height-15:bounds.append([n+1,span['text'],span['bbox']])
            path=work/f'page-{n+1:02d}.png';p.get_pixmap(matrix=fitz.Matrix(1.1,1.1)).save(path);pages.append(path)
        for i in range(0,len(pages),12):sheet(pages[i:i+12],work/f'contact-{i//12+1}.png')
        toc_ok=True
        if stem=='master':
            toc=(work/'master.toc').read_text();entries=re.findall(r'\\contentsline \{section\}\{\\numberline \{(\d+)\}(.*?)\}\{(\d+)\}',toc)
            if len(entries)!=10:raise AssertionError(f'Expected ten chapter entries, got {len(entries)}')
            for number,title,page in entries:
                # Chapter headings use the section number and title, independent of TOC wrapping.
                title_plain=title.replace('\\&','&')
                needle=re.sub(r'\s+','',number+title_plain)
                found=[j+1 for j,p in enumerate(doc) if needle in re.sub(r'\s+','',p.get_text())[:500]]
                if not found or int(page)!=found[-1]:raise AssertionError(f'TOC {number}: expected {page}, found {found}')
        warnings=[s for s in r.stdout.splitlines() if any(w in s for w in ['Overfull','Missing character','LaTeX Warning'])]
        report[dest]={'pages':len(doc),'bytes':pdf.stat().st_size,'passes':iteration+1,'warnings':warnings,'outOfBounds':bounds,'missingGlyphs':missing,'tableOfContentsVerified':toc_ok}
        if bounds or missing:raise AssertionError(report[dest])
        if stem=='standalone' and warnings:raise AssertionError(warnings)
        if args.install:shutil.copyfile(pdf,ROOT/'pdfs'/dest)
        print(dest,json.dumps(report[dest]))
    for path in ['notes/preamble.tex']+[f'notes/week{n:02d}.tex' for n in range(2,11)]:
        original=subprocess.check_output(['git','show','90db525435778ad591d46364b337898824465c90:'+path],cwd=ROOT)
        assert (ROOT/path).read_bytes()==original,path
    report['remainingChapters']={'latexSourcesUnchanged':True}
    (args.out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
