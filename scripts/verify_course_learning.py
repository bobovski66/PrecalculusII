"""Check guided workspaces, math answers, local links, and executable page scripts."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,math,os,re,subprocess,sys,tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from lab_content import LABS
from application_content import APPS

class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.links=[];self.labels=[];self.parts=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if "id" in a:self.ids.append(a["id"])
        if tag=="label" and "for" in a:self.labels.append(a["for"])
        if tag=="textarea" and "data-response" in a:self.parts+=1
        for k in ("href","src"):
            if a.get(k):self.links.append(a[k])

def main():
    failures=[];count=0
    # Include every HTML page, since revised navigation should lead to working resources.
    for f in ROOT.rglob("*.html"):
        if "dist" in f.parts:continue
        s=f.read_text();p=Page();p.feed(s)
        if len(p.ids)!=len(set(p.ids)):failures.append(f"Duplicate IDs: {f.relative_to(ROOT)}")
        for target in p.links:
            u=urlsplit(target)
            if u.scheme or target.startswith("//"):continue
            dest=(f.parent/unquote(u.path)).resolve() if u.path else f
            if not dest.exists():failures.append(f"Missing target {target} from {f.relative_to(ROOT)}")
        for script in re.findall(r"<script(?![^>]*\btype=['\"]application/json)[^>]*>(.*?)</script>",s,re.S):
            if not script.strip():continue
            with tempfile.NamedTemporaryFile(mode="w",suffix=".js") as tmp:
                tmp.write(script);tmp.flush()
                result=subprocess.run([os.environ.get("CODEX_PRIMARY_RUNTIME_NODE","node"),"--check",tmp.name],capture_output=True,text=True)
                if result.returncode:failures.append(f"JS syntax in {f.relative_to(ROOT)}: {result.stderr}")
        count+=1
    for path in (ROOT/"assets").rglob("*.js"):
        result=subprocess.run([os.environ.get("CODEX_PRIMARY_RUNTIME_NODE","node"),"--check",str(path)],capture_output=True,text=True)
        if result.returncode:failures.append(f"JS syntax in {path.relative_to(ROOT)}: {result.stderr}")
    for n,data in LABS.items():
        s=(ROOT/f"labs/week{n:02}_lab.html").read_text();p=Page();p.feed(s)
        payload=json.loads(re.search(r'<script type="application/json" id="lab-data">(.*?)</script>',s,re.S)[1])
        assert payload["key"]==data["key"] and payload["prefix"]==data["prefix"]
        assert p.parts==sum(len(q["parts"]) for q in data["problems"])==14
        assert len(data["problems"])==7
        assert all(label in p.ids for label in p.labels)
        for i,q in enumerate(data["problems"]):
            assert q["hint"] and q["solution"]
            for part,(_,target,tol) in q["checks"].items():
                assert 0<=part<len(q["parts"]) and math.isfinite(target) and tol>0
    for n,data in APPS.items():
        s=(ROOT/f"applications/week{n:02}_applications.html").read_text();p=Page();p.feed(s)
        assert p.parts==sum(len(q["parts"]) for q in data["problems"])==9
        assert all(label in p.ids for label in p.labels)
        assert len(data["problems"])==3
    for n in range(1,11):
        assert (ROOT/f"readings/module{n:02}_reading.html").is_file()
    math_checks=subprocess.run([os.environ.get("CODEX_PRIMARY_RUNTIME_NODE","node"),str(ROOT/"scripts/test_foundations_math.js")],capture_output=True,text=True)
    if math_checks.returncode:failures.append(math_checks.stderr)
    # Independent mathematical checks for the worked equation, triangle, and motion examples.
    for freq in (2,3):
        roots=[(u+2*k*math.pi)/freq for k in range(freq) for u in (math.pi/6,5*math.pi/6)]
        assert len(roots)==2*freq and all(0<=x<2*math.pi and abs(math.sin(freq*x)-.5)<1e-12 for x in roots)
    for B in (math.asin(.8),math.pi-math.asin(.8)):
        C=math.pi-math.pi/6-B
        assert C>0 and abs(5/math.sin(math.pi/6)-8/math.sin(B))<1e-12
    assert abs(sum(5*.6**k for k in range(20))-5*(1-.6**20)/.4)<1e-12
    assert abs(4*(.5j)**3+.5j)<1e-12
    assert abs(3*complex(0,.8)**6-(-3*.8**6))<1e-12
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"Passed: {count} HTML pages, 10 guided labs, 3 guided application pages, local links, JS syntax, and independent math checks.")

if __name__=="__main__":main()
