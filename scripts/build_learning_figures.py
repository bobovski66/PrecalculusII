"""Exact, reproducible figures for the expanded Precalculus II readings."""
from pathlib import Path
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/learning"
OUT.mkdir(parents=True, exist_ok=True)
BLUE, GREEN, GOLD, INK = "#28678b", "#26865d", "#b97424", "#193044"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
    "svg.hashsalt": "math142-expanded", "text.color": INK, "axes.labelcolor": INK,
    "axes.spines.top": False, "axes.spines.right": False, "savefig.facecolor": "white"})

def save(name, fig):
    fig.tight_layout(pad=1.5)
    fig.savefig(OUT / (name + ".svg"), bbox_inches="tight", metadata={"Date": None})
    fig.savefig(OUT / (name + ".pdf"), bbox_inches="tight",
                metadata={"CreationDate": None, "ModDate": None})
    plt.close(fig)

def plane(ax, x=(-1.5, 1.5), y=None):
    ax.set_aspect("equal")
    ax.set_xlim(*x)
    ax.set_ylim(*(y or x))
    ax.axhline(0, color="#aab8c2", lw=.8)
    ax.axvline(0, color="#aab8c2", lw=.8)
    ax.set_xlabel("x")
    ax.set_ylabel("y", rotation=0)
    ax.grid(alpha=.13)

def arrow(ax, start, end, color=BLUE, label=None, offset=(0, 9)):
    ax.annotate("", end, start, arrowprops={"arrowstyle": "->", "lw": 2.5, "color": color})
    if label:
        mid = (np.asarray(start) + np.asarray(end)) / 2
        ax.annotate(label, mid, xytext=offset, textcoords="offset points",
                    color=color, ha="center", fontsize=10)

def wave(ax, freq=1, target=.5):
    t = np.linspace(0, 2*np.pi, 1200)
    ax.plot(t, np.sin(freq*t), color=BLUE, lw=2)
    ax.axhline(target, color=GOLD, ls="--")
    roots = [(u + 2*k*np.pi)/freq for k in range(freq)
             for u in (np.arcsin(target), np.pi-np.arcsin(target))]
    ax.plot(roots, [target]*len(roots), "o", color=GOLD)
    ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi], ["0","π/2","π","3π/2","2π"])
    ax.set(xlabel="Angle x (radians)", ylabel="Output", ylim=(-1.3,1.35))
    ax.grid(alpha=.15)

