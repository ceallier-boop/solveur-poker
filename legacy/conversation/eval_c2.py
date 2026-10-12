import numpy as np, json
from hrcdata import *
import hrc_surrogate as hs
import eval_vs_hrc as ev
from loo_unequal import seff_for, canon
def stats_node(node,labs,M,decide):
    wts=np.array([node['hands'][x]['weight'] for x in NAMES]); mass=W*wts; tot=mass.sum()
    played=np.array([[node['hands'][x]['played'][j] for j in range(len(labs))] for x in NAMES])
    evs=np.array([[node['hands'][x]['evs'][j] for j in range(len(labs))] for x in NAMES])
    loss=evs.max(1)-(M*evs).sum(1); hd=played.argmax(1); floor=evs.max(1)-(played*evs).sum(1)
    tv=0.5*np.abs(M-played).sum(1)
    return dict(tv=100*float((mass*tv).sum()/tot),agree=100*float((mass*(decide==hd)).sum()/tot),loss=1000*float((mass*loss).sum()/tot),floor=1000*float((mass*floor).sum()/tot),
                gt10=100*float((mass*(loss>0.01)).sum()/tot),crit=100*float((mass*((played.max(1)>=0.8)&(decide!=hd))).sum()/tot))
def run(kd,h,predict,minreach=0.003):
    s,nodes=load(kd,h); st=stacks_of(s); ix=index_nodes(s,nodes); path,g=ev.path_probs(nodes,st)
    tl=tf=tt=tr=unc=0; rows=[]
    for i,n in sorted(nodes.items()):
        labs=act_labels(n,st)
        wts=np.array([n['hands'][x]['weight'] for x in NAMES]); mass=W*wts
        if mass.sum()<=0: continue
        pl=n['player']; others=1.0; allr=1.0
        for (p_,gp) in path[i]:
            allr*=gp
            if p_!=pl: others*=gp
        if allr<minreach: continue
        weight=others*mass.sum()/W.sum()
        r=predict(n,st)
        if r is None: unc+=weight; continue
        labs_m,M=r
        sd=stats_node(n,labs_m,M,M.argmax(1)); sd.update(key=canon(st,n['sequence']) if len(st)==3 else '',w=weight,reach=allr)
        tl+=weight*sd['loss']; tf+=weight*sd['floor']; tt+=weight*sd['tv']; tr+=weight; rows.append(sd)
    return st,dict(loss=tl,floor=tf,net=max(0,tl-tf),tv=tt/max(tr,1e-12),unc=unc,rows=rows)
def surr_pred(kind,seff_fn):
    def f(n,st):
        se=seff_fn(n,st); key=key_of(n['sequence'],[min(st)]*len(st)) if kind=='hu' else None
        if kind=='3w': key=canon(st,n['sequence'])
        sg=hs.surrogate(kind,se,key)
        if sg is None: return None
        slabs,F,_=sg
        # étiquettes du noeud HRC avec all-in effectif
        labs=[]
        for a in n['actions']:
            amt=a['amount']/10000
            labs.append('A' if a['type']=='R' and amt>=se-1e-9 else (f"R{amt:g}" if a['type']=='R' else a['type']))
        M=np.zeros((169,len(labs)))
        for j,l in enumerate(labs):
            if l in slabs: M[:,j]=F[:,slabs.index(l)]
        s=M.sum(1,keepdims=True)
        if (s<1e-9).all(): return None
        return labs,M/np.maximum(s,1e-12)
    return f
if __name__=='__main__':
    seff3=lambda n,st: seff_for(n['player'],n['sequence'],st)
    def seffhu(n,st): return min(st)
    tests=[('3 joueurs égaux 12 (nouvel export)', 'c2',7,'3w',lambda n,st:12),('3 joueurs égaux 14','c2',15,'3w',lambda n,st:14),('3 joueurs égaux 20','c2',14,'3w',lambda n,st:20),
           ('HU 12 (nouvel export)','c2',12,'hu',lambda n,st:12),('HU 15 (nouvel export)','c2',11,'hu',lambda n,st:15),('HU 20','c2',13,'hu',lambda n,st:20),
           ('HU 4/8','c2',8,'hu',seffhu),('HU 8/4','c2',9,'hu',seffhu)]
    for h in [1,2,3,4,5,6,16,17,18,19,20,21]: tests.append((f"3 joueurs inégaux H{h}",'c2',h,'3w',seff3))
    res={}
    for label,kd,h,kind,sf in tests:
        pred=surr_pred(kind,sf)
        st,r=run(kd,h,pred); res[label]=dict(stacks=st,loss=r['loss'],floor=r['floor'],net=r['net'],tv=r['tv'],unc=r['unc'])
        print(f"{label:38s} {str(st):18s} perte {r['loss']:6.1f} (plancher {r['floor']:5.1f}, nette {r['net']:5.1f}) TV {r['tv']:4.1f}% non couvert {r['unc']:.3f}",flush=True)
    json.dump(res,open('eval_c2.json','w'))
