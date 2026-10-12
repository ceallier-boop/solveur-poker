import numpy as np
from hrc_surrogate import *
from hrc_surrogate import _loc
from eval_vs_hrc import path_probs
def evaluate(kind,S,exclude,minreach=0.003,detail=False,hrc=None):
    kd,h=_loc(kind,(EQ3 if kind=='3w' else EQHU)[S])
    s,nodes=load(kd,h); st=stacks_of(s); ix=index_nodes(s,nodes); path,g=path_probs(nodes,st)
    tl=tf=tt=tr=unc=0
    for key,i in sorted(ix.items(), key=lambda kv: kv[1]):
        n=nodes[i]; labs=act_labels(n,st)
        wts=np.array([n['hands'][x]['weight'] for x in NAMES]); mass=W*wts
        if mass.sum()<=0: continue
        pl=n['player']; others=1.0; allr=1.0
        for (p_,gp) in path[i]:
            allr*=gp
            if p_!=pl: others*=gp
        if allr<minreach: continue
        own=mass.sum()/W.sum(); weight=others*own
        played=np.array([[n['hands'][x]['played'][j] for j in range(len(labs))] for x in NAMES]); evs=np.array([[n['hands'][x]['evs'][j] for j in range(len(labs))] for x in NAMES])
        sg=surrogate(kind,S,key,exclude)
        if sg is None: unc+=weight; continue
        slabs,F,_=sg; M=np.zeros((169,len(labs)))
        for j,l in enumerate(labs):
            if l in slabs: M[:,j]=F[:,slabs.index(l)]
        M=M/np.maximum(M.sum(1,keepdims=True),1e-12)
        tv=0.5*float((mass[:,None]*np.abs(M-played)).sum()/mass.sum()); best=evs.max(1)
        loss=float((mass*(best-(M*evs).sum(1))).sum()/mass.sum()); floor=float((mass*(best-(played*evs).sum(1))).sum()/mass.sum())
        tl+=weight*loss; tf+=weight*floor; tt+=weight*tv; tr+=weight
        if detail: print(f"  {key!r:12s} poids {weight:.3f} perte {1000*loss:6.1f} mBB TV {100*tv:4.1f}%")
    return 1000*tl,1000*tf,tt/max(tr,1e-12),unc
if __name__=='__main__':
    print("HU (stack retiré puis interpolé) : perte totale pondérée par main distribuée (mBB)")
    for S in [4,6,8,10,12,15,18,20]:
        l,f,tv,u=evaluate('hu',S,(S,)); print(f"  {S:>2} BB : perte {l:5.1f} (nette {max(0,l-f):5.1f}), plancher HRC {f:4.1f}, TV {100*tv:4.1f}%, non couvert {u:.3f}")
    print("3 joueurs")
    for S in [6,8,10,12,14,15,18,20]:
        l,f,tv,u=evaluate('3w',S,(S,)); print(f"  {S:>2} BB : perte {l:5.1f} (nette {max(0,l-f):5.1f}), plancher HRC {f:4.1f}, TV {100*tv:4.1f}%, non couvert {u:.3f}")
