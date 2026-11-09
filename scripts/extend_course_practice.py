"""Add transfer questions without changing the indices of saved earlier quiz answers."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
EXTRA={
5:[
["A signal is sin(πt/4). During 0 ≤ t < 8 seconds, when is the signal 1?",
 ["t = 1 only","t = 2 only","t = 2 and 6","t = 4 only"],1,
 "Find when the inside angle first reaches π/2. Check the full period.",
 "The period is 8 s, and the maximum occurs once, at t = 2 s."],
["A triangle has A = 30°, a = 6 cm, and B = 90°. What is side b?",
 ["3 cm","6 cm","9 cm","12 cm"],3,
 "Pair each side with its opposite sine.",
 "b/sin90° = 6/sin30°, so b = 12 cm."]
],
6:[
["A cart moves 4 m east under a constant force ⟨8,6⟩ N. How much work is done?",
 ["24 J","32 J","40 J","56 J"],1,
 "The displacement is ⟨4,0⟩. Take the dot product.",
 "Work is 8(4) + 6(0) = 32 J."],
["What is the projection of ⟨6,2⟩ onto the horizontal direction ⟨1,0⟩?",
 ["⟨0,2⟩","⟨6,2⟩","⟨6,0⟩","⟨1,0⟩"],2,
 "Keep the part parallel to the horizontal axis.",
 "The horizontal component gives the projection ⟨6,0⟩."]
],
7:[
["What are the arguments of the two square roots of 4i on [0°,360°)?",
 ["45° and 225°","90° and 270°","45° and 135°","0° and 180°"],0,
 "The argument of 4i is 90°. Add 360° before dividing to obtain the second root.",
 "The angles are 90°/2 = 45° and (90° + 360°)/2 = 225°."],
["A complex factor scales lengths by 1/2 and rotates 90° counterclockwise. Which factor is it?",
 ["2i","−i/2","1/2 + i","i/2"],3,
 "Its modulus must be 1/2 and its argument must be 90°.",
 "i/2 has the required modulus and direction."]
],
8:[
["For x = 2 + 3cos t, y = −1 + 3sin t, the curve is:",
 ["A radius-3 circle centered at (2,−1)","A radius-9 circle centered at (2,−1)",
 "A radius-3 circle centered at (−2,1)","An ellipse with different semiaxes"],0,
 "Subtract each center coordinate, then square and add.",
 "(x−2)² + (y+1)² = 9, so the center is (2,−1) and radius is 3."],
["What part of x = 4cos t, y = 3sin t is traced for 0 ≤ t ≤ π?",
 ["The full ellipse","The lower half","The upper half","Only the right half"],2,
 "Sine is nonnegative on that parameter interval.",
 "The y coordinate stays nonnegative, from the right vertex through the top to the left vertex."]
],
9:[
["A theater has 12 rows, starting with 10 seats and adding 2 per row. How many seats in all?",
 ["32","120","252","264"],2,
 "Find the last row, then average the first and last counts and multiply by 12.",
 "The last row has 32 seats; the total is 12(10 + 32)/2 = 252."],
["For a₁ = 2 and aₙ₊₁ = (aₙ + 10)/2, what happens to the gap 10 − aₙ?",
 ["It increases by 2","It halves each step","It stays fixed","It becomes zero after two steps"],1,
 "Subtract the recurrence from 10 and simplify.",
 "10 − aₙ₊₁ = (10 − aₙ)/2, so each remaining gap is half the preceding gap."]
],
10:[
["A wheel turns once every 12 s. Photos are taken every 12 s from t = 0. What do the photos show?",
 ["Every point on the circle","Two alternating positions","The same position each time","An outward spiral"],2,
 "Compare the observation interval with the period.",
 "Each photograph follows one whole revolution, so the sampled position repeats immediately."],
["A nonzero point is multiplied by 0.9i each step. Which description fits?",
 ["Quarter-turns with shrinking radii","Quarter-turns with fixed radii",
 "Half-turns with shrinking radii","No rotation and increasing radii"],0,
 "Read the modulus and argument of the multiplier.",
 "The factor has modulus 0.9 and argument 90°, so radii shrink and directions advance a quarter-turn."]
]}

def build():
    for n,extra in EXTRA.items():
        p=ROOT/f"quizzes/week{n:02}_quiz.html";s=p.read_text()
        start=s.index("const Q=")+len("const Q=")
        questions,end=json.JSONDecoder().raw_decode(s[start:])
        questions=questions[:10]+extra
        if n==10:
            questions[5][0]="If zₙ₊₁ = izₙ, where z₀ ≠ 0, after how many steps does it first return?"
        s=s[:start]+json.dumps(questions,ensure_ascii=False,separators=(",",":"))+s[start+end:]
        p.write_text(s)
    print("Added two transfer questions to each of Modules 5–10.")

if __name__=="__main__": build()
