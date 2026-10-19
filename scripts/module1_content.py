"""One content source for the Module 1 web reading and printed chapter."""
def figure(name,alt,caption):
    return f'<figure><img src="../assets/module1/{name}.svg" alt="{alt}" loading="lazy"><figcaption>{caption}</figcaption></figure>'
def example(title,body):return f'<div class="example"><h3>{title}</h3>{body}</div>'
def aside(title,body):return f'<aside class="note"><h3>{title}</h3>{body}</aside>'
SECTIONS=[]
def section(id,title,body,question,answer):SECTIONS.append(dict(id=id,title=title,body=body,question=question,answer=answer))
section('coordinates','Read a point before describing a turn',r'''
<p>Imagine a marker on the rim of a turning wheel. We want to describe where the marker is, how far it has traveled, and how quickly it moves. These are different questions. Trigonometry connects them by treating an angle as a record of turning.</p>
<p>Begin with a coordinate plane. The origin is the point where the axes meet. In an ordered pair \((x,y)\), the first number tells us horizontal position and the second tells us vertical position. Positive \(x\) means right; negative \(x\) means left. Positive \(y\) means above the horizontal axis; negative \(y\) means below it.</p>
'''+figure('coordinate-prerequisite','A right triangle from the origin to (4,3), with horizontal leg 4, vertical leg 3, and hypotenuse 5.','The coordinates describe two perpendicular moves. The distance from the origin is the hypotenuse.')+example('A point and its distance from the origin',r'''
<p>For \(P=(4,3)\), the Pythagorean theorem gives the distance \(r\) from the origin:</p>
\[r^2=4^2+3^2=25,\qquad r=5.\]
<p>If we shrink this triangle until its hypotenuse is 1, every length is divided by 5. The new point is \((4/5,3/5)\). It points in the same direction as \((4,3)\), but lies on a circle of radius 1. This process is called <em>normalizing</em> the coordinates.</p>''')+r'''
<p>We will use fractions and square roots to describe some positions exactly. An expression such as \(\sqrt2/2\) is an exact number. Its decimal approximation, about 0.707, is useful for estimating, but the rounded decimal loses some information. Both forms will appear in this module.</p>
<p>As you read, keep a sketch beside your calculations. A positive vertical coordinate should put the point above the horizontal axis; a distance should never be negative. These simple checks can catch many errors.</p>''',r'A point is at \((-3,4)\). Find its distance from the origin and divide both coordinates by that distance. Which signs should remain?',r'The distance is \(\sqrt{(-3)^2+4^2}=5\). The normalized point is \((-3/5,4/5)\). It stays left of the vertical axis and above the horizontal axis.')
section('rotation','An angle records a signed rotation',r'''
<p>An angle describes how a ray turns around its endpoint. A ray is a line that starts at one point and extends in one direction. In <em>standard position</em>, the endpoint is the origin and the starting ray points right along the positive \(x\)-axis. The final ray is called the <em>terminal ray</em>.</p>
<p>We use a sign to record the direction of turning. Counterclockwise turns are positive; clockwise turns are negative. A complete turn is \(360^\circ\), a half-turn is \(180^\circ\), and a quarter-turn is \(90^\circ\). The Greek letter \(\theta\), pronounced “theta,” often stands for an angle.</p>
'''+figure('signed-rotation','Two circles compare a positive 60-degree counterclockwise turn with a negative 60-degree clockwise turn.','Begin at the positive horizontal axis. The sign tells you which way to turn.')+example('Read the whole rotation',r'''
<p>For \(420^\circ\), turn counterclockwise through one full revolution and then another \(60^\circ\):</p>
\[420^\circ=360^\circ+60^\circ.\]
<p>For \(-120^\circ\), turn clockwise through \(120^\circ\). The terminal ray points down and left. You could reach that same ray by turning counterclockwise through \(240^\circ\), but the two descriptions record different journeys.</p>''')+r'''
<p>A diagram usually shows the final direction more easily than it shows several complete turns. Do not assume that an angle must be between zero and one revolution. A wheel may turn many times, and a negative angle is a perfectly valid description of motion.</p>''',r'Where do \(-90^\circ\) and \(450^\circ\) end? Describe the direction and amount of turning for each.',r'\(-90^\circ\) is one quarter-turn clockwise and ends on the negative \(y\)-axis. \(450^\circ\) is one full turn plus a quarter-turn counterclockwise and ends on the positive \(y\)-axis.')
section('radians','Radians compare an arc with a radius',r'''
<p>Degrees divide a full turn into 360 equal pieces. Radians measure the same turning in a way tied directly to the circle. An <em>arc</em> is a curved part of a circle. For a central angle, the two rays meet at the circle’s center and cut off an arc on its circumference.</p>
<p>Take the length of that arc and divide by the radius, using the same length units for both. The ratio is the angle’s magnitude in radians:</p>
\[\boxed{\theta=\frac{s}{r}}\qquad\text{(radian measure)}.\]
<p>An angle of 1 radian cuts off an arc whose length equals the radius. It is a little less than \(60^\circ\): about \(57.3^\circ\). A radian is an angle unit; it is not another name for \(\pi\).</p>
'''+figure('one-radian','A circle has two radii bounding a one-radian sector; its green arc has the same length as a radius.','One radian means one radius-length of arc.')+r'''
<p>Why does the size of the circle not change the angle? If you double the radius while keeping the same two rays, the arc also doubles. The ratio \(s/r\) stays the same. The picture below shows this for an angle of \(\pi/3\) radians.</p>
'''+figure('same-angle-two-radii','Concentric circles of radii 1.5 and 3 share a 60-degree central angle, with arcs of lengths pi/2 and pi.','Angle describes turning. Radius describes size. The ratio of arc length to radius separates these ideas.')+example('Why one turn is 2π radians',r'''
<p>A circle’s circumference is \(2\pi r\). For a complete turn, divide the full circumference by the radius:</p>
\[\theta=\frac{2\pi r}{r}=2\pi.\]
<p>Thus \(360^\circ=2\pi\) radians and \(180^\circ=\pi\) radians. The number \(\pi\) is about 3.14159. A half-turn has radian measure \(\pi\) because its arc has length \(\pi r\).</p>''')+r'''
<p>For clockwise motion, use a negative angle. If \(s\) means ordinary arc length, it is nonnegative and \(s/r\) gives the angle’s magnitude. A signed angle requires an orientation as well. We will keep signed arc length and distance traveled separate.</p>''',r'An arc is 9 cm long on a circle of radius 6 cm. What is the angle’s magnitude in radians? At the same angle on a circle of radius 12 cm, how long is the arc?',r'The angle is \(9/6=1.5\) radians. Doubling the radius doubles the arc, so the new arc is 18 cm. The angle remains 1.5 radians.')
section('conversion','Convert units without changing the angle',r'''
<p>The relation \(180^\circ=\pi\) radians lets us write the same angle in either unit. To convert, multiply by a fraction that equals 1 and cancels the unwanted unit.</p>
\[\text{Degrees to radians: multiply by }\frac{\pi\text{ rad}}{180^\circ}.\]
\[\text{Radians to degrees: multiply by }\frac{180^\circ}{\pi\text{ rad}}.\]
'''+example('Degrees to radians: 240°',r'''
\[240^\circ\cdot\frac{\pi\text{ rad}}{180^\circ}=\frac{240\pi}{180}\text{ rad}=\frac{4\pi}{3}\text{ rad}.\]
<p>The degree units cancel. Before calculating, we know that \(240^\circ\) is between a half-turn and a full turn. Our result, \(4\pi/3\), is between \(\pi\) and \(2\pi\), as expected.</p>''')+example('Radians to degrees: −5π/3',r'''
\[\left(-\frac{5\pi}{3}\text{ rad}\right)\frac{180^\circ}{\pi\text{ rad}}=-\frac{5(180^\circ)}{3}=-300^\circ.\]
<p>The \(\pi\) factors and radian units cancel. Keep the negative sign: changing units does not change the direction of rotation.</p>''')+figure('turn-fractions','Four circles show quarter, half, three-quarter, and full turns with their degree and radian measures.','A fraction of a full turn is the same fraction of 360° or of 2π radians.')+r'''
<table><thead><tr><th>Degrees</th><th>Radians</th><th>Fraction of one turn</th></tr></thead><tbody><tr><td>\(30^\circ\)</td><td>\(\pi/6\)</td><td>\(1/12\)</td></tr><tr><td>\(45^\circ\)</td><td>\(\pi/4\)</td><td>\(1/8\)</td></tr><tr><td>\(60^\circ\)</td><td>\(\pi/3\)</td><td>\(1/6\)</td></tr><tr><td>\(90^\circ\)</td><td>\(\pi/2\)</td><td>\(1/4\)</td></tr><tr><td>\(180^\circ\)</td><td>\(\pi\)</td><td>\(1/2\)</td></tr><tr><td>\(270^\circ\)</td><td>\(3\pi/2\)</td><td>\(3/4\)</td></tr><tr><td>\(360^\circ\)</td><td>\(2\pi\)</td><td>1</td></tr></tbody></table>
<p>Leave an answer such as \(4\pi/3\) exact unless a decimal is requested. To estimate it, use the calculator’s \(\pi\) key and round at the end. Replacing \(\pi\) by 3.14 too early can add avoidable error.</p>
'''+aside('Check the calculator’s angle mode',r'<p>In degree mode, \(\sin(30)=1/2\). In radian mode, the same turn is entered as \(\sin(\pi/6)=1/2\). Typing 30 in radian mode means 30 radians, a very different angle. Converting an angle and changing the calculator mode are separate actions.</p>'),r'Convert \(72^\circ\) to radians and \(7\pi/5\) radians to degrees. Check each result against one full turn.',r'\(72(\pi/180)=2\pi/5\) radians, one fifth of a turn. \((7\pi/5)(180/\pi)=252^\circ\), seven tenths of a turn.')
section('coterminal','Same final direction, different journeys',r'''
<p>Two angles are <em>coterminal</em> when they have the same starting and terminal rays. Adding or subtracting a full turn changes the amount of rotation without changing the final direction.</p>
\[\theta+360^\circ k\quad\text{or}\quad\theta+2\pi k,\qquad k\in\mathbb Z.\]
<p>The symbol \(\mathbb Z\) means the integers: \(\ldots,-2,-1,0,1,2,\ldots\). Choose the formula that matches your angle unit. For example, \(60^\circ\), \(420^\circ\), and \(-300^\circ\) all end on the same ray.</p>
'''+figure('coterminal-rotations','The terminal rays for 60, 420, and negative 300 degrees coincide although the recorded rotations differ.','A terminal ray does not tell us how many turns happened along the way.')+example('Find a representative between 0 and 2π',r'''
<p>Start with \(-13\pi/4\). A full turn is \(2\pi=8\pi/4\), so add full turns using a common denominator:</p>
\[-\frac{13\pi}{4}+\frac{8\pi}{4}=-\frac{5\pi}{4},\qquad -\frac{5\pi}{4}+\frac{8\pi}{4}=\frac{3\pi}{4}.\]
<p>Now \(0\leq3\pi/4&lt;2\pi\). The terminal ray is in the upper-left part of the plane. We added two full turns; the original clockwise rotation was not erased from its physical history.</p>''')+r'''
<p>The interval \([0,2\pi)\) includes 0 and excludes \(2\pi\). Those two angles point in the same direction, so including both would repeat a representative. Similarly, use \([0^\circ,360^\circ)\) for a single representative in degrees.</p>
<p>For the final point on a circle, a coterminal angle is enough. For distance traveled, use the actual rotation. A marker turning through \(420^\circ\) travels seven times as far as one turning through \(60^\circ\) on the same circle.</p>''',r'Find the angle in \([0^\circ,360^\circ)\) coterminal with \(870^\circ\). How many full turns did you set aside?',r'\(870^\circ-2(360^\circ)=150^\circ\). We set aside two full turns. The original rotation was two turns plus \(150^\circ\).')
section('arc-length','Arc length, distance, and displacement',r'''
<p>The equation \(\theta=s/r\) can be rearranged to find arc length. When \(\theta\) is a signed angle in radians, \(r\theta\) gives a <em>directed</em> arc length:</p>
\[s_{\text{directed}}=r\theta.\]
<p>If the motion proceeds in one direction without reversing, the distance traveled is</p>
\[\boxed{\text{distance}=r|\theta|}.\]
<p>The absolute-value bars remove the sign. A clockwise journey still covers a positive distance. If motion reverses, calculate the distance for each part and add those distances. The final net angle alone will not tell you the whole distance.</p>
'''+figure('arc-and-chord','A green curved arc and an orange straight chord join the same endpoints of a circle.','Distance along the rim follows the arc. Displacement compares the starting and ending positions directly.')+example('A clockwise turn on a radius-6 circle',r'''
<p>A point turns clockwise through \(120^\circ\) on a circle of radius 6 cm. Convert first:</p>
\[\theta=-120^\circ\frac{\pi}{180^\circ}=-\frac{2\pi}{3}\text{ rad}.\]
<p>Then the directed arc is \(6(-2\pi/3)=-4\pi\) cm, while the distance traveled is \(4\pi\) cm, about 12.57 cm. The negative directed arc records clockwise orientation; it is not a negative distance.</p>''')+aside('Why radians are required',r'<p>For a quarter-turn, \(\theta=\pi/2\), so the arc is \(r\pi/2\), one quarter of \(2\pi r\). Putting 90 directly into \(r\theta\) would give \(90r\), which is much larger than the whole circumference. Convert degrees before multiplying.</p>')+r'''
<p><em>Displacement</em> is the change in position from the start to the finish. Its magnitude is the straight-line distance between the endpoints, not the arc length. After one complete revolution, a point has traveled a whole circumference but has zero displacement.</p>''',r'A point on a circle of radius 2 m moves clockwise through half a turn. Find the signed angle, distance traveled, and magnitude of displacement.',r'The angle is \(-\pi\) radians. Distance is \(2|{-\pi}|=2\pi\) m. The endpoints are opposite ends of a diameter, so the displacement has magnitude 4 m.')
section('speed','Angular velocity and tangential speed',r'''
<p>Angular velocity describes the rate at which the angle changes. Over a time interval of length \(\Delta t\), the average angular velocity is</p>
\[\omega=\frac{\Delta\theta}{\Delta t}.\]
<p>The Greek letter \(\omega\) is “omega,” and \(\Delta\) means “change in.” With angles in radians and time in seconds, the units are radians per second, written rad/s. Counterclockwise angular velocity is positive; clockwise angular velocity is negative. Angular <em>speed</em> is the nonnegative magnitude \(|\omega|\).</p>
<p>For uniform rotation, the rate is constant. A point farther from the center travels a longer arc during the same turn, so its tangential speed is greater:</p>
\[\boxed{v=r|\omega|}.\]
'''+figure('angular-and-tangential-speed','Two circles with radii 2 and 4 meters turn through the same 30 degrees in 2 seconds; the outer point travels twice as fast.','The angular speed is shared by the whole wheel. Tangential speed depends on distance from the axis.')+example('Convert revolutions per minute',r'''
<p>A disk makes 6 counterclockwise revolutions per minute. A marker sits 0.5 m from the axis. Convert the angular rate one unit at a time:</p>
\[6\frac{\text{rev}}{\text{min}}\cdot\frac{2\pi\text{ rad}}{1\text{ rev}}\cdot\frac{1\text{ min}}{60\text{ s}}=\frac{\pi}{5}\text{ rad/s}.\]
<p>The revolutions and minutes cancel. The marker’s tangential speed is \(v=0.5(\pi/5)=\pi/10\) m/s, about 0.314 m/s. A marker twice as far from the axis would move twice as fast.</p>''')+r'''
<p>The <em>period</em> \(T\) is the time needed for one complete revolution. For uniform rotation, angular speed is \(2\pi/T\). If the rotation is counterclockwise, \(\omega=2\pi/T\); if clockwise, \(\omega=-2\pi/T\). A smaller period means a faster rotation.</p>
<p>Average speed and instantaneous speed agree here because the rotation rate is constant. If the wheel speeds up and slows down, one average rate describes only the chosen interval.</p>''',r'A wheel of radius 2 m makes one counterclockwise revolution every 20 seconds. Find its angular speed and tangential speed.',r'Angular speed is \(2\pi/20=\pi/10\) rad/s. Tangential speed is \(2(\pi/10)=\pi/5\) m/s. The units distinguish turning rate from distance rate.')
section('unit-circle','Sine and cosine are coordinates',r'''
<p>The <em>unit circle</em> has center \((0,0)\) and radius 1. Start at \((1,0)\) and turn through angle \(\theta\). The coordinates of the resulting point define two functions:</p>
\[\boxed{P=(\cos\theta,\sin\theta)}.\]
<p>Cosine is the horizontal coordinate. Sine is the vertical coordinate. The expression \(\sin\theta\) means “the sine of the angle \(\theta\),” not “sin multiplied by theta.” A function takes an input and assigns an output; here the input is an angle and the output is a coordinate.</p>
'''+figure('unit-circle-coordinates','A point on a unit circle has blue horizontal coordinate cosine theta and green vertical coordinate sine theta.','Keep the coordinate order: cosine first, sine second.')+r'''
<p>The familiar right-triangle ratios are built into this definition. In the first quadrant, the triangle has hypotenuse 1, adjacent side \(x\), and opposite side \(y\). Thus \(\cos\theta=x/1=x\) and \(\sin\theta=y/1=y\). The circle definition also handles angles beyond a right triangle, including negative angles and multiple turns.</p>
<p>Since every unit-circle point satisfies \(x^2+y^2=1\), its coordinates satisfy</p>
\[\boxed{\cos^2\theta+\sin^2\theta=1}.\]
<p>The notation \(\cos^2\theta\) means \((\cos\theta)^2\). Both coordinates lie between \(-1\) and 1. These are useful checks on calculated values.</p>
'''+figure('radius-scaling','Two circles are drawn at the same scale; the radius-3 point has coordinates three times those on the unit circle.','Changing the radius changes the physical coordinates, while sine and cosine of the angle stay the same.')+example('Scale from a unit circle to a real wheel',r'''
<p>If a point at angle \(\theta\) has unit-circle coordinates \((3/5,4/5)\), a point at that angle on a radius-5 circle has coordinates \((3,4)\). In general, on a circle centered at the origin:</p>
\[x=r\cos\theta,\qquad y=r\sin\theta.\]
<p>These are physical coordinates. Dividing them by the radius recovers the unit-circle coordinates. The radius does not change the angle’s sine or cosine.</p>'''),r'The unit-circle point at an angle is \((-3/5,-4/5)\). What is the corresponding point on a circle of radius 10 centered at the origin?',r'Multiply both coordinates by 10: \((-6,-8)\). Its distance from the origin is \(\sqrt{36+64}=10\), and both signs remain negative.')
section('exact-values','Derive exact values from two triangles',r'''
<p>You do not need a separate rule for every special angle. Two right triangles supply the coordinate magnitudes for \(30^\circ\), \(45^\circ\), and \(60^\circ\). The Pythagorean theorem explains where the square roots come from.</p>
<h3>The 45° triangle</h3><p>A right triangle with equal legs has two equal acute angles, each \(45^\circ\). If each leg is 1, its hypotenuse is \(\sqrt{1^2+1^2}=\sqrt2\). Divide every side by \(\sqrt2\) to make the hypotenuse 1:</p>
\[\cos45^\circ=\sin45^\circ=\frac{1}{\sqrt2}=\frac{\sqrt2}{2}.\]
<p>The last equality comes from multiplying top and bottom by \(\sqrt2\). It changes the form of the number, not its value.</p>
'''+figure('triangle-45','A 45-45-90 right triangle has legs 1 and hypotenuse square root of 2.','Equal legs give equal horizontal and vertical coordinates after normalization.')+r'''
<h3>The 30° and 60° triangles</h3><p>Cut an equilateral triangle of side 2 into two equal right triangles. Each has hypotenuse 2, short leg 1, and long leg \(\sqrt{2^2-1^2}=\sqrt3\). The angles are \(30^\circ\), \(60^\circ\), and \(90^\circ\).</p>
'''+figure('triangle-30','An equilateral triangle of side 2 is split by its altitude into right triangles with legs 1 and square root of 3.','Halving an equilateral triangle produces the ratio 1 : √3 : 2.')+r'''
<p>At \(30^\circ\), the horizontal leg is \(\sqrt3\) and the vertical leg is 1. Divide by the hypotenuse 2 to get \((\sqrt3/2,1/2)\). At \(60^\circ\), the roles of the two legs switch.</p>
<table><thead><tr><th>Angle</th><th>Radians</th><th>Cosine: horizontal</th><th>Sine: vertical</th></tr></thead><tbody><tr><td>\(0^\circ\)</td><td>0</td><td>1</td><td>0</td></tr><tr><td>\(30^\circ\)</td><td>\(\pi/6\)</td><td>\(\sqrt3/2\)</td><td>\(1/2\)</td></tr><tr><td>\(45^\circ\)</td><td>\(\pi/4\)</td><td>\(\sqrt2/2\)</td><td>\(\sqrt2/2\)</td></tr><tr><td>\(60^\circ\)</td><td>\(\pi/3\)</td><td>\(1/2\)</td><td>\(\sqrt3/2\)</td></tr><tr><td>\(90^\circ\)</td><td>\(\pi/2\)</td><td>0</td><td>1</td></tr></tbody></table>
<p>The axis points at \(0^\circ\) and \(90^\circ\) come directly from the circle. They do not require a right triangle with a zero-length leg.</p>''',r'Why is \(\sin60^\circ\) greater than \(\sin30^\circ\)? Check that the two coordinates at \(45^\circ\) satisfy the unit-circle equation.',r'The point at \(60^\circ\) is higher: \(\sqrt3/2&gt;1/2\). At \(45^\circ\), \((\sqrt2/2)^2+(\sqrt2/2)^2=1/2+1/2=1\).')
section('reference','Use reference angles and quadrant signs',r'''
<p>The axes divide the plane into four open regions called <em>quadrants</em>. Number them counterclockwise, beginning with the upper-right region. A point on an axis belongs to none of the open quadrants.</p>
'''+figure('quadrant-signs','The four quadrants show the signs of sine and cosine; the axis points are labeled (1,0), (0,1), (-1,0), and (0,-1).','The signs follow from left/right and above/below. They are coordinate signs, not an extra rule to memorize.')+r'''
<p>For a terminal ray away from the axes, the <em>reference angle</em> is the acute angle between that ray and the horizontal axis. “Acute” means greater than \(0^\circ\) and less than \(90^\circ\). Always measure it to the horizontal axis, which may mean the negative \(x\)-axis.</p>
'''+figure('reference-angles','Angles 120, 225, and 300 degrees have reference angles 60, 45, and 60 degrees measured to the horizontal axis.','Use the reference triangle for magnitudes, then the quadrant for signs.')+example('Find the point at 120°',r'''
<p>First locate the angle: \(120^\circ\) is in Quadrant II. The reference angle is \(180^\circ-120^\circ=60^\circ\). At \(60^\circ\), the coordinate magnitudes are \(1/2\) and \(\sqrt3/2\). Quadrant II lies left and up, so</p>
\[(\cos120^\circ,\sin120^\circ)=\left(-\frac12,\frac{\sqrt3}{2}\right).\]
<p>The horizontal coordinate gets the minus sign. The vertical coordinate remains positive. Squaring and adding gives \(1/4+3/4=1\), as it should.</p>''')+r'''
<p>When the original angle includes several turns, first find a coterminal angle in one revolution. Then locate its quadrant and reference angle. For a point on an axis, read the coordinates directly: \((1,0)\), \((0,1)\), \((-1,0)\), or \((0,-1)\). No acute reference triangle is needed.</p>
<p>A useful routine is: locate the ray, find the acute reference angle, determine the two magnitudes, and assign each sign from the picture. Keep the order \((\cos\theta,\sin\theta)\).</p>''',r'Find the unit-circle point at \(300^\circ\). Does \(-60^\circ\) give the same point? Explain.',r'The reference angle is \(60^\circ\), and Quadrant IV is right and down. The point is \((1/2,-\sqrt3/2)\). Since \(-60^\circ+360^\circ=300^\circ\), the angles are coterminal and give the same point.')
section('waves','A moving coordinate traces a wave',r'''
<p>A point turning around a circle moves in two dimensions. We can also study one coordinate at a time. Make a graph whose horizontal axis is the angle \(\theta\), and whose vertical axis is the point’s vertical coordinate. That graph is \(y=\sin\theta\).</p>
<p>Be careful about the two pictures. On the circle, \(x\) and \(y\) describe physical position. On the graph of sine, the horizontal axis is the <em>angle input</em>; it is not the point’s horizontal position.</p>
<table><thead><tr><th>Angle</th><th>Point on the circle</th><th>Cosine</th><th>Sine</th></tr></thead><tbody><tr><td>0</td><td>\((1,0)\)</td><td>1</td><td>0</td></tr><tr><td>\(\pi/2\)</td><td>\((0,1)\)</td><td>0</td><td>1</td></tr><tr><td>\(\pi\)</td><td>\((-1,0)\)</td><td>−1</td><td>0</td></tr><tr><td>\(3\pi/2\)</td><td>\((0,-1)\)</td><td>0</td><td>−1</td></tr><tr><td>\(2\pi\)</td><td>\((1,0)\)</td><td>1</td><td>0</td></tr></tbody></table>
'''+figure('circle-to-wave','A rotating point is paired with sine and cosine graphs from zero to four pi radians; sine is green and cosine is blue.','One full turn produces one complete cycle of each coordinate graph.')+r'''
<p>Between these quarter turns, the point moves smoothly, so its coordinates change smoothly. Sine rises from 0 to 1, falls through 0 to −1, and returns to 0. Cosine begins at 1 because the starting point is \((1,0)\).</p>
<p>A function is <em>periodic</em> if its values repeat after a fixed change in input. Adding a complete turn returns the point to exactly the same position:</p>
\[\sin(\theta+2\pi)=\sin\theta,\qquad\cos(\theta+2\pi)=\cos\theta.\]
<p>The period of each is \(2\pi\). A half-turn is generally not a period: it moves a point to the opposite side of the circle and reverses both coordinates. For instance, cosine is 1 at 0 and −1 at \(\pi\).</p>
'''+aside('Explore the connection',r'<p>In Circle to Wave, stop at each quarter-turn and compare the point’s height with the sine graph. Then show two full turns. The playback speed changes how quickly the demonstration runs; the graph against angle keeps the same shape. A graph against time requires a rotation rate, which we introduce next.</p>'),r'Why does sine start at 0 while cosine starts at 1? How many complete cycles appear from 0 to \(4\pi\)?',r'The starting point is \((1,0)\), so the horizontal coordinate is 1 and the vertical coordinate is 0. The interval from 0 to \(4\pi\) contains two full turns and therefore two cycles.')
section('models','Build a model of height over time',r'''
<p>To describe a turning wheel over time, connect two steps: time determines an angle, and the angle determines a position. For uniform rotation starting at angle zero,</p>
\[\theta(t)=\omega t.\]
<p>Here \(t\) is elapsed time. The notation \(\theta(t)\) means the angle at time \(t\). If \(\omega\) is in rad/s and \(t\) is in seconds, their product is in radians.</p>
<p>For a wheel of radius \(r\), centered horizontally at 0 and vertically at height \(c\), with a rider starting at the rightmost point,</p>
\[\boxed{x(t)=r\cos(\omega t),\qquad h(t)=c+r\sin(\omega t)}.\]
<p>The sine term is vertical displacement from the center. Adding \(c\) gives height above ground. The radius stretches the unit-circle coordinate; it does not change the value of sine itself.</p>
'''+example('A radius-8 Ferris wheel',r'''
<p>A wheel has radius 8 m, center height 10 m, and period 40 s. The rider starts at the rightmost point, and the wheel turns counterclockwise. First find the angular velocity:</p>
\[\omega=\frac{2\pi}{40}=\frac{\pi}{20}\text{ rad/s}.\]
<p>Next substitute the radius, center height, and angular rate:</p>
\[x(t)=8\cos\left(\frac{\pi t}{20}\right),\qquad h(t)=10+8\sin\left(\frac{\pi t}{20}\right).\]
<p>At \(t=10\), the angle is \(\pi/2\), so the rider is at \((0,18)\). This is the top: the 10 m center height plus the 8 m radius. At \(t=30\), the angle is \(3\pi/2\), so the height is \(10-8=2\) m.</p>''')+figure('ferris-height','A height-time curve passes through (0,10), (10,18), (20,10), (30,2), and (40,10).','The horizontal axis now measures seconds. The physical assumptions determine where the cycle begins and how long it takes.')+r'''
<p>Check a model against the situation before trusting a calculated value. The initial height should be 10 m, the height should stay between 2 and 18 m, and one full cycle should take 40 seconds. A negative height would signal a problem with this physical setup.</p>
<p>If a rider begins at another angle \(\theta_0\), use \(\theta(t)=\theta_0+\omega t\) inside the coordinate formulas. For clockwise rotation, use a negative \(\omega\). Starting position and direction matter; the radius and period alone do not determine a unique height formula.</p>
<p>This is the connection we will develop further: circular motion gives coordinate functions, and those functions let us model repeating behavior.</p>''',r'In the example, what is the height at 20 seconds? If the radius became 12 m but the center stayed 10 m high, what would the model predict at the bottom?',r'At 20 seconds, \(\theta=\pi\), so \(h=10\) m. A radius of 12 m with the same center would predict a bottom height of \(10-12=-2\) m. A wheel meant to stay above ground would need a higher center or a different physical setup.')

