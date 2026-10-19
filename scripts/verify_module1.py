"""Check published question contracts, links, semantics, and unchanged modules."""
from pathlib import Path
import json,re,sys,subprocess
from urllib.parse import urlsplit,unquote
from lxml import html,etree
ROOT=Path(__file__).resolve().parents[1]
C=json.loads((ROOT/'scripts/module1_original_contracts.json').read_text());BASE=C['base']
PAGES=['readings/module01_reading.html','demos/unit_circle.html','demos/circle_to_wave.html','labs/week01_lab.html','applications/week01_applications.html','practice/unit_circle_practice.html','quizzes/week01_quiz.html']
def original(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def snap(el):return {'tag':el.tag,'attrs':dict(el.attrib),'text':el.text or '','tail':el.tail or '','children':[snap(c) for c in el if isinstance(c.tag,str)]}
def main():
    snapshots={};configs={}
    for path in PAGES:
        p=ROOT/path;s=p.read_text();doc=html.fromstring(s);ids=doc.xpath('//*[@id]/@id');assert len(ids)==len(set(ids)),path
        assert len(doc.xpath('//main'))==1 and len(doc.xpath('//h1'))==1,path
        assert doc.xpath('//a[@class="skip" and @href="#main"]'),path
        for node in doc.xpath('//*[@href or @src]'):
            raw=node.get('href',node.get('src'));url=urlsplit(raw)
            if url.scheme or url.netloc:continue
            target=(p.parent/unquote(url.path)).resolve() if url.path else p
            assert target.exists(),(path,raw)
            if url.fragment and target.suffix=='.html':assert html.fromstring(target.read_text()).xpath('//*[@id=$id]',id=url.fragment),(path,raw)
        for img in doc.xpath('//img'):assert len(img.get('alt',''))>25,(path,'image description')
        for el in doc.xpath('//input|//textarea|//select'):
            assert el.get('id') and doc.xpath('//label[@for=$id]',id=el.get('id')),(path,el.get('id'))
        for el in doc.xpath('//*[@aria-describedby]'):
            for id in el.get('aria-describedby').split():assert id in ids,(path,id)
        scripts=doc.xpath('//script[not(@src) and not(@type="application/json")]')
        assert len(scripts)==1 and 'MathJax' in scripts[0].text,path
        config=doc.xpath('//script[@id="activityData"]')
        if config:configs[path]=json.loads(config[0].text)
        snapshots[path]=snap(doc)
    assert configs[PAGES[3]]['questions']==C['lab'] and configs[PAGES[3]]['key']==C['labKey']
    assert configs[PAGES[6]]['questions']==C['quiz'] and configs[PAGES[6]]['key']==C['quizKey']
    assert configs[PAGES[5]]['key']==C['practiceKey']
    assert [q[1] for q in configs[PAGES[4]]['questions']]==C['applications']
    assert len(C['lab'])==7 and len(C['quiz'])==10 and len(C['applications'])==11
    tex=(ROOT/'notes/week01.tex').read_text()
    for q in C['tryIts']+C['exercises']:assert q in tex,'Changed original chapter problem'
    assert len(C['tryIts'])==6 and len(C['exercises'])==13
    tracked=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],cwd=ROOT,text=True).splitlines()
    changed=set(PAGES+['index.html','notes/week01.tex','notes/master.tex','notes/standalone.tex','README.md','.github/workflows/build-notes.yml','pdfs/PrecalcII_Week01.pdf','pdfs/PrecalculusII_Complete_Reader.pdf'])
    for path in tracked:
        if path not in changed:assert (ROOT/path).read_bytes()==original(path),f'Out-of-scope change: {path}'
    home=(ROOT/'index.html').read_text();old=original('index.html').decode()
    assert re.search(r'const modules=(.*?);const resources=',home,re.S)[1]==re.search(r'const modules=(.*?);const resources=',old,re.S)[1]
    for key in ['math142_progress_v1','math142_theme','w${m.week}_${j}']:assert key in home
    assert "m.week===1?['readings/module01_reading.html'" in home
    for svg in (ROOT/'assets/module1').glob('*.svg'):
        etree.parse(str(svg));assert svg.with_suffix('.pdf').exists()
    assert len(list((ROOT/'assets/module1').glob('*.svg')))==18
    if '--dom-json' in sys.argv:print(json.dumps(snapshots,ensure_ascii=False))
    else:print('PASS: seven pages; links and labels; original 7 lab prompts, 11 application questions, 10 quiz items, 6 practice and 13 review problems; saved-progress keys; 18 diagram pairs; other modules unchanged.')
if __name__=='__main__':main()
