(() => {
  "use strict";
  const M=window.math142Foundations;
  const by=id=>document.getElementById(id);
  const fmt=x=>x===null?"undefined":(Math.abs(x)<1e-9?0:x).toFixed(3);
  function circle(g,c){
    const ox=c.width/2,oy=c.height/2,r=Math.min(c.width*.34,c.height*.35);
    g.clearRect(0,0,c.width,c.height);g.lineWidth=1;g.strokeStyle="#c2ced6";
    g.beginPath();g.moveTo(35,oy);g.lineTo(c.width-35,oy);g.moveTo(ox,20);g.lineTo(ox,c.height-30);g.stroke();
    g.strokeStyle="#96adbc";g.lineWidth=2;g.beginPath();g.arc(ox,oy,r,0,2*Math.PI);g.stroke();
    g.font="17px system-ui";g.fillStyle="#526572";g.fillText("x",c.width-28,oy-8);g.fillText("y",ox+10,25);
    return {ox,oy,r,X:x=>ox+r*x,Y:y=>oy-r*y};
  }
  function line(g,p,q,color,width=3,dash=[]){
    g.strokeStyle=color;g.lineWidth=width;g.setLineDash(dash);g.beginPath();g.moveTo(...p);g.lineTo(...q);g.stroke();g.setLineDash([]);
  }
  function point(g,x,y,color,r=5){g.fillStyle=color;g.beginPath();g.arc(x,y,r,0,2*Math.PI);g.fill();}
  function six(){
    const a=by("angle"),cv=by("graph"),g=cv.getContext("2d");
    function draw(){
      const d=Number(a.value),v=M.six(d),norm=((d%360)+360)%360;
      by("angleOut").textContent=d+"°";
      by("coords").textContent="(cos θ, sin θ) = ("+fmt(v.cos)+", "+fmt(v.sin)+")";
      by("quad").textContent=norm%90===0?"The point lies on a coordinate axis.":"Quadrant "+(Math.floor(norm/90)+1);
      const names=[["sin",v.sin,"y"],["cos",v.cos,"x"],["tan",v.tan,"y / x"],
        ["csc",v.csc,"1 / y"],["sec",v.sec,"1 / x"],["cot",v.cot,"x / y"]];
      by("values").innerHTML="<table><thead><tr><th>Function</th><th>Ratio</th><th>Value</th></tr></thead><tbody>"+
        names.map(([name,value,ratio])=>"<tr><th>"+name+" θ</th><td>"+ratio+"</td><td>"+fmt(value)+"</td></tr>").join("")+"</tbody></table>";
      by("denominator-note").textContent=v.cos===0?"Cosine is zero: tangent and secant are undefined. Cotangent is zero.":
        v.sin===0?"Sine is zero: cosecant and cotangent are undefined. Tangent is zero.":
        "Both coordinate denominators are nonzero, so all six values are defined.";
      const p=circle(g,cv);const {ox,oy,r,X,Y}=p;
      line(g,[ox,oy],[X(v.cos),oy],"#28678b",5);
      line(g,[X(v.cos),oy],[X(v.cos),Y(v.sin)],"#26865d",5);
      line(g,[ox,oy],[X(v.cos),Y(v.sin)],"#b97424",3);point(g,X(v.cos),Y(v.sin),"#b97424",6);
      line(g,[X(1),Y(-1.25)],[X(1),Y(1.25)],"#26865d",1);
      g.font="16px system-ui";g.fillStyle="#26865d";g.fillText("x = 1",X(1)-38,Y(1.3));
      if(v.tan!==null){
        const extent=1.25/Math.max(1,Math.abs(v.tan));
        line(g,[X(-extent),Y(-extent*v.tan)],[X(extent),Y(extent*v.tan)],"#a7b8c3",2,[6,5]);
        if(Math.abs(v.tan)<=1.25){point(g,X(1),Y(v.tan),"#26865d",6);}
      }
      g.fillStyle="#193044";g.font="17px system-ui";
      g.fillText("Blue: horizontal coordinate     Green: vertical coordinate",35,cv.height-12);
      by("tangent-note").textContent=v.tan===null?"The terminal line is vertical; it has no slope.":
        Math.abs(v.tan)>1.25?"The tangent-line intersection is outside this view. Its height is "+fmt(v.tan)+".":
        "The line through the point meets x = 1 at height "+fmt(v.tan)+".";
    }
    a.addEventListener("input",draw);draw();
  }
  function wave(){
    const ids=["a","b","c","d"],inputs=ids.map(by),cv=by("graph"),g=cv.getContext("2d");
    function draw(){
      const [A,B,C,D]=inputs.map(e=>Number(e.value)),kind=by("wave-kind").value,m=M.wave(A,B,C,D,kind);
      ids.forEach((id,i)=>by(id+"o").textContent=inputs[i].value);
      by("equation").textContent="y = "+A+" "+kind+"("+B+"(x − "+C+")) + "+D;
      by("properties").textContent="Amplitude "+m.amplitude+"; midline "+D+"; range ["+m.minimum+", "+m.maximum+"]. "+
        (m.period===null?"Constant output: no least positive period.":"Period "+fmt(m.period)+" input units; horizontal shift "+C+".");
      const focus=by("view").value==="cycle",W=cv.width,H=cv.height,pad=65;
      const xmin=focus?C-m.cycle*.15:-2*Math.PI,xmax=focus?C+m.cycle*1.15:2*Math.PI;
      const extent=Math.max(5,Math.abs(A)+Math.abs(D)+1),ymin=-extent,ymax=extent;
      const X=x=>pad+(x-xmin)/(xmax-xmin)*(W-2*pad),Y=y=>H-pad-(y-ymin)/(ymax-ymin)*(H-2*pad);
      g.clearRect(0,0,W,H);g.font="15px system-ui";
      for(let i=0;i<=8;i++){
        const x=xmin+i*(xmax-xmin)/8,y=ymin+i*(ymax-ymin)/8;
        line(g,[X(x),pad],[X(x),H-pad],"#e0e7eb",1);
        line(g,[pad,Y(y)],[W-pad,Y(y)],"#e0e7eb",1);
        g.fillStyle="#526572";g.fillText(x.toFixed(2),X(x)-17,H-pad+25);g.fillText(y.toFixed(1),8,Y(y)+5);
      }
      if(xmin<=0&&xmax>=0)line(g,[X(0),pad],[X(0),H-pad],"#8da4b5",1.5);
      line(g,[pad,Y(0)],[W-pad,Y(0)],"#8da4b5",1.5);
      line(g,[pad,Y(D)],[W-pad,Y(D)],"#b97424",2,[6,5]);
      g.save();g.beginPath();g.rect(pad,pad,W-2*pad,H-2*pad);g.clip();
      g.strokeStyle="#28678b";g.lineWidth=3;g.beginPath();
      for(let i=0;i<=1200;i++){let x=xmin+i*(xmax-xmin)/1200;i?g.lineTo(X(x),Y(m.value(x))):g.moveTo(X(x),Y(m.value(x)));}
      g.stroke();
      if(m.period!==null)m.landmarks.forEach(p=>point(g,X(p.x),Y(p.y),"#b97424",5));
      g.restore();
      g.fillStyle="#193044";g.fillText("Input x",W/2-22,H-10);g.fillText("Output y",12,28);
      by("landmarks").innerHTML=m.period===null?"<p>The graph is the constant y = "+D+".</p>":
        "<table><thead><tr><th>Cycle point</th><th>x</th><th>y</th></tr></thead><tbody>"+
        m.landmarks.map((p,i)=>"<tr><td>"+["Start","Quarter","Half","Three quarters","End"][i]+"</td><td>"+fmt(p.x)+"</td><td>"+fmt(p.y)+"</td></tr>").join("")+"</tbody></table>";
    }
    inputs.forEach(e=>e.addEventListener("input",draw));["view","wave-kind"].forEach(id=>by(id).addEventListener("change",draw));
    by("reset").onclick=()=>{[2,1,0,0].forEach((v,i)=>inputs[i].value=v);by("wave-kind").value="sin";by("view").value="fixed";draw();};draw();
  }
  function inverse(){
    const a=by("angle"),choice=by("inverse-kind"),cv=by("canvas"),g=cv.getContext("2d");
    function draw(){
      const deg=Number(a.value),v=M.inverse(deg),kind=choice.value,principal=v[kind],p=circle(g,cv);
      by("angleLabel").textContent=deg+"°";
      by("original").textContent="sin θ = "+fmt(v.values.sin)+"; cos θ = "+fmt(v.values.cos);
      by("outputs").innerHTML=["sin","cos","tan"].map(name=>"<p><strong>arc"+name+"("+name+" θ)</strong> = "+
        (v[name]===null?"undefined (the original tangent is undefined)":fmt(v[name])+"°")+"</p>").join("");
      const low=kind==="cos"?0:-Math.PI/2,high=kind==="cos"?Math.PI:Math.PI/2;
      g.strokeStyle="#26865d";g.lineWidth=8;g.beginPath();g.arc(p.ox,p.oy,p.r, -high,-low);g.stroke();
      const t=deg*Math.PI/180;
      line(g,[p.ox,p.oy],[p.X(Math.cos(t)),p.Y(Math.sin(t))],"#b97424",7);
      point(g,p.X(Math.cos(t)),p.Y(Math.sin(t)),"#b97424",7);
      if(principal!==null){
        const u=principal*Math.PI/180;
        line(g,[p.ox,p.oy],[p.X(Math.cos(u)),p.Y(Math.sin(u))],"#26865d",3);
        point(g,p.X(Math.cos(u)),p.Y(Math.sin(u)),"#26865d",4);
      }
      if(kind==="tan"){
        for(const t of [-Math.PI/2,Math.PI/2]){
          g.fillStyle="white";g.strokeStyle="#26865d";g.lineWidth=2;g.beginPath();g.arc(p.X(Math.cos(t)),p.Y(Math.sin(t)),6,0,2*Math.PI);g.fill();g.stroke();
        }
      }
      by("branch-note").textContent=kind==="cos"?"Arccosine chooses angles in [0°, 180°].":
        kind==="sin"?"Arcsine chooses angles in [−90°, 90°].":"Arctangent chooses angles strictly between −90° and 90°.";
      by("comparison").textContent=principal===null?"The original tangent has a zero denominator. There is no inverse-composition output at this angle.":
        Math.abs(principal-deg)<1e-7?"The original angle is in the selected principal range, so it is recovered unchanged.":
        "Original angle "+deg+"°; principal angle "+fmt(principal)+"°. Both have the same "+kind+" value.";
    }
    a.addEventListener("input",draw);choice.addEventListener("change",draw);draw();
  }
  const mode=document.body.dataset.explorer;
  if(mode==="six")six();else if(mode==="wave")wave();else if(mode==="inverse")inverse();
})();
