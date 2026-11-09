"""Build the three foundation explorers with the course resource navigation."""
from pathlib import Path
from build_course_learning import head,masthead,footer

ROOT=Path(__file__).resolve().parents[1]

def shell(n,title,mode,controls,visual,questions):
    scripts=('<link rel="stylesheet" href="../assets/foundations-demos.css">'
      '<script defer src="../assets/foundations-math.js"></script>'
      '<script defer src="../assets/foundations-demos.js"></script>'
      '<script defer src="../assets/demo-angle-units.js"></script>')
    page=head(title,scripts).replace("<body>",f'<body data-explorer="{mode}">')+masthead(n,title)
    page+='<main id="main" class="demo-main"><div class="explorer-layout"><section class="panel explorer-controls demo-controls">'+controls+'</section><section class="explorer-visual">'+visual+'</section></div>'
    page+='<section class="panel guide-list"><h2>Investigate</h2><ol>'+''.join('<li>'+q+'</li>' for q in questions)+'</ol></section></main>'+footer()
    return page

def build():
    controls='''<p>Start with a unit-circle point. Its two coordinates determine the four additional ratios.</p>
<label for="angle">Angle θ: <output id="angleOut">30°</output></label>
<input type="range" min="0" max="360" value="30" step="1" id="angle">
<div class="readout"><h2>Coordinates</h2><p id="coords"></p><p id="quad"></p></div>
<div class="readout"><h2>Six values</h2><div id="values"></div><p class="exact-note">Decimal values are rounded to three places. Use special triangles for exact forms.</p></div>
<p id="denominator-note" class="readout" role="status"></p>'''
    visual='''<canvas id="graph" width="850" height="540" role="img" aria-label="Unit circle showing signed horizontal and vertical coordinates, a terminal line, and its tangent-line intersection"></canvas>
<p class="small" id="tangent-note" role="status"></p>
<p class="small">The dashed line extends through the origin in both directions. This allows its intersection with x = 1 to remain meaningful when the point lies on the left.</p>
<p><a href="reciprocal_trig_graphs.html">Compare reciprocal graphs</a> · <a href="trig_graphs.html">Explore all six graphs</a></p>'''
    questions=[
      "Set the angle to 60°. Calculate tangent from the two displayed coordinates before reading its value.",
      "Compare 120° and 240°. Which coordinate signs change, and which function signs change?",
      "At 90°, identify each zero denominator. Explain why tangent is undefined while cotangent is zero.",
      "Compare 89° and 91°. Describe the tangent-line intersection and the sign of its height."
    ]
    (ROOT/"demos/six_trig_functions.html").write_text(shell(2,"Six Trigonometric Functions","six",controls,visual,questions))

    controls='''<p>Change one parameter at a time. The fixed horizontal axes make translations visible; cycle view helps inspect a single period.</p>
<label for="wave-kind">Wave function</label><select id="wave-kind"><option value="sin">Sine</option><option value="cos">Cosine</option></select>
<label for="a">Amplitude coefficient A: <output id="ao"></output></label><input id="a" type="range" min="-5" max="5" step=".25" value="2">
<label for="b">Frequency coefficient B: <output id="bo"></output></label><input id="b" type="range" min=".25" max="5" step=".25" value="1">
<label for="c">Horizontal shift C: <output id="co"></output></label><input id="c" type="range" min="-6" max="6" step=".25" value="0">
<label for="d">Vertical shift D: <output id="do"></output></label><input id="d" type="range" min="-5" max="5" step=".25" value="0">
<label for="view">Horizontal viewing window</label><select id="view"><option value="fixed">Fixed axes: −2π to 2π</option><option value="cycle">Focus on one cycle</option></select>
<button id="reset">Reset parameters</button>
<div class="readout"><strong id="equation"></strong><p id="properties" role="status"></p></div>'''
    visual='''<canvas id="graph" width="1000" height="560" role="img" aria-label="Transformed sine or cosine graph with numerical axes, a dashed midline, and five landmark points"></canvas>
<p class="small">Orange points mark a cycle beginning at x = C. Points outside the selected window appear in the table below. The vertical axis remains centered on zero and expands when needed.</p>
<section class="panel"><h2>Five cycle landmarks</h2><div id="landmarks"></div></section>'''
    questions=[
      "Keep fixed axes and compare C = 0, 1, and −1. Follow one peak as the curve moves.",
      "Compare A = 4 with A = −4. Explain what happens at the first quarter-cycle landmark.",
      "Compare B = 1, 2, and 4 on the same horizontal axes. Then use cycle view to check each period.",
      "Set A = 0. Explain why the constant graph has no least positive period.",
      "Choose cosine with A = −2, B = 1, C = 0, D = 3. Predict the first three landmark heights."
    ]
    (ROOT/"demos/sinusoid_explorer.html").write_text(shell(3,"Sinusoid Explorer","wave",controls,visual,questions))

    controls='''<p>Keep the original angle, then compare it with the angle selected by an inverse trig function.</p>
<label for="angle">Original angle θ: <output id="angleLabel"></output></label><input id="angle" type="range" min="-360" max="360" step="1" value="150">
<label for="inverse-kind">Inverse shown on the circle</label><select id="inverse-kind"><option value="sin">Arcsine</option><option value="cos">Arccosine</option><option value="tan">Arctangent</option></select>
<div class="readout"><h2>Original ratios</h2><p id="original"></p></div>
<div class="readout"><h2>All principal outputs</h2><div id="outputs"></div></div>
<p id="branch-note" class="readout"></p>'''
    visual='''<canvas id="canvas" width="850" height="540" role="img" aria-label="Unit circle showing the principal angle range in green and comparing original and selected angle rays"></canvas>
<p class="small">Orange ray: original angle. Green ray: principal output. The green arc marks the output range; open endpoints for arctangent are excluded.</p>
<section class="panel"><p id="comparison" role="status"></p></section>
<p><a href="inverse_trig_graphs.html">Explore the inverse graphs and their reflected branches</a></p>'''
    questions=[
      "At 150°, compare arcsine with arccosine. Explain which principal range contains the original angle.",
      "Compare original angles 30° and 150°. Which sine information is shared, and which coordinate distinguishes them?",
      "At −120°, read all three outputs and justify their quadrants.",
      "At 90°, explain why arcsine and arccosine are defined but the tangent composition is undefined.",
      "Find an angle outside each selected range that produces a different principal angle."
    ]
    (ROOT/"demos/inverse_trig.html").write_text(shell(4,"Inverse Trigonometry Explorer","inverse",controls,visual,questions))
    print("Built the Module 2–4 explorers.")

if __name__=="__main__":build()
