"""Reproducible, mathematically scaled SVG/PDF figures for Module 1."""
from pathlib import Path
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch
OUT=Path(__file__).resolve().parents[1]/'assets/module1'
OUT.mkdir(parents=True,exist_ok=True)
B,G,O,I='#28678b','#26865d','#b97424','#193044'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':I,'axes.labelcolor':I,'svg.hashsalt':'precalc142-module1','savefig.facecolor':'white','axes.spines.top':False,'axes.spines.right':False})
def save(name,fig):
    fig.savefig(OUT/f'{name}.svg',bbox_inches='tight',pad_inches=.24,metadata={'Date':None})
    svg=OUT/f'{name}.svg';svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
    fig.savefig(OUT/f'{name}.pdf',bbox_inches='tight',pad_inches=.24,metadata={'CreationDate':None,'ModDate':None})
    plt.close(fig)
def plane(ax,lim=1.4):
    ax.set_aspect('equal');ax.set_xlim(-lim,lim);ax.set_ylim(-lim,lim);ax.axis('off')
    ax.annotate('',(lim,0),(-lim,0),arrowprops={'arrowstyle':'->','color':'#a0b3bf','lw':1})
    ax.annotate('',(0,lim),(0,-lim),arrowprops={'arrowstyle':'->','color':'#a0b3bf','lw':1})
    ax.text(lim-.05,-.15,'x',ha='right');ax.text(.08,lim-.06,'y')
def ray(ax,a,r=1,color=O):
    p=r*np.array([math.cos(a),math.sin(a)]);ax.plot([0,p[0]],[0,p[1]],color=color,lw=2.6);ax.plot(*p,'o',color=color,ms=6);return p
def arc(ax,r,a,color=G,lw=3):
    t=np.linspace(0,a,100);ax.plot(r*np.cos(t),r*np.sin(t),color=color,lw=lw)
    if abs(a)>.05:
        ax.add_patch(FancyArrowPatch((r*math.cos(t[-4]),r*math.sin(t[-4])),(r*math.cos(a),r*math.sin(a)),arrowstyle='->',mutation_scale=13,color=color,lw=lw))
def unit(ax):
    plane(ax);ax.add_patch(Circle((0,0),1,fill=False,color=B,lw=2))
