'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),{execFileSync}=require('node:child_process');
const P=require('../assets/module1/module1.js');
const snapshots=JSON.parse(execFileSync('python3',['scripts/verify_module1.py','--dom-json'],{encoding:'utf8',maxBuffer:8*1024*1024}));
function matches(el,selector){
 let parts=selector.trim().split(/\s+/),last=parts.pop();if(!simple(el,last))return false;let p=el.parentElement;
 while(parts.length){let s=parts.pop();while(p&&!simple(p,s))p=p.parentElement;if(!p)return false;p=p.parentElement;}return true;
}
function simple(el,s){if(!el)return false;let tag=s.match(/^[a-zA-Z][\w-]*/)?.[0];if(tag&&el.tagName!==tag.toUpperCase())return false;for(let m of s.matchAll(/\.([\w-]+)/g))if(!el.className.split(/\s+/).includes(m[1]))return false;for(let m of s.matchAll(/\[([\w-]+)(?:=["']?([^\]"']+)["']?)?\]/g)){if(!(m[1] in el.attrs))return false;if(m[2]!==undefined&&el.attrs[m[1]]!==m[2])return false;}return true;}
class Element{
 constructor(tag,attrs={},text=''){this.tagName=tag.toUpperCase();this.attrs={...attrs};this.children=[];this.parentElement=null;this.ownText=text;this._value=null;this.style={};this.events={};this.disabled='disabled' in attrs;this.checked='checked' in attrs;this.hidden='hidden' in attrs;this.max=attrs.max||'';this.classList={add:(...ss)=>this.className=[...new Set(this.className.split(/\s+/).filter(Boolean).concat(ss))].join(' '),remove:(...ss)=>this.className=this.className.split(/\s+/).filter(s=>!ss.includes(s)).join(' '),toggle:(s,on)=>{let has=this.className.split(/\s+/).includes(s),yes=on===undefined?!has:on;yes?this.classList.add(s):this.classList.remove(s);return yes;}};}
 get previousElementSibling(){return this.parentElement?.children[this.parentElement.children.indexOf(this)-1]||null;}
 get id(){return this.attrs.id||'';}get className(){return this.attrs.class||'';}set className(x){this.attrs.class=x;}
 get dataset(){let d={};Object.entries(this.attrs).filter(([k])=>k.startsWith('data-')).forEach(([k,v])=>d[k.slice(5).replace(/-([a-z])/g,(_,x)=>x.toUpperCase())]=v);return d;}
 get value(){if(this._value!==null)return this._value;if(this.tagName==='TEXTAREA')return this.ownText;if(this.tagName==='SELECT'){let o=this.children.find(x=>'selected' in x.attrs)||this.children[0];return o?.attrs.value||'';}return this.attrs.value||'';}set value(v){this._value=String(v);if(this.tagName==='SELECT'&&!this.children.some(x=>x.attrs.value===this._value))this._value='';}
 get selectedOptions(){return this.children.filter(x=>x.attrs.value===this.value);}
 get textContent(){return this.ownText+this.children.map(x=>x.textContent+(x.tail||'')).join('');}set textContent(x){this.ownText=String(x);this.children=[];}
 set innerHTML(x){this._html=x;this.children=[];this.ownText='';}get innerHTML(){return this._html||'';}
 hasAttribute(k){return Object.hasOwn(this.attrs,k);}
 getAttribute(k){return Object.hasOwn(this.attrs,k)?this.attrs[k]:null;}setAttribute(k,v){this.attrs[k]=String(v);}removeAttribute(k){delete this.attrs[k];}
 querySelectorAll(q){let selectors=q.split(','),out=[];for(let c of this.children){if(selectors.some(s=>matches(c,s)))out.push(c);out.push(...c.querySelectorAll(q));}return out;}querySelector(q){return this.querySelectorAll(q)[0]||null;}
 closest(q){for(let x=this;x;x=x.parentElement)if(matches(x,q))return x;return null;}
 append(...nodes){for(let n of nodes){n.parentElement=this;this.children.push(n);}}replaceChildren(...nodes){this.children=[];this.ownText='';this._html='';this.append(...nodes);}after(n){let p=this.parentElement;if(p){n.parentElement=p;p.children.splice(p.children.indexOf(this)+1,0,n);}}remove(){let p=this.parentElement;if(p)p.children=p.children.filter(n=>n!==this);}
 addEventListener(type,fn){(this.events[type]??=[]).push(fn);}dispatch(type,event={}){for(let fn of this.events[type]||[])fn({preventDefault(){},...event});}click(){if(!this.disabled)this.dispatch('click');}focus(){this.focused=true;}scrollIntoView(o){this.scrolled=o;}
}
function fromJSON(o){let e=new Element(o.tag,o.attrs,o.text);e.tail=o.tail;for(let c of o.children)e.append(fromJSON(c));return e;}
function open(file,initial={},seed=17){
 const root=fromJSON(snapshots[file]),data={...initial},events={},frames=new Map(),blobs=[],downloads=[];let counter=0,clock=0;
 const window={innerWidth:1450,prints:0,confirm:()=>true,addEventListener(k,f){(events[k]??=[]).push(f);},print(){this.prints++;for(let f of events.beforeprint||[])f();}};
 const document={readyState:'complete',body:root.querySelector('body'),hidden:false,querySelectorAll:q=>root.querySelectorAll(q),getElementById:id=>root.querySelectorAll('[id]').find(x=>x.id===id)||null,createElement:tag=>{let e=new Element(tag);if(tag==='a')e.click=()=>downloads.push(e);return e;},addEventListener(k,f){(events[k]??=[]).push(f);}};
 const math=Object.assign(Object.create(Math),{random(){seed=(1664525*seed+1013904223)>>>0;return seed/4294967296;}});
 const sandbox={document,window,localStorage:{getItem:k=>{if(initial.__failStorage)throw Error('blocked');return data[k]??null;},setItem:(k,v)=>{if(initial.__failStorage)throw Error('blocked');data[k]=String(v);},removeItem:k=>{if(initial.__failStorage)throw Error('blocked');delete data[k];}},Math:math,console,Blob:class{constructor(parts,options){this.parts=parts;this.options=options;}},URL:{createObjectURL:b=>{blobs.push(b);return'blob:test';},revokeObjectURL(){}},setTimeout:()=>0,requestAnimationFrame:f=>{frames.set(++counter,f);return counter;},cancelAnimationFrame:id=>frames.delete(id)};
 sandbox.globalThis=sandbox;
 for(let el of root.querySelectorAll('script'))if(!el.getAttribute('src')&&!el.getAttribute('type'))vm.runInNewContext(el.textContent,sandbox);
 assert.equal(sandbox.window.MathJax.tex.inlineMath[0][0],'\\(');assert.equal(sandbox.window.MathJax.tex.displayMath[0][0],'\\[');assert.equal(sandbox.window.MathJax.svg.fontCache,'none');
 vm.runInNewContext(fs.readFileSync('assets/module1/module1.js','utf8'),sandbox,{filename:'module1.js'});
 return{root,document,window,data,events,frames,blobs,downloads,$:id=>document.getElementById(id),fire:(name,e)=>{for(let f of events[name]||[])f(e);},advance(ms){clock+=ms;let f=[...frames.values()];frames.clear();for(let fn of f)fn(clock);}};
}
const close=(a,b)=>assert.ok(Math.abs(a-b)<1e-8+Math.max(Math.abs(a),Math.abs(b))*1e-10,a+' != '+b);
for(let [input,want] of [['5pi/6',5*Math.PI/6],['-sqrt(2)/2',-Math.SQRT2/2],['√3/2',Math.sqrt(3)/2],['2(3+4)',14],['-2^2',-4],['(-2)^2',4],['1e-4',.0001],['(3pi)/(2)',1.5*Math.PI]])close(P.evaluate(input),want);
for(let bad of ['', ' ', '1/0','sqrt(-2)','alert(1)','Math.PI','pi;1','(1+2','2**3','1e309','1/1e309','Infinity','0/0'])assert.throws(()=>P.evaluate(bad),bad);
for(let i=0;i<16;i++){close(P.evaluate(P.C[i]),Math.cos(P.A[i]*Math.PI/180));close(P.evaluate(P.S[i]),Math.sin(P.A[i]*Math.PI/180));close(P.evaluate(P.R[i]),P.A[i]*Math.PI/180);}
const oracle=JSON.parse(execFileSync('python3',['-c',String.raw`
from decimal import Decimal as D,getcontext
import random,json
getcontext().prec=60
pi=D('3.14159265358979323846264338327950288419716939937510582097494459')
def sc(x):
 s=x;c=D(1);a=x;b=D(1)
 for n in range(1,100):
  a=-a*x*x/D((2*n)*(2*n+1));b=-b*x*x/D((2*n-1)*(2*n));s+=a;c+=b
 return s,c
r=random.Random(14201);out=[]
for k in range(500):
 d=D(r.randrange(-2880,2881))/4;radius=D(r.randrange(5,31))/10;n=d%D(360)
 if n<0:n+=360
 y,x=sc(n*pi/180);ref=None if n%90==0 else min(n%180,180-n%180)
 out.append(dict(d=float(d),r=float(radius),n=float(n),x=float(x),y=float(y),px=float(radius*x),py=float(radius*y),arc=float(radius*d*pi/180),distance=float(abs(radius*d*pi/180)),ref=None if ref is None else float(ref)))
print(json.dumps(out))`],{encoding:'utf8'}));
for(let q of oracle){let p=P.angle(q.d,q.r);for(let [key,want] of Object.entries({normalized:q.n,x:q.x,y:q.y,physicalX:q.px,physicalY:q.py,directedArc:q.arc,distance:q.distance}))close(p[key],want);assert.equal(p.reference,q.ref);}
const C=JSON.parse(fs.readFileSync('scripts/module1_original_contracts.json','utf8'));
for(let [file,key,count] of [['labs/week01_lab.html',C.labKey,7],['applications/week01_applications.html','m142app1',11]]){
 let saved={student:'Ada <Lee>',date:'2026-10-19'};for(let i=0;i<count;i++)saved['a'+i]='Response '+i+'\n<script>alert("x")</script> π/3';let p=open(file,{[key]:JSON.stringify(saved)});assert.equal(p.$('student').value,saved.student);for(let i=0;i<count;i++)assert.equal(p.$('a'+i).value,saved['a'+i]);p.$('a0').value='Revised work';p.$('a0').dispatch('input');assert.equal(JSON.parse(p.data[key]).a0,'Revised work');p.$('prepare').click();assert.equal(p.downloads.length,1);let output=p.blobs[0].parts.join('');assert.ok(output.includes('&lt;script&gt;')&&!output.includes('<script>'));assert.equal((output.match(/<section>/g)||[]).length,count);p.$('print').click();assert.equal(p.window.prints,1);assert.equal(p.root.querySelectorAll('.print-answer').length,count+2);assert.equal(p.root.querySelectorAll('.print-answer')[2].textContent,'Revised work');p.window.confirm=()=>false;p.$('clear').click();assert.equal(p.$('a0').value,'Revised work');p.window.confirm=()=>true;p.$('clear').click();assert.equal(p.$('a0').value,'');assert.ok(!p.data[key]);let bad=open(file,{__failStorage:true});bad.$('student').value='Test';bad.$('a0').value='Keep this';bad.$('a0').dispatch('input');assert.ok(bad.$('saveStatus').textContent.includes('unavailable'));bad.$('prepare').click();assert.equal(bad.downloads.length,1);
}
{
 let p=open('quizzes/week01_quiz.html');let buttons=p.root.querySelectorAll('[data-check-quiz]');buttons[0].click();assert.ok(p.$('feedback0').textContent.includes('Enter'));for(let i=0;i<10;i++){p.$('q'+i).value=C.quiz[i][1];buttons[i].click();assert.ok(p.$('q'+i).disabled);}assert.equal(p.$('score').textContent,'10 of 10 questions mastered');p.$('reset').click();assert.equal(p.$('score').textContent,'0 of 10 questions mastered');
 let legacy=open('quizzes/week01_quiz.html',{[C.quizKey]:JSON.stringify({0:true,7:true,99:true,noise:true}),[C.quizKey+'_responses_v1']:JSON.stringify({1:'-3pi/4'})});assert.equal(legacy.$('score').textContent,'2 of 10 questions mastered');assert.ok(legacy.$('q0').disabled&&legacy.$('q7').disabled);assert.equal(legacy.$('q1').value,'-3pi/4');for(let corrupt of ['"oops"','[]','null','{']){let t=open('quizzes/week01_quiz.html',{[C.quizKey]:corrupt});assert.equal(t.$('score').textContent,'0 of 10 questions mastered');}
 let blocked=open('quizzes/week01_quiz.html',{__failStorage:true});blocked.$('q0').value='5pi/6';blocked.root.querySelectorAll('[data-check-quiz]')[0].click();assert.ok(blocked.$('q0').disabled);
}
const render=process.argv.find(x=>x.startsWith('--render-dir='))?.split('=')[1];if(render)fs.mkdirSync(render,{recursive:true});function saveSVG(name,markup){if(!render)return;let chunks=markup.match(/<svg[\s\S]*?<\/svg>/g)||[];chunks.forEach((x,i)=>fs.writeFileSync(render+'/'+name+(chunks.length>1?'-'+(i+1):'')+'.svg',x));}
{
 let p=open('demos/unit_circle.html');p.$('radius').value='3';p.$('radius').dispatch('input');assert.ok(p.$('plot').innerHTML.includes('r="195"'));assert.equal(p.$('xy').textContent,'(√3/2, 1/2)');saveSVG('circle-radius3',p.$('plot').innerHTML);let old=p.$('xy').textContent;p.$('angle').value='405';p.$('angle').dispatch('input');let point=p.$('xy').textContent,arc=p.$('arc').textContent;p.$('angle').value='-315';p.$('angle').dispatch('input');assert.equal(p.$('xy').textContent,point);assert.notEqual(p.$('arc').textContent,arc);saveSVG('circle-negative-turn',p.$('plot').innerHTML);p.$('radiansEntry').value='pi/7';p.$('radiansEntry').dispatch('change');close(Number(p.$('angle').value),180/7);p.$('degreesEntry').value='bad';p.$('degreesEntry').dispatch('change');assert.equal(p.$('plot').innerHTML,'');assert.ok(p.$('circleError').textContent);p.$('reset').click();assert.equal(p.$('xy').textContent,old);
}
{
 let p=open('demos/circle_to_wave.html');p.$('canvas').clientWidth=1000;p.$('degreesEntry').value='60';p.$('degreesEntry').dispatch('change');assert.ok(p.$('canvas').innerHTML.includes('1100 530'));saveSVG('wave-wide-60',p.$('canvas').innerHTML);p.$('canvas').clientWidth=500;p.fire('resize');assert.ok(p.$('canvas').innerHTML.includes('480 740'));saveSVG('wave-narrow-60',p.$('canvas').innerHTML);p.$('plotUnits').value='deg';p.$('plotUnits').dispatch('change');assert.ok(p.$('canvas').innerHTML.includes('720°'));p.$('radiansEntry').value='4pi';p.$('radiansEntry').dispatch('change');assert.ok(p.$('out').textContent.startsWith('720°'));saveSVG('wave-two-turns',p.$('canvas').innerHTML);p.$('restart').click();p.$('toggle').click();for(let i=0;i<200;i++)p.advance(100);assert.ok(p.$('out').textContent.startsWith('720°'));assert.equal(p.frames.size,0);p.$('restart').click();p.$('toggle').click();p.document.hidden=true;p.fire('visibilitychange');assert.equal(p.frames.size,0);p.$('degreesEntry').value='721';p.$('degreesEntry').dispatch('change');assert.equal(p.$('canvas').innerHTML,'');assert.ok(p.$('waveError').textContent);
}
{
 let p=open('practice/unit_circle_practice.html',{[C.practiceKey]:JSON.stringify({correct:17,attempts:23})},25);let attempts=23,correct=17;
 for(let mode of ['rad','deg','sin','cos','point']){p.$('topic').value=mode;p.$('topic').dispatch('change');for(let n=0;n<12;n++){assert.ok(p.$('next').disabled);assert.ok(p.$('values').textContent.includes('reveal'));let question=p.$('question').textContent;let i=mode==='rad'||mode==='point'?P.A.findIndex(d=>question.includes((mode==='rad'?'Convert ':'= ')+d+'°')):P.R.findIndex(r=>question.includes((mode==='deg'?'Convert ':'(')+r+(mode==='deg'?' radians':')')));assert.ok(i>=0,question);let value=P.practiceValue(mode,i),choices=p.$('choices').querySelectorAll('button');assert.equal(new Set(choices.map(b=>b.textContent)).size,4);let wrong=choices.find(b=>b.textContent!==value);wrong.click();attempts++;assert.ok(wrong.disabled);assert.ok(p.$('next').disabled);let right=choices.find(b=>b.textContent===value);assert.ok(right);right.click();attempts++;correct++;assert.ok(!p.$('next').disabled);assert.ok(p.$('feedback').textContent.startsWith('Correct.'));right.click();assert.deepEqual(JSON.parse(p.data[C.practiceKey]),{correct,attempts});if(mode==='point'&&n===0)saveSVG('practice-revealed',p.$('circle').innerHTML);p.$('next').click();}}
 p.$('reset').click();assert.equal(p.$('score').textContent,'0 correct answers · 0 total attempts');open('practice/unit_circle_practice.html',{__failStorage:true});
}
console.log('PASS: 500 independent geometry oracles; 16 exact-angle values; all 10 quiz items and legacy mastery; 7 lab and 11 application responses, exports, and printing; both explorer layouts and animation; 60 practice questions and preserved scores.');
