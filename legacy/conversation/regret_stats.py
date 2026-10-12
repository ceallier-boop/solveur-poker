import numpy as np, json
from hrcdata import *
import eval_vs_hrc as ev
import hrc_surrogate as hs
import scorecard as sc   # réutilise corrected(), score()
def wq(x,w,q):
    o=np.argsort(x); c=np.cumsum(w[o])/w.sum(); return float(x[o][np.searchsorted(c,q)])
def stats(node,st,labs,M,decide):
    wts=np.array([node['hands'][x]['weight'] for x in NAMES]); mass=W*wts
    played=np.array([[node['hands'][x]['played'][j] for j in range(len(labs))] for x in NAMES])
    evs=np.array([[node['hands'][x]['evs'][j] for j in range(len(labs))] for x in NAMES])
    loss=evs.max(1)-(M*evs).sum(1); hd=played.argmax(1)
    crit=(played.max(1)>=0.8)&(decide!=hd)         # HRC joue une action à ≥80 % et le modèle en décide une autre
    return mass,loss,crit
def collect(model_rows):
    ms=[];ls=[];cs=[];rs=[]
    for mass,loss,crit,reach in model_rows:
        ms.append(mass*reach);ls.append(loss);cs.append(crit)
    m=np.concatenate(ms); l=np.concatenate(ls); c=np.concatenate(cs)
    return dict(mean=1000*float((m*l).sum()/m.sum()),p95=1000*wq(l,m,0.95),p99=1000*wq(l,m,0.99),mx=1000*float(l.max()),
                gt10=100*float((m*(l>0.01)).sum()/m.sum()),gt50=100*float((m*(l>0.05)).sum()/m.sum()),gt100=100*float((m*(l>0.10)).sum()/m.sum()),
                crit=100*float((m*c).sum()/m.sum()))
out={}
# modèle corrigé (stack retiré)
rows=[]
for kind,Ss in [('hu',[6,8,10,12]),('3w',[10,12])]:
    for S in Ss:
        for key,n,st,labs,M,allr in sc.corrected(kind,S,False):
            mass,loss,crit=stats(n,st,labs,M,M.argmax(1)); rows.append((kind,mass,loss,crit,allr))
for kind in ['3w','hu']:
    r=[(a[1],a[2],a[3],a[4]) for a in rows if a[0]==kind]; out[f"corrigé {kind}"]=collect(r)
# push/fold maison
SCN=[('3w',8),('3w',7),('3w',6),('hu',21),('hu',20),('hu',19),('hu',18),('hu',17)]
pr=[]
for kind,h in SCN:
    s,nodes=load(kind,h); st=stacks_of(s); ix=index_nodes(s,nodes); model=ev.models_for(kind,st); path,g=ev.path_probs(nodes,st)
    for key,name,mk,typ,opp in ev.node_defs(kind,st):
        if key=='SBSHOVE': key=ev.find_sbshove(nodes,ix,st) if kind=='3w' else None
        if key is None or key not in ix: continue
        node=nodes[ix[key]]; labs=act_labels(node,st)
        if typ=='shove':
            idx,_=ev.shove_idx(node,st,opp)
            if idx is None: continue
        else:
            if 'C' not in labs: continue
            idx=labs.index('C')
        fi=labs.index('F'); v=model[mk]; M=np.zeros((169,len(labs))); M[:,idx]=v; M[:,fi]+=1-v
        decide=np.where(v>=0.5,idx,fi); mass,loss,crit=stats(node,st,labs,M,decide)
        rr=1.0
        for (p_,gp) in path[ix[key]]: rr*=gp
        pr.append((kind,mass,loss,crit,rr,name))
for kind in ['3w','hu']:
    out[f"push/fold {kind}"]=collect([(a[1],a[2],a[3],a[4]) for a in pr if a[0]==kind])
for lab,fn in [('push/fold : calls',lambda a:'face' in a[5]),('push/fold : all-in BTN',lambda a:a[5].startswith('BTN')),('push/fold : all-in SB',lambda a:a[5].startswith('SB') and 'face' not in a[5])]:
    out[lab]=collect([(a[1],a[2],a[3],a[4]) for a in pr if fn(a)])
for k,v in out.items(): print(f"{k:26s} regret moyen {v['mean']:5.1f} | P95 {v['p95']:5.1f} | P99 {v['p99']:5.1f} | max {v['mx']:6.1f} mBB | >10 mBB {v['gt10']:4.1f}% | >50 mBB {v['gt50']:4.1f}% | >100 mBB {v['gt100']:4.1f}% | erreurs critiques {v['crit']:4.1f}%")
json.dump(out,open('regret_stats.json','w'))
