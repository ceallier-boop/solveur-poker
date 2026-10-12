"""Modèle corrigé : stratégies HRC interpolées selon la profondeur de stack (limp, raise, all-in inclus),
avec règle du stack effectif pour les répartitions inégales."""
import numpy as np
from hrcdata import *
EQ3={4:('3wc',1),6:('3wc',2),8:8,10:7,12:[6,('c2',7)],14:('c2',15),15:('3wc',3),18:5,20:('c2',14),25:4}
EQHU={2:22,4:21,6:20,8:19,10:18,12:[17,('c2',12)],15:[('huc',4),('c2',11)],18:16,20:('c2',13),25:15}
def _loc(kind,v):
    if isinstance(v,list): v=v[0]
    return (v if isinstance(v,tuple) else (kind,v))
_cache={}
_E=np.load('/home/claude/E3.npy'); _P=W/W.sum(); _vs=_E@_P
_order=np.argsort(_vs); _pct=np.zeros(169); _c=np.cumsum(_P[_order]); _pct[_order]=_c-_P[_order]/2
def fill_unreached(F,reached,wmass):
    """mains sans donnée : fréquence lissée en fonction du rang d'équité, calée sur les mains atteintes"""
    if reached.sum()<4 or reached.all(): return F
    out=F.copy(); idx=np.where(reached)[0]
    edges=np.quantile(_pct[idx],np.linspace(0,1,7))
    centers=[];vals=[]
    for a,b in zip(edges[:-1],edges[1:]):
        m=idx[(_pct[idx]>=a)&(_pct[idx]<=b)]
        if len(m)==0: continue
        w=wmass[m]+1e-9; centers.append(np.average(_pct[m],weights=w)); vals.append(np.average(F[m],axis=0,weights=w))
    centers=np.array(centers); vals=np.array(vals)
    for i in np.where(~reached)[0]:
        out[i]=[np.interp(_pct[i],centers,vals[:,j]) for j in range(F.shape[1])]
    s=out.sum(1,keepdims=True); return out/np.where(s>0,s,1)
def sol(kind,h):
    kd,hh=_loc(kind,h)
    k=(kd,hh)
    if k not in _cache:
        s,nodes=load(kd,hh); st=stacks_of(s); ix=index_nodes(s,nodes)
        d={}
        for key,i in ix.items():
            n=nodes[i]; labs=act_labels(n,st)
            played=np.array([[n['hands'][x]['played'][j] for j in range(len(labs))] for x in NAMES])
            evs=np.array([[n['hands'][x]['evs'][j] for j in range(len(labs))] for x in NAMES])
            wt=np.array([n['hands'][x]['weight'] for x in NAMES])
            d[key]=dict(labels=labs,played=played,evs=evs,w=wt,player=n['player'],seq=n['sequence'])
        _cache[k]=(st,d)
    return _cache[k]
def stacks_avail(kind,exclude=()):
    base=EQ3 if kind=='3w' else EQHU
    return sorted(S for S in base if S not in exclude)
def _at(kind,S,key):
    base=EQ3 if kind=='3w' else EQHU
    v=base[S]; locs=v if isinstance(v,list) else [v]
    ns=[sol(kind,l)[1].get(key) for l in locs]; ns=[n for n in ns if n is not None]
    if not ns: return None
    if len(ns)==1: return ns[0]
    labs=list(dict.fromkeys(sum([n['labels'] for n in ns],[])))
    P=np.zeros((169,len(labs))); Wt=np.zeros(169); cnt=np.zeros(169)
    for n in ns:
        r=n['w']>0.05
        for j,l in enumerate(labs):
            if l in n['labels']: P[r,j]+=n['played'][r,n['labels'].index(l)]
        cnt[r]+=1; Wt+=n['w']
    P=np.where(cnt[:,None]>0,P/np.maximum(cnt[:,None],1),0.0)
    s_=P.sum(1,keepdims=True); P=np.where(s_>0,P/np.where(s_>0,s_,1),0.0)
    return dict(labels=labs,played=P,w=Wt/len(ns),player=ns[0]['player'],seq=ns[0]['seq'],evs=None)
def surrogate(kind,S,key,exclude=()):
    """renvoie (labels, F[169,nA], w[169]) pour le noeud `key` à la profondeur S (interpolation linéaire entre stacks HRC)"""
    av=stacks_avail(kind,exclude)
    if S<=av[0]: lo=hi=av[0]
    elif S>=av[-1]: lo=hi=av[-1]
    else:
        lo=max(x for x in av if x<=S); hi=min(x for x in av if x>=S)
    nl=_at(kind,lo,key); nh=_at(kind,hi,key)
    if nl is None and nh is None:
        # chercher le stack disponible le plus proche qui possède le noeud
        cand=[x for x in av if _at(kind,x,key) is not None]
        if not cand: return None
        c=min(cand,key=lambda x:abs(x-S)); n=_at(kind,c,key); return n['labels'],n['played'].copy(),n['w'].copy()
    if nl is None: nl=nh
    if nh is None: nh=nl
    t=0.0 if lo==hi else (S-lo)/(hi-lo)
    if lo!=hi and (hi-lo)>4: t=min(1.0,max(0.0,(t-0.25)/0.5))   # écart > 4 BB : stack HRC le plus proche sur les 25 % extrêmes de l'écart, interpolation au milieu
    labs=list(dict.fromkeys(nl['labels']+nh['labels']))
    F=np.zeros((169,len(labs)))
    wl,wh=nl['w'],nh['w']
    for j,l in enumerate(labs):
        fl=nl['played'][:,nl['labels'].index(l)] if l in nl['labels'] else None
        fh=nh['played'][:,nh['labels'].index(l)] if l in nh['labels'] else None
        if fl is None: fl=fh      # action absente de l'arbre d'un côté : on garde la fréquence de l'autre côté
        if fh is None: fh=fl
        # main non atteinte d'un côté : on prend l'autre côté
        a=np.where(wl>0.05,fl,fh); b=np.where(wh>0.05,fh,fl)
        F[:,j]=(1-t)*a+t*b
    s=F.sum(1,keepdims=True); F=np.where(s>0,F/np.where(s>0,s,1),1.0/len(labs))
    reached=(wl>0.05)|(wh>0.05); wm=(1-t)*wl+t*wh
    F=fill_unreached(F,reached,W*wm)
    return labs,F,wm