FORMULAS=r'''
<table><thead><tr><th>Question</th><th>Relationship</th><th>What to check</th></tr></thead><tbody>
<tr><td>How much turning?</td><td>\(180^\circ=\pi\text{ rad}\)</td><td>Keep the sign; match the unit.</td></tr>
<tr><td>Same terminal ray?</td><td>\(\theta+2\pi k\), \(k\in\mathbb Z\)</td><td>Use full turns, not half-turns.</td></tr>
<tr><td>How far along the rim?</td><td>\(d=r|\theta|\)</td><td>Radians; one direction without reversing.</td></tr>
<tr><td>How fast is the turning?</td><td>\(\omega=\Delta\theta/\Delta t\)</td><td>Signed rate, such as rad/s.</td></tr>
<tr><td>How fast is the rim point?</td><td>\(v=r|\omega|\)</td><td>Distance/time, such as m/s.</td></tr>
<tr><td>Where is the unit-circle point?</td><td>\((\cos\theta,\sin\theta)\)</td><td>Horizontal first; check signs.</td></tr>
<tr><td>Where is the radius-\(r\) point?</td><td>\((r\cos\theta,r\sin\theta)\)</td><td>Center at the origin.</td></tr>
<tr><td>Height on a wheel?</td><td>\(h=c+r\sin(\omega t)\)</td><td>Rightmost start, constant rotation rate.</td></tr>
</tbody></table>'''
TRY_SOLUTIONS=[
r'All three terminal rays coincide. \(-120^\circ+360^\circ=240^\circ\), and \(600^\circ-360^\circ=240^\circ\). They point down and left, although the signed rotations differ.',
r'\(225^\circ(\pi/180^\circ)=5\pi/4\) radians, in Quadrant III. \((-\pi/3)(180^\circ/\pi)=-60^\circ\), in Quadrant IV.',
r'One revolution is \(2\pi\) radians, so angular speed is \(2\pi/40=\pi/20\) rad/s. Tangential speed is \(12(\pi/20)=3\pi/5\) m/s, about 1.885 m/s.',
r'Convert \(135^\circ=3\pi/4\) radians. Arc length is \(0.6(3\pi/4)=9\pi/20\) m. Average angular speed is \((3\pi/4)/3=\pi/4\) rad/s. Average tangential speed is \((9\pi/20)/3=3\pi/20\) m/s, assuming the turn proceeds in one direction.',
r'At \(150^\circ\), the point is \((-\sqrt3/2,1/2)\). At \(330^\circ\), it is \((\sqrt3/2,-1/2)\). Corresponding coordinates have equal absolute values, and both signs are opposite.',
r'The direction is not specified, so state an assumption. For counterclockwise rotation, \(\omega=2\pi/30=\pi/15\), \(x(t)=6\cos(\pi t/15)\), and \(h(t)=7+6\sin(\pi t/15)\). At 7.5 s the angle is \(\pi/2\), so the height is 13 m. Clockwise rotation would instead put the rider at height 1 m at that time.'
]
REVIEW_SOLUTIONS=[
r'\(-135^\circ=-3\pi/4\) radians; \(300^\circ=5\pi/3\) radians. Multiply each degree value by \(\pi/180\).',
r'\(11\pi/6=330^\circ\); \(-5\pi/4=-225^\circ\). Multiply each radian value by \(180/\pi\).',
r'\(19\pi/6-2\pi=19\pi/6-12\pi/6=7\pi/6\), which is in \([0,2\pi)\).',
r'\(s=8(5\pi/12)=10\pi/3\) cm. The angle is already in radians.',
r'\(33\frac13=100/3\) rev/min. Multiply by \(2\pi\) rad/rev and divide by 60 s/min to get \(10\pi/9\) rad/s.',
r'They are coordinates on a radius-1 circle centered at the origin. No such point can be farther than 1 unit horizontally or vertically from the origin.',
r'At \(2\pi/3\): \((-1/2,\sqrt3/2)\). At \(5\pi/4\): \((-\sqrt2/2,-\sqrt2/2)\). At \(11\pi/6\): \((\sqrt3/2,-1/2)\). Use the reference angle for magnitudes and the quadrant for signs.',
r'\(x=10\cos\theta\), \(y=12+10\sin\theta\). The center adds 12 to the vertical coordinate; the radius multiplies both unit-circle coordinates.',
r'\(-7\pi/6+2\pi=5\pi/6\). The point is \((-\sqrt3/2,1/2)\), in Quadrant II.',
r'In 120 seconds the wheel turns through \(18\pi\) radians, or \(3240^\circ\). Divide each by 120: the angular speed is \(3\pi/20\) rad/s, or \(27^\circ\)/s.',
r'\(75^\circ=5\pi/12\) radians, so the arc is \(4(5\pi/12)=5\pi/3\) m, approximately 5.24 m.',
r'The point is \((0,-1)\), on the negative \(y\)-axis. Open quadrants exclude their boundary axes, so it belongs to none of them.',
r'The radius would increase from 8 to 12 m, increasing the amplitude of each coordinate function to 12. The period remains 40 s and the center height remains 10 m. The predicted height range becomes \([-2,22]\) m; a wheel staying above ground would require a higher center.'
]
