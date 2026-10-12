import numpy as np, json
from hrcdata import *
import hrc_surrogate as hs
from solver_hu import solve3
from eval_vs_hrc import path_probs
E=np.load('E3.npy'); HU=hs.EQHU
def hu_node(S,key):
    s,nodes=load('hu',HU[S]); st=stacks_of(s); ix=index_nodes(s,nodes); n=nodes[ix[key]]; labs=act_labels(n,st)
    return n,labs,st
def col(n,labs,l,field):
    j=labs.index(l); return np.array([n['hands'][x][field][j] for x in NAMES])
def fit_types(S):
    """T et décalages par main pour les trois pots post-flop, à partir des EV HRC (stack S)"""
    n0,l0,st=hu_node(S,''); out={}
    def one(name,key,act,q,hero_row_is_bb):
        n,labs,_=hu_node(S,key); ev=col(n,labs,act,'evs'); w=np.array([n['hands'][x]['weight'] for x in NAMES])
        sbar=E@q; x=2*sbar-1; m=w>0.05; ww=(W*w)[m]
        T=float((ww*x[m]*(ev[m]-1)).sum()/(ww*x[m]**2).sum())
        delta=ev-(T*x+1)
        out[name]=(T,hs.fill_unreached(delta[:,None],m,W*w)[:,0] if m.sum()<169 else delta)
    pL=col(n0,l0,'C','played'); qL=W*pL; qL/=qL.sum()
    one('X','0C','X',qL,True)
    if 'R3.5' in l0:
        pR=col(n0,l0,'R3.5','played'); qR=W*pR
        if qR.sum()>0: qR/=qR.sum(); one('C35','0R3.5','C',qR,True)
    nX,lX,_=hu_node(S,'0C')
    s_,nodes_=load('hu',HU[S]); ix_=index_nodes(s_,nodes_)
    if 'R3' in lX and '0C-1R3' in ix_:
        pR3=col(nX,lX,'R3','played'); q3=W*pR3
        if q3.sum()>0: q3/=q3.sum(); one('C3','0C-1R3','C',q3,False)
    return out
def interp(S,exclude):
    av=hs.stacks_avail('hu',exclude); lo=max([x for x in av if x<=S],default=av[0]); hi=min([x for x in av if x>=S],default=av[-1])
    return lo,hi
def payoffs(S,exclude=()):
    if S in HU and S not in exclude: p=fit_types(S)
    else:
        lo,hi=interp(S,exclude); a=fit_types(lo); b=fit_types(hi); t=0 if lo==hi else (S-lo)/(hi-lo)
        p={}
        for k in a:
            if k in b: p[k]=((1-t)*a[k][0]+t*b[k][0],(1-t)*a[k][1]+t*b[k][1])
            else: p[k]=a[k]
    return p
def build(p,S):
    zero=np.zeros(169)
    def get(k): return p.get(k,(0.0,zero))
    Tx,dx=get('X'); T3,d3=get('C3'); T35,d35=get('C35')
    x=2*E-1
    Cl=Tx*x-dx[None,:]          # SB net : check après limp (offset de la main du BB)
    Ci=T3*x+d3[:,None]          # SB net : call de l'iso-raise (offset de la main du SB)
    C=T35*x-d35[None,:]         # SB net : call du raise 3,5 (offset de la main du BB)
    return C,Cl,Ci
def evaluate(S,fin,minreach=0.003):
    s,nodes=load('hu',HU[S]); st=stacks_of(s); ix=index_nodes(s,nodes); path,g=path_probs(nodes,st)
    MAP={'':('root',['F','C','R3.5','A']),'0C':('bl',['X','R3','A']),'0R3.5':('bvr',['F','C','A']),'0RA':('bvs',['F','C']),
         '0C-1RA':('sl',['F','C']),'0C-1R3':('si',['F','C','A']),'0C-1R3-0RA':('c4',['F','C']),'0R3.5-1RA':('s3',['F','C'])}
    tl=tt=tr=0
    for key,(mk,labs_m) in MAP.items():
        if key not in ix: continue
        n=nodes[ix[key]]; labs=act_labels(n,st)
        wts=np.array([n['hands'][x]['weight'] for x in NAMES]); mass=W*wts
        if mass.sum()<=0: continue
        pl=n['player']; others=1.0; allr=1.0
        for (p_,gp) in path[ix[key]]:
            allr*=gp
            if p_!=pl: others*=gp
        if allr<minreach: continue
        weight=others*mass.sum()/W.sum()
        played=np.array([[n['hands'][x]['played'][j] for j in range(len(labs))] for x in NAMES]); evs=np.array([[n['hands'][x]['evs'][j] for j in range(len(labs))] for x in NAMES])
        Mm=fin[mk]; M=np.zeros((169,len(labs)))
        for j,l in enumerate(labs):
            if l in labs_m: M[:,j]=Mm[:,labs_m.index(l)]
        M=M/np.maximum(M.sum(1,keepdims=True),1e-12)
        tv=0.5*float((mass[:,None]*np.abs(M-played)).sum()/mass.sum()); loss=float((mass*(evs.max(1)-(M*evs).sum(1))).sum()/mass.sum())
        tl+=weight*loss; tt+=weight*tv; tr+=weight
    return 1000*tl,tt/tr
if __name__=='__main__':
    print("Solveur heads-up avec limp/raise et correction post-flop apprise sur HRC")
    for S in [6,8,10,12]:
        w_=np.ones(169); 
        for label,excl in [("dans l'échantillon",()),("stack retiré",(S,))]:
            p=payoffs(S,excl); C,Cl,Ci=build(p,S)
            fin=solve3(E,W,S,o=3.5,ri=3.0,iters=2500,overrides=(C,Cl,Ci),compute_expl=False)
            l,tv=evaluate(S,fin)
            print(f"  HU {S:>2} BB {label:20s}: perte {l:6.1f} mBB (réf. plancher ~2-8), TV {100*tv:4.1f}%",flush=True)
