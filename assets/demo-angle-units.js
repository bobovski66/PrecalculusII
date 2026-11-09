/* Dual-unit angle entries supplement (but do not replace) the original demo controls. */
(()=>{const specs={
'unit_circle.html':[['angle','Rotation angle','deg']],
'circle_to_wave.html':[['angle','Rotation angle','deg']],
'six_trig_functions.html':[['angle','Unit-circle angle','deg']],
'inverse_trig.html':[['angle','Original angle','deg']],
'polar_complex.html':[['a','Angle of z','deg'],['b','Angle of w','deg']],
'motion_synthesis.html':[['angle','Rotation per step','deg']],
'sinusoid_explorer.html':[['c','Horizontal shift','rad']],
'conic_explorer.html':[],
'vector_explorer.html':[],
'trig_equations.html':[],
'sequence_explorer.html':[]
};const name=location.pathname.split('/').pop(),items=specs[name]||[],root=document.querySelector('.demo-controls');if(!root)return;
function displayNumber(n){return Number(n.toFixed(4)).toString()}
for(const [id,title,unit] of items){let slider=document.getElementById(id);if(!slider)continue;let card=document.createElement('div');card.className='angle-unit-tools';let header=document.createElement('strong');header.textContent=title+' — degrees and radians';let row=document.createElement('div');row.className='angle-unit-row';const make=(label)=>{let l=document.createElement('label');l.textContent=label;let input=document.createElement('input');input.type='number';input.step='any';input.setAttribute('aria-label',title+' in '+label.toLowerCase());l.append(input);row.append(l);return input};let degrees=make('Degrees (°)'),radians=make('Radians (rad)');let help=document.createElement('small');help.textContent='Enter the angle in either unit, or drag the slider.';card.append(header,row,help);slider.insertAdjacentElement('afterend',card);
const sync=()=>{let value=Number(slider.value),d=unit==='deg'?value:value*180/Math.PI,r=unit==='rad'?value:value*Math.PI/180;if(document.activeElement!==degrees)degrees.value=displayNumber(d);if(document.activeElement!==radians)radians.value=displayNumber(r)};
function apply(v){if(!Number.isFinite(v))return;slider.value=String(Math.max(Number(slider.min||-Infinity),Math.min(Number(slider.max||Infinity),v)));slider.dispatchEvent(new Event('input',{bubbles:true}));slider.dispatchEvent(new Event('change',{bubbles:true}));sync()}
const entered=input=>input.value.trim()===''?NaN:Number(input.value);const fromDegrees=()=>apply(unit==='deg'?entered(degrees):entered(degrees)*Math.PI/180),fromRadians=()=>apply(unit==='rad'?entered(radians):entered(radians)*180/Math.PI);for(const event of ['input','change']){degrees.addEventListener(event,fromDegrees);radians.addEventListener(event,fromRadians);}slider.addEventListener('input',sync);sync();
let previous=slider.value;setInterval(()=>{if(slider.value!==previous){previous=slider.value;sync()}},250);
}
if(!items.length && ['vector_explorer.html','trig_equations.html','conic_explorer.html'].includes(name)){let p=document.createElement('p');p.className='muted';p.textContent=name==='trig_equations.html'?'Angle conversion: 180° = π rad. Solutions are measured in radians.':name==='conic_explorer.html'?'For angular parameterizations, 2π radians = 360°.':'Vector direction: 180° = π radians. Both units describe the same geometric angle.';root.append(p)}
})();