def make():
    fig, axs = plt.subplots(1,2,figsize=(9,3.9),gridspec_kw={"width_ratios":[1,1.6]})
    ax=axs[0]; plane(ax); ax.add_patch(Circle((0,0),1,fill=False,color=BLUE,lw=2))
    ax.axhline(.5,color=GOLD,ls="--")
    for a,lab in [(np.pi/6,"π/6"),(5*np.pi/6,"5π/6")]:
        p=(np.cos(a),np.sin(a));arrow(ax,(0,0),p,GREEN)
        ax.annotate(lab,p,xytext=(0,12),textcoords="offset points",ha="center")
    ax.set_title("sin x = 1/2");wave(axs[1]);axs[1].set_title("Two angles in one turn")
    save("m05-circle-solutions",fig)

    fig,axs=plt.subplots(2,1,figsize=(8,5.2),sharex=True)
    for ax,n in zip(axs,[1,2]):wave(ax,n);ax.set_title(f"sin({'' if n==1 else n}x) = 1/2: {2*n} intersections",fontsize=12)
    save("m05-frequency",fig)

    fig,ax=plt.subplots(figsize=(7,3.8));A=np.array([0,0]);B=np.array([8,0]);C=np.array([3,4])
    ax.plot([0,8,3,0],[0,0,4,0],color=BLUE,lw=2);ax.plot([3,3],[0,4],ls="--",color=GREEN)
    for p,l,off in [(A,"A",(0,-18)),(B,"B",(0,-18)),(C,"C",(0,12))]:
        ax.annotate(l,p,xytext=off,textcoords="offset points",ha="center")
    ax.text(1,2.2,"b",fontsize=14);ax.text(5.7,2.3,"a",fontsize=14)
    ax.text(3.2,1.7,"h = b sin A\n   = a sin B",color=GREEN)
    ax.set_aspect("equal");ax.axis("off");ax.set(xlim=(-.7,8.7),ylim=(-.7,4.8))
    save("m05-sine-law",fig)

    fig,axs=plt.subplots(1,2,figsize=(9,3.7))
    cpt=np.array([8*np.cos(np.pi/6),4])
    for ax,bx,lab in zip(axs,[cpt[0]+3,cpt[0]-3],["B ≈ 53.13°","B ≈ 126.87°"]):
        ax.plot([0,bx,cpt[0],0],[0,0,4,0],color=BLUE,lw=2)
        ax.text(1,.3,"A = 30°",fontsize=10);ax.text(cpt[0]/2-1.1,2.4,"b = 8",fontsize=10)
        ax.text((bx+cpt[0])/2+.2,2,"a = 5",fontsize=10)
        ax.text(bx,-.5,"B",ha="center");ax.text(cpt[0],4.3,"C",ha="center")
        ax.set_title(lab);ax.set_aspect("equal");ax.axis("off");ax.set(xlim=(-.7,11),ylim=(-1,5))
    save("m05-ssa",fig)

    fig,ax=plt.subplots(figsize=(6,4));plane(ax,(-1,8),(-1,10))
    ax.plot([0,6,6],[0,0,8],color=GREEN,lw=2.5)
    arrow(ax,(0,0),(6,8),BLUE,"displacement: 10 km",(-32,10))
    ax.text(3,-.65,"6 km east",ha="center");ax.text(6.3,4,"8 km north")
    ax.set_title("Route length: 6 + 8 = 14 km")
    save("m06-displacement",fig)

    fig,axs=plt.subplots(1,2,figsize=(8.5,4))
    for ax in axs:plane(ax,(-3,5),(-1,7))
    u=np.array([3,4]);v=np.array([-2,1])
    arrow(axs[0],(0,0),u,BLUE,"u");arrow(axs[0],u,u+v,GOLD,"v")
    arrow(axs[0],(0,0),u+v,GREEN,"u + v",(-35,0))
    axs[0].set_title("Head to tail")
    arrow(axs[1],(0,0),u,BLUE,"u");arrow(axs[1],(0,0),v,GOLD,"v",(-5,9))
    arrow(axs[1],v,u,GREEN,"u − v",(15,8))
    axs[1].set_title("Difference joins endpoints")
    save("m06-addition",fig)

    fig,axs=plt.subplots(1,3,figsize=(9,3.4))
    for ax,d in zip(axs,[45,90,135]):
        plane(ax,(-1.6,1.6));ax.set_xticks([]);ax.set_yticks([])
        arrow(ax,(0,0),(1.2,0),BLUE);arrow(ax,(0,0),(1.2*np.cos(np.deg2rad(d)),1.2*np.sin(np.deg2rad(d))),GREEN)
        ax.set_title(f"{d}°: dot product "+("positive" if d<90 else "zero" if d==90 else "negative"),fontsize=10)
    save("m06-alignment",fig)

    fig,ax=plt.subplots(figsize=(6,4));plane(ax,(-.7,5),(-.7,4.7))
    ax.plot([0,4.5],[0,4.5],color="#bac9d3");arrow(ax,(0,0),(4,3),BLUE,"u = (4, 3)")
    arrow(ax,(0,0),(3.5,3.5),GREEN,"projection",(0,18))
    ax.plot([3.5,4],[3.5,3],"--",color=GOLD,lw=2);ax.text(3.9,3.6,"remainder",fontsize=10)
    save("m06-projection",fig)

    fig,axs=plt.subplots(1,2,figsize=(8,3.8))
    point=np.array([1,np.sqrt(3)])
    for ax in axs:plane(ax,(-2.6,2.6));ax.plot(*point,"o",color=GOLD)
    arrow(axs[0],(0,0),point,BLUE);axs[0].set_title("(2, 60°)")
    axs[1].plot([0,-1.2],[0,-1.2*np.sqrt(3)],"--",color="#8c9ca8")
    arrow(axs[1],(0,0),point,GREEN);axs[1].set_title("(−2, 240°): reverse the ray")
    save("m07-polar-addresses",fig)

    fig,ax=plt.subplots(figsize=(6,4.2));plane(ax,(-1,7),(-1,7))
    arrow(ax,(0,0),(np.sqrt(3),1),BLUE,"z: length 2",(-25,8))
    arrow(ax,(0,0),(0,6),GREEN)
    ax.text(.25,3.1,"zw: length 6",color=GREEN)
    ax.text(2.1,4,"w: scale by 3\nand turn by 60°",color=GOLD)
    ax.set_xlabel("Real part");ax.set_ylabel("Imaginary part",rotation=90)
    save("m07-multiplication",fig)

    fig,axs=plt.subplots(1,2,figsize=(8,3.8))
    for ax,n in zip(axs,[3,4]):
        plane(ax);ax.add_patch(Circle((0,0),1,fill=False,color="#c4d1d9"))
        t=np.arange(n)*2*np.pi/n;ax.plot(np.cos(t),np.sin(t),"o",color=GOLD,ms=8)
        for k,a in enumerate(t):ax.text(1.22*np.cos(a),1.22*np.sin(a),f"{round(k*360/n)}°",ha="center",va="center",fontsize=10)
        ax.set_title(f"{n} roots of 1");ax.set_xticks([]);ax.set_yticks([])
    save("m07-roots",fig)

    fig,ax=plt.subplots(figsize=(6,4));plane(ax,(-.4,2.5),(-1.4,1.4))
    t=np.linspace(0,np.pi,400);r=2*np.cos(t);ax.plot(r*np.cos(t),r*np.sin(t),color=BLUE,lw=2)
    for a in [0,np.pi/4,np.pi/2,3*np.pi/4,np.pi]:
        rr=2*np.cos(a);ax.plot(rr*np.cos(a),rr*np.sin(a),"o",color=GOLD)
    ax.plot(1,0,"+",color=GREEN,ms=12);ax.set_title("r = 2 cos θ: center (1, 0), radius 1")
    save("m07-polar-curve",fig)

    fig,axs=plt.subplots(1,2,figsize=(8,3.7))
    t=np.linspace(0,2*np.pi,400)
    for ax,b in zip(axs,[1,2]):
        plane(ax);ax.plot(np.cos(t),np.sin(t),color="#b6c9d5")
        a=b*np.pi/4;arrow(ax,(0,0),(np.cos(a),np.sin(a)),BLUE)
        ax.plot(np.cos(a),np.sin(a),"o",color=GOLD)
        ax.set_title(f"(cos {'t' if b==1 else '2t'}, sin {'t' if b==1 else '2t'}) at t = π/4",fontsize=11)
    save("m08-timing",fig)

    fig,ax=plt.subplots(figsize=(7,3.7));t=np.linspace(0,100/49,300)
    ax.plot(10*np.sqrt(3)*t,10*t-4.9*t*t,color=BLUE,lw=2)
    tt=np.arange(0,2.01,.25);ax.plot(10*np.sqrt(3)*tt,10*tt-4.9*tt*tt,"o",color=GOLD)
    ax.set(xlabel="Horizontal position (m)",ylabel="Height (m)",ylim=(0,6))
    ax.set_title("Markers every 0.25 seconds");ax.grid(alpha=.15)
    save("m08-projectile",fig)

    fig,ax=plt.subplots(figsize=(7,4));plane(ax,(-6,6),(-4,4))
    ax.add_patch(Ellipse((0,0),10,6,fill=False,color=BLUE,lw=2))
    p=np.array([0,3]);ax.plot([-4,4],[0,0],"o",color=GOLD)
    for x in [-4,4]:ax.plot([x,p[0]],[0,p[1]],color=GREEN,lw=2)
    ax.text(-2.5,1.7,"5",color=GREEN);ax.text(2.4,1.7,"5",color=GREEN)
    ax.text(-4,-.65,"focus (−4, 0)",ha="center",fontsize=9);ax.text(4,-.65,"focus (4, 0)",ha="center",fontsize=9)
    ax.set_title("Ellipse: focal distances add to 10")
    save("m08-ellipse",fig)

    fig,ax=plt.subplots(figsize=(6,4.5));plane(ax,(-6,6),(-3.5,6))
    x=np.linspace(-5.8,5.8,400);ax.plot(x,x*x/8,color=BLUE,lw=2)
    ax.axhline(-2,color=GOLD,ls="--");ax.plot(0,2,"o",color=GOLD)
    p=(4,2);ax.plot(*p,"o",color=GREEN)
    ax.plot([0,4],[2,2],color=GREEN,lw=2);ax.plot([4,4],[-2,2],color=GREEN,lw=2)
    ax.text(.2,2.3,"focus");ax.text(-5.7,-2.7,"directrix y = −2",color=GOLD)
    ax.text(1.7,2.25,"4");ax.text(4.25,0,"4");ax.set_title("x² = 8y: equal distances")
    save("m08-parabola",fig)

    fig,ax=plt.subplots(figsize=(7,4.2));plane(ax,(-9,9),(-9,9))
    xx=np.linspace(3,9,400);yy=4*np.sqrt(xx*xx/9-1)
    for sx in [-1,1]:
        for sy in [-1,1]:ax.plot(sx*xx,sy*yy,color=BLUE)
    xx=np.linspace(-9,9,100)
    for sy in [-1,1]:ax.plot(xx,sy*4*xx/3,"--",color=GREEN,lw=1)
    ax.plot([-3,3],[0,0],"o",color=BLUE);ax.plot([-5,5],[0,0],"o",color=GOLD)
    ax.set_title("x²/9 − y²/16 = 1");save("m08-hyperbola",fig)

    fig,axs=plt.subplots(1,2,figsize=(8,3.7));n=np.arange(1,7);a=3+2*(n-1)
    for ax,y,title in zip(axs,[a,np.cumsum(a)],["Individual terms aₙ","Running totals Sₙ"]):
        ax.bar(n,y,color=BLUE if title.startswith("Individual") else GREEN,width=.6)
        ax.set(xlabel="Index n",ylabel="Value",title=title,xticks=n);ax.grid(axis="y",alpha=.15)
    save("m09-terms-sums",fig)

    fig,axs=plt.subplots(1,2,figsize=(9,3.8));n=np.arange(1,16);a=5*.6**(n-1)
    axs[0].plot(n,a,"o-",color=BLUE);axs[0].set(title="Terms: aₙ = 5(0.6)ⁿ⁻¹",ylabel="Term")
    axs[1].plot(n,np.cumsum(a),"o-",color=GREEN);axs[1].axhline(12.5,color=GOLD,ls="--",label="Limit 12.5")
    axs[1].set(title="Partial sums approach 12.5",ylabel="Total");axs[1].legend()
    for ax in axs:ax.set_xlabel("Number of terms n");ax.grid(alpha=.15)
    save("m09-geometric-limit",fig)

    fig,axs=plt.subplots(1,2,figsize=(8.7,3.8));n=np.arange(1,9);a=6-6*.5**(n-1)
    axs[0].plot(n,a,"o-",color=BLUE);axs[0].axhline(6,color=GOLD,ls="--");axs[0].set(title="aₙ approaches 6",ylabel="Value")
    axs[1].bar(n,6-a,color=GREEN);axs[1].set(title="Gap: 6 − aₙ",ylabel="Distance to equilibrium")
    for ax in axs:ax.set_xlabel("Index n");ax.grid(axis="y",alpha=.15)
    save("m09-feedback",fig)

    fig,axs=plt.subplots(1,2,figsize=(9,3.8),gridspec_kw={"width_ratios":[1,1.5]})
    ax=axs[0];plane(ax,(-6,6));ax.add_patch(Circle((0,0),5,fill=False,color=BLUE))
    a=np.pi/3;arrow(ax,(0,0),(5*np.cos(a),5*np.sin(a)),GREEN)
    ax.set_title("Radius 5 m")
    t=np.linspace(0,40,500);axs[1].plot(t,5*np.cos(np.pi*t/10),color=BLUE,label="x(t)")
    axs[1].plot(t,5*np.sin(np.pi*t/10),color=GREEN,label="y(t)")
    axs[1].set(xlabel="Time (s)",ylabel="Coordinate (m)",xticks=[0,10,20,30,40]);axs[1].legend();axs[1].grid(alpha=.15)
    save("m10-one-motion",fig)

    fig,axs=plt.subplots(1,2,figsize=(8,3.7))
    for ax,step,title in zip(axs,[np.pi/2,np.pi],["Every 5 s: four positions","Every 10 s: two positions"]):
        plane(ax,(-6,6));ax.add_patch(Circle((0,0),5,fill=False,color="#c4d1d9"))
        t=np.arange(5)*step;ax.plot(5*np.cos(t),5*np.sin(t),"o",color=GOLD,ms=8)
        ax.set_title(title,fontsize=11)
    save("m10-sampling",fig)

    fig,axs=plt.subplots(1,3,figsize=(10,3.6))
    for ax,rho in zip(axs,[1,.8,1.08]):
        n=np.arange(21);z=3*(rho*np.exp(1j*np.pi/2))**n;lim=max(4,float(np.max(abs(z)))*1.2)
        plane(ax,(-lim,lim));ax.plot(z.real,z.imag,"o-",color=BLUE,ms=3)
        if rho==1:ax.add_patch(Circle((0,0),3,fill=False,color="#bac9d3",ls="--",lw=1))
        ax.set_title(f"Scale ρ = {rho}",fontsize=12);ax.set_xticks([]);ax.set_yticks([])
    save("m10-spirals",fig)

    fig,ax=plt.subplots(figsize=(5,4));plane(ax,(-.4,1.6),(-.4,1.6))
    points=[(0,0),(1,0),(1,1),(0,1),(0,0)]
    for a,b,label in zip(points,points[1:],["1","i","−1","−i"]):arrow(ax,a,b,BLUE,label,(0,10))
    ax.set_title("Four step vectors: total displacement 0");save("m10-displacements",fig)
    print(f"Built {len(list(OUT.glob('*.svg')))} SVG/PDF diagram pairs.")

if __name__ == "__main__":
    make()
