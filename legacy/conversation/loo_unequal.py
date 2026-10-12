import numpy as np, json
from hrc_surrogate import *
from eval_vs_hrc import path_probs
UN={9:(12,21,21),10:(21,12,21),11:(21,21,12),12:(8,14,14),13:(14,8,14),14:(14,14,8)}
def seff_for(actor,seq,st):
    """stack effectif du noeud : BTN racine = min(b,max(s,c)) ; sinon min(acteur, dernier agresseur) ; sinon min(SB,BB)"""
    b,s,c=st
    aggr=None
    for a in seq:
        if a['type']=='R': aggr=a['player']
    if aggr is None:
        if not seq and actor==0: return min(b,max(s,c))
        return min(st[actor],st[2] if actor==1 else st[1]) if actor!=0 else min(b,max(s,c))
    return min(st[actor],st[aggr])
def canon(st,seq_actions):
    """clé canonique et étiquettes de chaque action avec all-in effectif"""
    key=[]; hist=[]
    for a in seq_actions:
        se=seff_for(a['player'],hist,st); amt=a['amount']/10000
        allin=a['type']=='R' and amt>=se-1e-9
        key.append(f"{a['player']}{a['type']}{'A' if allin else (format(amt,'g') if a['type']=='R' else '')}"); hist.append(a)
    return '-'.join(key)
def evaluate_unequal(h,minreach=0.003,detail=False,old=None):
    s,nodes=load('3w',h); st=stacks_of(s); path,g=path_probs(nodes,st)
    tl=tf=tt=tr=unc=0
    for i,n in sorted(nodes.items()):
        wts=np.array([n['hands'][x]['weight'] for x in NAMES]); mass=W*wts
        if mass.sum()<=0: continue
        pl=n['player']; others=1.0; allr=1.0
        for (p_,gp) in path[i]:
            allr*=gp
            if p_!=pl: others*=gp
        if allr<minreach: continue
        own=mass.sum()/W.sum(); weight=others*own
        key=canon(st,n['sequence']); se=seff_for(pl,n['sequence'],st)
        labs=[]
        for a in n['actions']:
            amt=a['amount']/10000
            labs.append('A' if a['type']=='R' and amt>=se-1e-9 else (f"R{amt:g}" if a['type']=='R' else a['type']))
        played=np.array([[n['hands'][x]['played'][j] for j in range(len(labs))] for x in NAMES]); evs=np.array([[n['hands'][x]['evs'][j] for j in range(len(labs))] for x in NAMES])
        sg=surrogate('3w',se,key)
        if sg is None: unc+=weight; continue
        slabs,F,_=sg; M=np.zeros((169,len(labs)))
        for j,l in enumerate(labs):
            if l in slabs: M[:,j]=F[:,slabs.index(l)]
        M=M/np.maximum(M.sum(1,keepdims=True),1e-12)
        tv=0.5*float((mass[:,None]*np.abs(M-played)).sum()/mass.sum()); best=evs.max(1)
        loss=float((mass*(best-(M*evs).sum(1))).sum()/mass.sum()); floor=float((mass*(best-(played*evs).sum(1))).sum()/mass.sum())
        tl+=weight*loss; tf+=weight*floor; tt+=weight*tv; tr+=weight
        if detail: print(f"   {key!r:16s} S_eff {se:>4g} poids {weight:.3f} perte {1000*loss:6.1f} TV {100*tv:4.1f}%")
    return 1000*tl,1000*tf,tt/max(tr,1e-12),unc
if __name__=='__main__':
    old=json.load(open('eval_vs_hrc2.json'))
    print("Stacks inégaux : modèle corrigé (HRC interpolé + stack effectif) comparé aux solutions HRC inégales")
    for h,cfg in UN.items():
        l,f,tv,u=evaluate_unequal(h)
        ov=sum(r['reach']*max(0,r['loss']-r['floor']) for r in old[f'3w{h}']['rows'])
        print(f"  {cfg}: perte {l:5.1f} mBB (nette {max(0,l-f):5.1f}), plancher {f:4.1f}, TV {100*tv:4.1f}%, non couvert {u:.3f} | ancien modèle push/fold (nœuds couverts seulement) : {ov:4.1f}")
