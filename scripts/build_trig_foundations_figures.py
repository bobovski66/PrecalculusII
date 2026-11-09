"""Scaled diagrams for Modules 2–4, shared by their HTML and PDF readings."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc

OUT=Path(__file__).resolve().parents[1]/"assets/learning"
OUT.mkdir(parents=True,exist_ok=True)
B,G,O,I="#28678b","#26865d","#b97424","#193044"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,
 "text.color":I,"axes.labelcolor":I,"svg.hashsalt":"math142-foundations",
 "axes.spines.top":False,"axes.spines.right":False,"savefig.facecolor":"white"})
BUILT=[]
def save(name,fig):
    fig.tight_layout(pad=1.7)
    fig.savefig(OUT/(name+".svg"),bbox_inches="tight",pad_inches=.14,metadata={"Date":None})
    fig.savefig(OUT/(name+".pdf"),bbox_inches="tight",pad_inches=.14,metadata={"CreationDate":None,"ModDate":None})
    plt.close(fig);BUILT.append(name)
def plane(ax,lim=1.4):
    ax.set_aspect("equal");ax.set(xlim=(-lim,lim),ylim=(-lim,lim))
    ax.axhline(0,color="#b8c7d0",lw=.8);ax.axvline(0,color="#b8c7d0",lw=.8)
    ax.set_xlabel("x");ax.set_ylabel("y",rotation=0);ax.grid(alpha=.12)
def arrow(ax,p,q,color=B):
    ax.annotate("",q,p,arrowprops={"arrowstyle":"->","color":color,"lw":2.3})
def angle_axis(ax):
    ax.set_xticks(np.arange(5)*np.pi/2,["0","π/2","π","3π/2","2π"])
    ax.set_xlabel("Angle (radians)");ax.grid(alpha=.15)

def make():
    fig,axs=plt.subplots(1,2,figsize=(8.5,3.8),gridspec_kw={"width_ratios":[1.15,1]})
    ax=axs[0];plane(ax);ax.add_patch(Circle((0,0),1,fill=False,color=B,lw=2))
    x,y=.5,np.sqrt(3)/2;arrow(ax,(0,0),(x,y),O)
    ax.plot([0,x],[0,0],color=B,lw=4);ax.plot([x,x],[0,y],color=G,lw=3)
    ax.text(.1,-.18,"cos 60° = 1/2",color=B,fontsize=10)
    ax.text(.62,.38,"sin 60°\n= √3/2",color=G,fontsize=10)
    ax.text(-.22,.26,"60°",fontsize=10);ax.set_title("One unit-circle point")
    ax=axs[1];ax.axis("off")
    for j,txt in enumerate(["sin = √3/2","cos = 1/2","tan = (√3/2)/(1/2) = √3",
                           "csc = 2/√3","sec = 2","cot = 1/√3"]):
        ax.text(.04,.94-j*.15,txt,fontsize=12,color=B if j<3 else G,transform=ax.transAxes)
    save("m02-coordinate-ratios",fig)

    fig,axs=plt.subplots(1,2,figsize=(8.2,4))
    for ax,d in zip(axs,[30,150]):
        plane(ax,1.55);ax.add_patch(Circle((0,0),1,fill=False,color=B))
        a=np.deg2rad(d);xx=np.linspace(-1.35,1.35,100)
        ax.plot(xx,np.tan(a)*xx,"--",color="#9caebc")
        arrow(ax,(0,0),(np.cos(a),np.sin(a)),O)
        ax.axvline(1,color=G,lw=1.5);ax.plot(1,np.tan(a),"o",color=G)
        ax.text(.95,1.35,"x = 1",ha="right",color=G,fontsize=10)
        ax.text(-1.35,-1.3,"tan = "+("√3/3" if d==30 else "−√3/3"),fontsize=11)
        ax.set_title(f"Angle {d}°")
    save("m02-tangent-slope",fig)

    fig,axs=plt.subplots(1,2,figsize=(8.4,3.9))
    for ax,k in zip(axs,[1,2]):
        a,b=4*k,3*k;ax.plot([0,a,a,0],[0,0,b,0],color=B,lw=2)
        ax.plot([a-.35,a-.35,a],[0,.35,.35],color=I)
        ax.text(a/2,-.55,str(a),ha="center");ax.text(a+.25,b/2,str(b))
        ax.text(a/2-.5,b/2+.4,str(5*k));ax.text(1,.22,"θ",fontsize=13)
        ax.set_aspect("equal");ax.set(xlim=(-.6,9),ylim=(-1,7));ax.axis("off")
        ax.set_title(f"sin θ = {b}/{5*k} = 3/5",fontsize=12)
    save("m02-similar-triangles",fig)

    fig,axs=plt.subplots(1,2,figsize=(9,3.9))
    t=np.linspace(-.35,2*np.pi+.35,2400)
    for ax,fn,name,recip,poles in [(axs[0],np.cos,"cos","sec",[np.pi/2,3*np.pi/2]),
                                  (axs[1],np.sin,"sin","csc",[0,np.pi,2*np.pi])]:
        v=fn(t);inv=np.full_like(v,np.nan)
        np.divide(1,v,out=inv,where=np.abs(v)>1/3.2)
        ax.plot(t,v,color=B,lw=2,label=name+" θ")
        ax.plot(t,inv,color=G,lw=2,label=recip+" θ")
        for p in poles:ax.axvline(p,color=O,ls="--",lw=1)
        ax.axhline(0,color="#becbd4",lw=.7);angle_axis(ax);ax.set(ylim=(-3.3,3.3),ylabel="Output")
        ax.legend(loc="upper center",ncol=2,fontsize=10);ax.set_title("Coordinate and reciprocal")
    save("m02-reciprocal-graphs",fig)

    fig,ax=plt.subplots(figsize=(7.3,4.4));run=20;eye=1.6;rise=run*np.tan(np.deg2rad(40))
    ax.plot([-2,23],[0,0],color=I);ax.plot([run,run],[0,eye+rise],color=G,lw=3)
    ax.plot([0,run],[eye,eye+rise],color=B,lw=2)
    ax.plot([0,run],[eye,eye],"--",color="#98aebc");ax.plot([0,0],[0,eye],color=O,lw=3)
    ax.text(8,-1.1,"20 m horizontally",ha="center");ax.text(5,2.5,"40°",color=B)
    ax.text(-2.6,3.4,"Eyes:\n1.6 m",fontsize=10)
    ax.text(20.6,9,"rise above\neye level",color=G,fontsize=10)
    ax.set_aspect("equal");ax.set(xlim=(-4,25),ylim=(-2,21));ax.axis("off")
    save("m02-height-measurement",fig)

    fig,axs=plt.subplots(1,2,figsize=(9.2,3.8),gridspec_kw={"width_ratios":[1,1.7]})
    ax=axs[0];plane(ax);ax.add_patch(Circle((0,0),1,fill=False,color=B))
    a=np.pi/3;arrow(ax,(0,0),(np.cos(a),np.sin(a)),O)
    ax.plot([np.cos(a),np.cos(a)],[0,np.sin(a)],color=G,lw=3);ax.set_title("Follow the height")
    ax=axs[1];t=np.linspace(0,2*np.pi,500)
    ax.plot(t,np.sin(t),color=G,label="sin: height",lw=2)
    ax.plot(t,np.cos(t),color=B,label="cos: horizontal",lw=2)
    ax.plot(a,np.sin(a),"o",color=O);angle_axis(ax);ax.set(ylim=(-1.25,1.4),ylabel="Coordinate");ax.legend(fontsize=10)
    save("m03-circle-wave",fig)

    fig,ax=plt.subplots(figsize=(8,4));t=np.linspace(0,2*np.pi,500)
    ax.plot(t,3*np.sin(t)-2,color=B,lw=2.5)
    for y in [-5,-2,1]:ax.axhline(y,color=O if y==-2 else "#b8c7d1",ls="--",lw=1)
    ax.annotate("",(np.pi/2,1),(np.pi/2,-2),arrowprops={"arrowstyle":"<->","color":G,"lw":2})
    ax.text(np.pi/2+.13,-.5,"amplitude 3",color=G)
    ax.text(4.5,-1.6,"midline −2",color=O)
    angle_axis(ax);ax.set(ylim=(-6,2),ylabel="y",yticks=[-5,-2,1],title="y = 3 sin x − 2")
    save("m03-amplitude-midline",fig)

    fig,axs=plt.subplots(3,1,figsize=(8,6),sharex=True)
    t=np.linspace(0,2*np.pi,1200)
    for ax,n,lab in zip(axs,[1,2,4],["2π","π","π/2"]):
        ax.plot(t,np.sin(n*t),color=B,lw=2);ax.set(ylim=(-1.3,1.3),ylabel="Output")
        ax.set_title(f"sin({'' if n==1 else n}x): period {lab}",fontsize=11)
        angle_axis(ax)
    save("m03-period-comparison",fig)

    fig,axs=plt.subplots(2,1,figsize=(8,4.8),sharex=True);t=np.linspace(-.5,5,700)
    for ax,c,title in zip(axs,[1,.5],["sin(2(x − 1)): shift 1","sin(2x − 1) = sin(2(x − 1/2)): shift 1/2"]):
        ax.plot(t,np.sin(2*(t-c)),color=B,lw=2)
        ax.axhline(0,color="#9dafbc");ax.axvline(c,color=O,ls="--")
        ax.plot(c,0,"o",color=G);ax.set(title=title,ylim=(-1.3,1.3),ylabel="Output");ax.grid(alpha=.15)
    axs[-1].set_xlabel("x");save("m03-phase-shifts",fig)

    fig,axs=plt.subplots(1,2,figsize=(9.2,3.9),gridspec_kw={"width_ratios":[1,1.7]})
    ax=axs[0];ax.add_patch(Circle((0,11),9,fill=False,color=B,lw=2));ax.axhline(0,color=I)
    ax.plot(9,11,"o",color=O);ax.plot([0,9],[11,11],color=G,lw=2)
    ax.text(0,21,"One turn: 30 s",ha="center");ax.text(2,12,"radius 9 m",fontsize=10)
    ax.text(0,-1.8,"center height 11 m",ha="center",fontsize=10)
    ax.set_aspect("equal");ax.set(xlim=(-11,12),ylim=(-3,23));ax.axis("off")
    ax=axs[1];t=np.linspace(0,30,500);ax.plot(t,11+9*np.sin(np.pi*t/15),color=B,lw=2)
    tt=np.array([0,7.5,15,22.5,30]);yy=11+9*np.sin(np.pi*tt/15)
    ax.plot(tt,yy,"o",color=O);ax.axhline(11,color=G,ls="--");ax.grid(alpha=.15)
    ax.set(xlabel="Time (s)",ylabel="Height above ground (m)",ylim=(0,23),xticks=tt,yticks=[2,11,20])
    save("m03-wheel-model",fig)

    fig,ax=plt.subplots(figsize=(8,3.9));t=np.linspace(-2*np.pi,2*np.pi,1100)
    ax.plot(t,np.sin(t),color="#abbcc7",lw=2);u=np.linspace(-np.pi/2,np.pi/2,350)
    ax.plot(u,np.sin(u),color=G,lw=3.5)
    ax.axhline(.5,color=O,ls="--")
    for a in [np.pi/6,5*np.pi/6]:ax.plot(a,.5,"o",color=O)
    ax.axvspan(-np.pi/2,np.pi/2,color=G,alpha=.06)
    ax.set_xticks(np.arange(-4,5)*np.pi/2,["−2π","−3π/2","−π","−π/2","0","π/2","π","3π/2","2π"])
    ax.set(xlabel="Angle (radians)",ylabel="Sine value",ylim=(-1.25,1.4))
    ax.text(-1.3,1.16,"chosen inverse-sine branch",color=G,fontsize=11)
    ax.grid(alpha=.12);save("m04-principal-branch",fig)

    fig,ax=plt.subplots(figsize=(6,4.9));plane(ax,1.9);u=np.linspace(-np.pi/2,np.pi/2,400)
    ax.plot(u,np.sin(u),color=B,lw=2.5,label="restricted sine")
    ax.plot(np.sin(u),u,color=G,lw=2.5,label="arcsine")
    ax.plot([-1.8,1.8],[-1.8,1.8],"--",color=O,label="y = x")
    ax.plot(np.pi/6,.5,"o",color=B);ax.plot(.5,np.pi/6,"o",color=G)
    ax.legend(loc="upper left",fontsize=10);save("m04-inverse-reflection",fig)

    fig,ax=plt.subplots(figsize=(6.5,4.3));plane(ax);ax.add_patch(Circle((0,0),1,fill=False,color=B,lw=2))
    ax.axhline(.5,color=O,ls="--")
    for a,col in [(np.pi/6,G),(5*np.pi/6,B)]:
        arrow(ax,(0,0),(np.cos(a),.5),col);ax.plot(np.cos(a),.5,"o",color=col)
        ax.text(1.12*np.cos(a),.66,"30° chosen" if col==G else "150° original",ha="center",color=col,fontsize=10)
    ax.set_title("Same sine: 1/2");save("m04-shared-sine",fig)

    fig,axs=plt.subplots(1,2,figsize=(8.8,3.8))
    for ax,x,y,h,title in [(axs[0],4,3,5,"arctan(3/4): an acute angle"),
                            (axs[1],12,-5,13,"arcsin(−5/13): a negative angle")]:
        ax.plot([0,x,x,0],[0,0,y,0],color=B,lw=2)
        ax.text(x/2,.4 if y<0 else -.6,str(x),ha="center")
        ax.text(x+.25,y/2,str(abs(y)));ax.text(x/2-1,y/2+(.5 if y>0 else -.8),str(h))
        ax.text(x*.15,.2 if y>0 else -.8,"θ")
        ax.set_aspect("equal");ax.axis("off");ax.set_title(title,fontsize=11)
        ax.set(xlim=(-1,x+2),ylim=(min(y,0)-1.6,max(y,0)+1.6))
    save("m04-composition-triangle",fig)

    fig,ax=plt.subplots(figsize=(6.8,4.8));plane(ax,1.35);ax.add_patch(Circle((0,0),1,fill=False,color="#b8c9d5"))
    alpha,beta=np.deg2rad([30,45])
    h=np.cos(beta)*np.array([np.cos(alpha),np.sin(alpha)])
    v=np.sin(beta)*np.array([-np.sin(alpha),np.cos(alpha)])
    point=h+v
    arrow(ax,(0,0),h,B);arrow(ax,h,point,G);arrow(ax,(0,0),point,O)
    ax.text(.55,.12,"horizontal\ncontribution",color=B,fontsize=10,ha="center")
    ax.text(.7,.75,"vertical\ncontribution",color=G,fontsize=10)
    ax.text(-.13,1.2,"final angle: 30° + 45° = 75°",color=O,fontsize=11,ha="center")
    ax.plot(point[0],point[1],"o",color=O)
    save("m04-rotation-addition",fig)
    print(f"Built {len(BUILT)} SVG/PDF diagram pairs for Modules 2–4.")

if __name__=="__main__":make()