def make():
    f,axs=plt.subplots(1,2,figsize=(8,3.5))
    for ax,a,title in zip(axs,[math.pi/3,-math.pi/3],['Counterclockwise: +60°','Clockwise: −60°']):
        unit(ax);ray(ax,a);arc(ax,.48,a);ax.set_title(title,fontsize=12,pad=12)
    save('signed-rotation',f)
    f,axs=plt.subplots(1,3,figsize=(10,3.4))
    for ax,d in zip(axs,[60,420,-300]):
        unit(ax);ray(ax,math.pi/3);arc(ax,.46,(60 if d>0 else -300)*math.pi/180);ax.set_title(f'{d}°',fontsize=15)
        ax.text(0,-1.28,{60:'1/6 turn',420:'1 full turn + 1/6 turn',-300:'5/6 turn clockwise'}[d],ha='center',fontsize=10)
    save('coterminal-rotations',f)
    f,ax=plt.subplots(figsize=(5.8,4));plane(ax,1.55);ax.add_patch(Circle((0,0),1,fill=False,color=B,lw=2));ray(ax,0);ray(ax,1);arc(ax,1,1);arc(ax,.35,1,color=O,lw=1.5)
    ax.text(.6,-.15,'radius r');ax.text(1.12,.65,'arc length s = r',color=G);ax.text(.43,.24,'1 rad',fontsize=10);ax.set_title('One radian: the arc is as long as the radius',fontsize=12)
    save('one-radian',f)
    f,ax=plt.subplots(figsize=(6.4,4.5));plane(ax,3.65)
    for r in [1.5,3]:
        ax.add_patch(Circle((0,0),r,fill=False,color=B,alpha=.6,lw=1.4));ray(ax,math.pi/3,r);ray(ax,0,r);arc(ax,r,math.pi/3)
    ax.text(.2,3.04,r'$\theta=\pi/3$ for both circles',color=B,fontsize=12)
    ax.text(1.5,-.35,'radius 3; arc π',ha='center',fontsize=10);ax.text(1.15,1.2,'radius 1.5\narc π/2',fontsize=10)
    ax.set_title('Doubling the radius doubles the arc length',loc='left',pad=14,fontsize=12)
    save('same-angle-two-radii',f)
    f,axs=plt.subplots(1,4,figsize=(10,3))
    for ax,d,lab in zip(axs,[90,180,270,360],[r'$\pi/2$',r'$\pi$',r'$3\pi/2$',r'$2\pi$']):
        ax.set_aspect('equal');ax.axis('off');ax.set_xlim(-1.3,1.3);ax.set_ylim(-1.45,1.35)
        ax.add_patch(Circle((0,0),1,fill=False,color='#c8d6df'));arc(ax,1,math.radians(d));ray(ax,0);ray(ax,math.radians(d));ax.set_title(f'{d}° = '+lab);ax.text(0,-1.3,f'{d//90}/4 of a turn' if d!=360 else 'One full turn',ha='center',fontsize=10)
    save('turn-fractions',f)
    f,ax=plt.subplots(figsize=(6,4));unit(ax);a=2*math.pi/3;p=ray(ax,a);arc(ax,1,a);ax.plot([1,p[0]],[0,p[1]],'--',lw=2,color=O);ax.set_title('Curved path: arc length',color=G,pad=14,fontsize=12);ax.set_ylim(-1.9,1.4);ax.text(0,-1.65,'Straight shortcut: chord / displacement',color=O,fontsize=10,ha='center');save('arc-and-chord',f)
    f,axs=plt.subplots(1,2,figsize=(8,4))
    for ax,r in zip(axs,[2,4]):
        plane(ax,4.7);ax.add_patch(Circle((0,0),r,fill=False,color=B));ray(ax,math.pi/6,r);arc(ax,r,math.pi/6);ax.set_title(f'Radius {r} m',fontsize=12)
        ax.set_ylim(-6.3,4.7);ax.text(0,-5.5,r'$\omega=\pi/12$ rad/s'+'\n'+(r'$v=\pi/6$ m/s' if r==2 else r'$v=\pi/3$ m/s'),ha='center',fontsize=11)
    f.suptitle('Same 30° turn in 2 seconds; different distances',fontsize=12);save('angular-and-tangential-speed',f)
    f,ax=plt.subplots(figsize=(6,4.5));unit(ax);a=math.pi/3;p=ray(ax,a);ax.plot([p[0],p[0]],[0,p[1]],color=G,lw=3);ax.plot([0,p[0]],[0,0],color=B,lw=3);ax.text(.5,1.15,r'$P=(\cos\theta,\sin\theta)$',ha='center',fontsize=13);ax.text(.25,-.17,r'$x=\cos\theta$',ha='center',color=B);ax.text(.6,.4,r'$y=\sin\theta$',color=G);arc(ax,.3,a,color=O,lw=1.3);save('unit-circle-coordinates',f)
    f,ax=plt.subplots(figsize=(5.5,3.7));ax.set_aspect('equal');ax.axis('off');ax.set_xlim(-.35,1.65);ax.set_ylim(-.4,1.4);ax.plot([0,1,1,0],[0,0,1,0],color=B,lw=2.5);ax.plot([.88,.88,1],[0,.12,.12],color=I);ax.text(.5,-.15,'1',ha='center');ax.text(1.1,.5,'1');ax.text(.32,.66,r'$\sqrt{2}$',fontsize=14);ax.text(.25,.08,'45°');ax.set_title('Equal legs → equal coordinates',fontsize=12);save('triangle-45',f)
    f,ax=plt.subplots(figsize=(6.8,4));ax.set_aspect('equal');ax.axis('off');ax.set_xlim(-.35,3.8);ax.set_ylim(-.4,2.1)
    h=math.sqrt(3);ax.plot([0,2,1,0],[0,0,h,0],color=B,lw=2.5);ax.plot([1,1],[0,h],'--',color=G,lw=2);ax.text(.5,-.2,'1',ha='center');ax.text(1.5,-.2,'1',ha='center');ax.text(.3,.95,'2');ax.text(1.65,.95,'2');ax.text(1.1,.8,r'$\sqrt{3}$');ax.text(.25,.1,'60°');ax.text(.82,1.16,'30°',fontsize=10);ax.plot([1,1.12,1.12],[.12,.12,0],color=I);ax.text(2.4,1.3,'Bisect an equilateral\ntriangle with side 2.',fontsize=11);ax.text(2.4,.5,r'$\sqrt{2^2-1^2}=\sqrt{3}$',fontsize=12);save('triangle-30',f)
    f,ax=plt.subplots(figsize=(6,4.8));unit(ax)
    for t in ax.texts:t.set_visible(False)
    for x,y,txt in [(.56,.58,'I\ncos +, sin +'),(-.56,.58,'II\ncos −, sin +'),(-.56,-.58,'III\ncos −, sin −'),(.56,-.58,'IV\ncos +, sin −')]:ax.text(x,y,txt,ha='center',va='center',fontsize=11)
    for x,y,t,ha in [(1.12,-.15,'(1, 0)','left'),(-1.12,-.15,'(−1, 0)','right'),(0,1.13,'(0, 1)','center'),(0,-1.2,'(0, −1)','center')]:ax.text(x,y,t,ha=ha,fontsize=10)
    ax.set_xlim(-1.85,1.85);save('quadrant-signs',f)
    f,axs=plt.subplots(1,3,figsize=(10,3.4))
    for ax,d,reference in zip(axs,[120,225,300],[60,45,60]):
        unit(ax);a=math.radians(d);p=ray(ax,a);ax.plot([p[0],p[0]],[0,p[1]],'--',color=G)
        start=math.pi if d in [120,225] else 2*math.pi;stop=a
        ts=np.linspace(min(start,stop),max(start,stop),50);ax.plot(.35*np.cos(ts),.35*np.sin(ts),color=G,lw=2)
        mid=(start+stop)/2;ax.text(.58*math.cos(mid),.58*math.sin(mid),f'{reference}°',ha='center',va='center',fontsize=10,color=G);ax.set_title(f'Angle {d}°',fontsize=12)
    save('reference-angles',f)
    f,axs=plt.subplots(1,2,figsize=(8,4))
    for ax,r,lab in zip(axs,[1,3],[r'$(1/2,\sqrt{3}/2)$',r'$(3/2,3\sqrt{3}/2)$']):
        plane(ax,3.6);ax.add_patch(Circle((0,0),r,fill=False,color=B,lw=2));p=ray(ax,math.pi/3,r);ax.plot([p[0],p[0]],[0,p[1]],'--',color=G);ax.text(.15,3.25,lab,ha='left',fontsize=12);ax.set_title(f'Radius {r}',fontsize=12)
    f.suptitle('Same angle; multiply both coordinates by the radius',fontsize=12);save('radius-scaling',f)
    f,axs=plt.subplots(1,2,figsize=(9.6,3.8),gridspec_kw={'width_ratios':[1,2]});unit(axs[0]);ray(axs[0],math.pi/3);axs[0].set_title('A point turns on the circle',fontsize=11)
    t=np.linspace(0,4*math.pi,500);ax=axs[1];ax.plot(t,np.cos(t),color=B,label='cos θ: horizontal');ax.plot(t,np.sin(t),color=G,label='sin θ: vertical');ax.axhline(0,color='#c5cfd6',lw=.8);ax.set_xticks([0,math.pi,2*math.pi,3*math.pi,4*math.pi],['0','π','2π','3π','4π']);ax.set_yticks([-1,0,1]);ax.set_xlabel('Angle θ (radians)');ax.set_ylabel('Coordinate value');ax.legend(loc='upper center',bbox_to_anchor=(.5,1.3),ncol=1,fontsize=10);ax.set_ylim(-1.25,1.25);f.subplots_adjust(wspace=.4,top=.78);save('circle-to-wave',f)
    f,ax=plt.subplots(figsize=(8,3.9));t=np.linspace(0,40,300);ax.plot(t,10+8*np.sin(math.pi*t/20),color=G,lw=2.5)
    for tt,hh in [(0,10),(10,18),(20,10),(30,2),(40,10)]:ax.plot(tt,hh,'o',color=O);ax.annotate(f'({tt}, {hh})',(tt,hh),xytext=(0,12 if hh!=18 else -23),textcoords='offset points',ha='center',fontsize=10)
    ax.set(xlim=(-2,42),ylim=(0,21),xlabel='Time t (seconds)',ylabel='Height above ground (meters)');ax.set_xticks(range(0,41,10));ax.set_yticks([0,2,10,18]);ax.grid(alpha=.15);save('ferris-height',f)
    f,ax=plt.subplots(figsize=(6.5,4.5));ax.set_aspect('equal');ax.axis('off');ax.set(xlim=(-17,19),ylim=(-1,31));ax.axhline(0,color=I,lw=1.5);ax.add_patch(Circle((0,14),12,fill=False,color=B,lw=2));ax.plot([0,12],[14,14],color=O,lw=2);ax.plot(12,14,'o',color=O);ax.text(13,14,'Start',va='center');ax.text(6,15.2,'12 m radius',ha='center');ax.annotate('',(-15,14),(-15,0),arrowprops={'arrowstyle':'<->','color':G});ax.text(-16,7,'14 m',rotation=90,va='center');ax.text(0,29,'48 seconds per counterclockwise turn',ha='center',fontsize=11);ax.text(5,-.5,'Ground',va='top');save('application-ferris-setup',f)
    f,ax=plt.subplots(figsize=(6,4));unit(ax);p=ray(ax,math.pi/4);ax.text(.7,.2,'0.75 m',color=O);ax.set_title('4 revolutions per minute',pad=15);ax.set_ylim(-1.8,1.4);ax.text(0,-1.65,'Follow the sensor for 15 seconds.',ha='center');arc(ax,.45,math.pi/2);save('application-antenna-setup',f)
    f,ax=plt.subplots(figsize=(6,4));ax.set_aspect('equal');ax.set(xlim=(-.6,5.3),ylim=(-.6,4.2));ax.spines[['top','right']].set_visible(False);ax.set_xticks(range(6));ax.set_yticks(range(5));ax.grid(alpha=.15);ax.plot([0,4,4,0],[0,0,3,0],color=B,lw=2.5);ax.plot(4,3,'o',color=O);ax.text(4.13,3.15,'P = (4, 3)');ax.text(1.5,1.5,'r = 5',rotation=37);ax.text(2,-.38,'4 right',ha='center');ax.text(4.13,1.4,'3 up');ax.set_xlabel('Horizontal coordinate x');ax.set_ylabel('Vertical coordinate y');save('coordinate-prerequisite',f)
    print('Built 18 SVG/PDF diagram pairs.')
if __name__=='__main__':make()
