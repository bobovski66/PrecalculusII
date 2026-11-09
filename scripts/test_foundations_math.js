const assert=require("node:assert/strict");
const M=require("../assets/foundations-math.js");
const near=(a,b,t=1e-9)=>assert.ok(Math.abs(a-b)<t,String(a)+" != "+b);
assert.equal(M.six(90).tan,null);
assert.equal(M.six(90).cot,0);
assert.equal(M.six(180).cot,null);
assert.equal(M.six(180).tan,0);
near(M.six(60).tan,Math.sqrt(3));
near(M.inverse(150).sin,30);
near(M.inverse(150).cos,150);
near(M.inverse(-120).sin,-60);
assert.equal(M.inverse(90).tan,null);
assert.equal(M.wave(0,2,1,3).period,null);
assert.throws(()=>M.wave(1,0,0,0),RangeError);
for(let i=0;i<721;i++){
  const angle=i-360,v=M.six(angle),inv=M.inverse(angle);
  near(v.sin*v.sin+v.cos*v.cos,1);
  near(M.six(angle+360).sin,v.sin);
  near(M.six(angle+360).cos,v.cos);
  assert.ok(inv.sin>=-90-1e-9&&inv.sin<=90+1e-9);
  assert.ok(inv.cos>=-1e-9&&inv.cos<=180+1e-9);
  near(Math.sin(inv.sin*Math.PI/180),v.sin);
  near(Math.cos(inv.cos*Math.PI/180),v.cos);
  if(inv.tan!==null){
    assert.ok(inv.tan>-90&&inv.tan<90);
    near(Math.tan(inv.tan*Math.PI/180),v.tan,1e-7);
  }
}
for(const B of [.25,.5,1,2,4,-2]){
  const m=M.wave(-3,B,1,-2);
  near(m.minimum,-5);near(m.maximum,1);
  for(const x of [-4,-1,0,1,3,6])near(m.value(x+m.period),m.value(x));
  near(m.landmarks[0].y,-2);near(m.landmarks[4].y,-2);
}
const c=M.wave(-2,Math.PI,1,3,"cos");
assert.deepEqual(c.landmarks.map(p=>Number(p.y.toFixed(8))),[1,3,5,3,1]);
console.log("Passed axis-domain, principal-range, periodicity, constant-wave, and landmark checks.");
