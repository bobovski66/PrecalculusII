/* Mathematical models shared by the foundation explorers and invariant checks. */
(function(root){
  "use strict";
  const EPS=1e-10;
  function six(degrees){
    const angle=degrees*Math.PI/180;
    let x=Math.cos(angle),y=Math.sin(angle);
    if(Math.abs(x)<EPS)x=0;if(Math.abs(y)<EPS)y=0;
    return {x,y,sin:y,cos:x,tan:x===0?null:y===0?0:y/x,cot:y===0?null:x===0?0:x/y,
      sec:x===0?null:1/x,csc:y===0?null:1/y};
  }
  function wave(A,B,C,D,kind="sin"){
    if(!Number.isFinite(B)||B===0)throw new RangeError("Choose a nonzero frequency coefficient.");
    const cycle=2*Math.PI/Math.abs(B);
    const value=x=>A*(kind==="cos"?Math.cos(B*(x-C)):Math.sin(B*(x-C)))+D;
    return {amplitude:Math.abs(A),period:A===0?null:cycle,cycle,
      minimum:D-Math.abs(A),maximum:D+Math.abs(A),midline:D,shift:C,value,
      landmarks:Array.from({length:5},(_,i)=>({x:C+i*cycle/4,y:value(C+i*cycle/4)}))};
  }
  function inverse(degrees){
    const values=six(degrees),r=180/Math.PI;
    return {values,sin:Math.asin(Math.max(-1,Math.min(1,values.sin)))*r,
      cos:Math.acos(Math.max(-1,Math.min(1,values.cos)))*r,
      tan:values.tan===null?null:Math.atan(values.tan)*r};
  }
  const api={six,wave,inverse};
  root.math142Foundations=api;
  if(typeof module!=="undefined"&&module.exports)module.exports=api;
})(typeof window==="undefined"?globalThis:window);
