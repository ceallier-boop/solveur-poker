import numpy as np, glob, json
from hrc_surrogate import *
from hrc_surrogate import _loc
from loo_unequal import seff_for
from pushfold_raise import notation
import pushfold as pf
E=np.load('E3.npy'); P=W/W.sum()
fr=lambda x:format(x,'g').replace('.',',')
PF_MAP={'':'btn','0F':'s1','0RA':'sc','0RA-1F':'b2','0F-1RA':'b1'}   # lignes couvertes par le push/fold
def pf_vec(cfg,key):
    fn='uneq_'+'_'.join(format(x,'g') for x in cfg)+'.npz'
    d=np.load(fn); return d[PF_MAP[key]] if key in PF_MAP else None
def canon_label(a,se):
    amt=a['amount']/10000
    return 'A' if a['type']=='R' and amt>=se-1e-9 else (f"R{amt:g}" if a['type']=='R' else a['type'])
def build_rows(kind,skel_stack,strategy,st,pl,minreach=0.005):
    """parcourt l'arbre HRC du stack `skel_stack` ; strategy(key,actor,seq,labels)->(labels,F)|None"""
    base=EQ3 if kind=='3w' else EQHU
    kd,hh=_loc(kind,base[skel_stack]); s,nodes=load(kd,hh); sst=stacks_of(s)
    rows=[]
    def rec(i,own,reach):
        n=nodes[i]; pl_i=n['player']; seq=n['sequence']
        labs_skel=[canon_label(a,100) for a in n['actions']]  # types
        key=key_of(seq,sst)
        sg=strategy(key,pl_i,seq,n)
        if sg is None: return
        labs,F=sg
        mass=W*own[pl_i]
        if mass.sum()<=0 or reach<minreach: return
        am=F.argmax(1); items=[]; pf_=0
        for j,l in enumerate(labs):
            v=((am==j)&(own[pl_i]>=0.05)).astype(float); share=100*float((mass*v).sum()/mass.sum())
            if l=='F': pf_=share; continue
            if share<0.5: continue
            items.append((l,share,v))
        hist=' ; '.join(f"{pl[a['player']]} {('fold' if a['type']=='F' else 'check' if a['type']=='X' else ('limp' if (a['type']=='C' and not any(b['type']=='R' for b in seq[:k]) and pl[a['player']]=='SB') else 'paie') if a['type']=='C' else ('all-in' if a['amount']/10000>=sst[a['player']]-1e-9 else 'raise à '+fr(a['amount']/10000)))}" for k,a in enumerate(seq))
        rows.append(dict(key=key,player=pl[pl_i],hist=hist,reach=reach,items=items,fold=pf_,labs=labs))
        for j,a in enumerate(n['actions']):
            c=a.get('node')
            if c is None or c not in nodes: continue
            f=F[:,labs.index(canon_label(a,sst[pl_i]))] if canon_label(a,sst[pl_i]) in labs else np.zeros(169)
            g=float((mass*f).sum()/W.sum())
            own2=[o.copy() for o in own]; own2[pl_i]=own[pl_i]*f
            # joueurs qui n'ont pas encore agi gardent un poids 1
            rec(c,own2,reach*g)
    rec(0,[np.ones(169) for _ in range(len(sst))],1.0)
    return rows
def strat_equal(kind,S):
    def fn(key,actor,seq,node):
        if kind=='3w' and S<8: return None
        sg=surrogate(kind,S,key)
        if sg is None: return None
        labs,F,_=sg; return labs,F
    return fn
def strat_uneq(cfg):
    st=list(cfg)
    def fn(key,actor,seq,node):
        se=seff_for(actor,[a for a in seq],st)
        if se>=4:
            sg=surrogate('3w',se,key)
            if sg is None: return None
            labs,F,_=sg; return labs,F
        v=pf_vec(cfg,key)
        if v is None: return None
        # push/fold : actions fold/all-in ou call/fold selon le noeud
        labs_node=[canon_label(a,se) for a in node['actions']]
        F=np.zeros((169,len(labs_node)))
        tgt='A' if key in ('','0F') else 'C'
        for j,l in enumerate(labs_node):
            if l=='F': F[:,j]=1-v
            elif l==tgt: F[:,j]=v
        return labs_node,F
    return fn
if __name__=='__main__':
    # exemples
    rows=build_rows('3w',18,strat_equal('3w',15),[15,15,15],['BTN','SB','BB'])
    for r in rows[:6]: print(r['player'],r['hist'] or 'début',f"{100*r['reach']:.1f}%",[(l,round(s)) for l,s,_ in r['items']],round(r['fold']))
    print('--- 15/10/5')
    rows=build_rows('3w',12,strat_uneq((15,10,5)),[15,10,5],['BTN','SB','BB'])
    for r in rows[:8]: print(r['player'],r['hist'] or 'début',f"{100*r['reach']:.1f}%",[(l,round(s)) for l,s,_ in r['items']],round(r['fold']))
