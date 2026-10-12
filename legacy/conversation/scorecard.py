import numpy as np, json, csv
from hrcdata import *
import eval_vs_hrc as ev
import hrc_surrogate as hs
THR_NOISE=3e-3; THR_SIG=1e-2          # BB : <=3 mBB bruit HRC ; >10 mBB significatif
def wcorr(a,b,w):
    ma=np.average(a,weights=w); mb=np.average(b,weights=w)
    va=np.average((a-ma)**2,weights=w); vb=np.average((b-mb)**2,weights=w)
    if va<1e-12 or vb<1e-12: return np.nan
    return float(np.average((a-ma)*(b-mb),weights=w)/np.sqrt(va*vb))
def score(node,st,labs,M,decide):
    """M : (169,nA) distribution du modèle alignée sur les actions HRC ; decide : indices d'action décidés par le modèle"""
    wts=np.array([node['hands'][x]['weight'] for x in NAMES]); mass=W*wts; tot=mass.sum()
    played=np.array([[node['hands'][x]['played'][j] for j in range(len(labs))] for x in NAMES])
    evs=np.array([[node['hands'][x]['evs'][j] for j in range(len(labs))] for x in NAMES])
    tv=0.5*np.abs(M-played).sum(1)
    hd=played.argmax(1)                              # décision dominante HRC
    same=(decide==hd)
    best=evs.max(1); got=(M*evs).sum(1); loss=best-got
    # une décision différente est « sans conséquence » si la perte d'EV reste au niveau du bruit de HRC
    useful=same|(loss<=THR_NOISE)
    sig=loss>THR_SIG; diff=~same
    gtop=int(np.argmax((mass[:,None]*played).sum(0)))
    r=wcorr(M[:,gtop],played[:,gtop],mass)
    lossmass=float((mass*loss).sum())
    return dict(mae=100*float((mass*tv).sum()/tot),rmse=100*float(np.sqrt((mass*tv**2).sum()/tot)),corr=r,
                agree=100*float((mass*same).sum()/tot),useful=100*float((mass*useful).sum()/tot),
                diff_noconseq=100*float((mass*(diff&(loss<=THR_SIG))).sum()/max((mass*diff).sum(),1e-12)),
                sig_rate=100*float((mass*sig).sum()/tot),loss=1000*lossmass/tot,
                sig_share_of_loss=100*float((mass*loss*sig).sum()/max(lossmass,1e-12)))
rows=[]
def add(model,kind,S,key_name,m,reach=None):
    rows.append(dict(model=model,kind=kind,stack=S,node=key_name,reach=reach,**m))
# ---------- M1 : push/fold maison
SC=[('3w',8),('3w',7),('3w',6),('hu',22),('hu',21),('hu',20),('hu',19),('hu',18),('hu',17)]
for kind,h in SC:
    s,nodes=load(kind,h); st=stacks_of(s); ix=index_nodes(s,nodes); S=st[0]
    model=ev.models_for(kind,st); path_,g_=ev.path_probs(nodes,st)
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
        decide=np.where(v>=0.5,idx,fi)
        rr=1.0
        for (p_,gp) in path_[ix[key]]: rr*=gp
        add('push/fold',kind,S,name,score(node,st,labs,M,decide),rr)
# ---------- M2 : modèle corrigé, stack retiré puis interpolé (3 joueurs 10, 12 ; HU 6, 8, 10, 12)
def corrected(kind,S,hybrid=False):
    h=(hs.EQ3 if kind=='3w' else hs.EQHU)[S]
    s,nodes=load(kind,h); st=stacks_of(s); ix=index_nodes(s,nodes); path,g=ev.path_probs(nodes,st); out=[]
    for key,i in ix.items():
        n=nodes[i]; labs=act_labels(n,st)
        allr=1.0
        for (p_,gp) in path[i]: allr*=gp
        if allr<0.01: continue
        wts=np.array([n['hands'][x]['weight'] for x in NAMES])
        if (W*wts).sum()<=0: continue
        sg=hs.surrogate(kind,S,key,(S,)) if not hybrid else hybrid_sur(kind,S,key)
        if sg is None: continue
        slabs,F,_=sg; M=np.zeros((169,len(labs)))
        for j,l in enumerate(labs):
            if l in slabs: M[:,j]=F[:,slabs.index(l)]
        M=M/np.maximum(M.sum(1,keepdims=True),1e-12)
        out.append((key,n,st,labs,M,allr))
    return out
def hybrid_sur(kind,S,key):
    av=hs.stacks_avail(kind,(S,))
    lo=max([x for x in av if x<S],default=None); hi=min([x for x in av if x>S],default=None)
    if lo is not None and hi is not None and hi-lo<=4: return hs.surrogate(kind,S,key,(S,))
    cand=[x for x in av if hs._at(kind,x,key) is not None]
    if not cand: return None
    b=min(cand,key=lambda x:(abs(x-S),x)); n=hs._at(kind,b,key); return n['labels'],n['played'].copy(),n['w'].copy()
def name_of(key,kind):
    return {'':'premier acteur','0F':'SB après fold BTN','0C':'BB face au limp','0RA':'face à un all-in','0R3.5':'BB face au raise 3,5'}.get(key,key)
for kind,Ss in [('hu',[6,8,10,12]),('3w',[10,12])]:
    for S in Ss:
        for mdl,hyb in [('corrigé',False)]:
            for key,n,st,labs,M,allr in corrected(kind,S,hyb):
                add(mdl,kind,S,f"{key or 'racine'} ({'+'.join(labs)})",score(n,st,labs,M,M.argmax(1)),allr)
with open('scorecard.csv','w',newline='') as f:
    w_=csv.DictWriter(f,fieldnames=['model','kind','stack','node','reach','mae','rmse','corr','agree','useful','diff_noconseq','sig_rate','loss','sig_share_of_loss']); w_.writeheader(); w_.writerows(rows)
json.dump(rows,open('scorecard.json','w'))
print(len(rows),"lignes")
