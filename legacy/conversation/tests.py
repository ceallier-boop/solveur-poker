import numpy as np, pickle, time
from numba import njit
import crsolve as cs
from pushfold import eval7, build_classes
combos,nc,names=build_classes()
E=np.load('E_final.npy'); T=np.load('T_final.npy')
P=pickle.load(open('final_strats.pkl','rb')); res3=P['res3']; resHU=P['resHU']; pm3=P['pm3']; pmHU=P['pmHU']
th=cs.ThreeHanded(E,T,cr=True)
idx={n:i for i,n in enumerate(names)}
# ---------- combos
allc=[];allcls=[]
for i in range(169):
    for k in range(nc[i]): allc.append((combos[i,k,0],combos[i,k,1])); allcls.append(i)
allc=np.array(allc,dtype=np.int64); allcls=np.array(allcls,dtype=np.int64)

@njit(cache=True)
def showdown(h,nh,used,S_nh):
    # h: (3,2) cartes ; renvoie parts (3,) pour les nh premiers joueurs
    bd=np.zeros(5,np.int64); m=0
    u=used.copy()
    while m<5:
        x=np.random.randint(52)
        if not u[x]: u[x]=True; bd[m]=x; m+=1
    cards=np.zeros(7,np.int64); sc=np.zeros(3,np.int64); best=-1
    for p in range(nh):
        cards[0]=h[p,0]; cards[1]=h[p,1]
        for q in range(5): cards[2+q]=bd[q]
        sc[p]=eval7(cards)
        if sc[p]>best: best=sc[p]
    nw=0
    for p in range(nh):
        if sc[p]==best: nw+=1
    out=np.zeros(3)
    for p in range(nh):
        if sc[p]==best: out[p]=1.0/nw
    return out

@njit(cache=True)
def sim(mode, hero, allc, allcls, combos, nc, pB,aS,cS,d1,d2,d3, S, N, seed):
    np.random.seed(seed)
    tot=0.0
    h=np.zeros((3,2),np.int64); used=np.zeros(52,np.bool_)
    done=0
    while done<N:
        used[:]=False
        ok=True
        # joueur 0 = BTN, 1 = SB, 2 = BB ; le heros est a sa place selon mode
        cl=np.zeros(3,np.int64)
        for p in range(3):
            if (mode==0 and p==0) or (mode in (1,2) and p==1) or (mode in (3,4) and p==2):
                k=np.random.randint(nc[hero]); c0=combos[hero,k,0]; c1=combos[hero,k,1]; cl[p]=hero
            else:
                j=np.random.randint(1326); c0=allc[j,0]; c1=allc[j,1]; cl[p]=allcls[j]
            if used[c0] or used[c1]: ok=False; break
            used[c0]=True; used[c1]=True; h[p,0]=c0; h[p,1]=c1
        if not ok: continue
        done+=1
        r=np.random.random(); r2=np.random.random(); r3=np.random.random()
        btn_push = r<pB[cl[0]]
        pay=0.0
        if mode==0:   # BTN pousse (hero BTN) -> EV du push
            sb_call = r2<cS[cl[1]]
            if sb_call: bb_call = r3<d3[cl[2]]
            else: bb_call = r3<d2[cl[2]]
            if (not sb_call) and (not bb_call): pay=1.5
            elif (not sb_call) and bb_call:
                hh=np.zeros((3,2),np.int64); hh[0]=h[0]; hh[1]=h[2]
                s=showdown(hh,2,used,0); pay=s[0]*(2*S+0.5)-S
            elif sb_call and (not bb_call):
                hh=np.zeros((3,2),np.int64); hh[0]=h[0]; hh[1]=h[1]
                s=showdown(hh,2,used,0); pay=s[0]*(2*S+1)-S
            else:
                s=showdown(h,3,used,0); pay=s[0]*3*S-S
        elif mode==1:  # hero SB, BTN fold, SB pousse
            if not btn_push:
                bb_call = r3<d1[cl[2]]
                if not bb_call: pay=1.0
                else:
                    hh=np.zeros((3,2),np.int64); hh[0]=h[1]; hh[1]=h[2]
                    s=showdown(hh,2,used,0); pay=s[0]*2*S-S
        elif mode==2:  # hero SB, BTN push : SB call (EV du call, BB repond d3)
            if btn_push:
                bb_call = r3<d3[cl[2]]
                if not bb_call:
                    hh=np.zeros((3,2),np.int64); hh[0]=h[1]; hh[1]=h[0]
                    s=showdown(hh,2,used,0); pay=s[0]*(2*S+1)-S
                else:
                    hh=np.zeros((3,2),np.int64); hh[0]=h[1]; hh[1]=h[0]; hh[2]=h[2]
                    s=showdown(hh,3,used,0); pay=s[0]*3*S-S
        elif mode==3:  # hero BB, BTN fold, SB push, BB call
            sb_push = r2<aS[cl[1]]
            if (not btn_push) and sb_push:
                hh=np.zeros((3,2),np.int64); hh[0]=h[2]; hh[1]=h[1]
                s=showdown(hh,2,used,0); pay=s[0]*2*S-S
        else:          # mode 4 : hero BB, BTN push, SB call, BB call
            sb_call = r2<cS[cl[1]]
            if btn_push and sb_call:
                hh=np.zeros((3,2),np.int64); hh[0]=h[2]; hh[1]=h[0]; hh[2]=h[1]
                s=showdown(hh,3,used,0); pay=s[0]*3*S-S
        tot+=pay
    return tot/N

S=10; f=res3[S]; pB,aS,cS,d1,d2,d3=[f[k] for k in ['btn','s1','sc','b1','b2','b3']]
btn,s1,sc,b1,b2,b3,cbb=th.node_cfvs(S,pB,aS,cS,d1,d2,d3)
print("== TEST 1 : simulation complète avec vraies cartes vs modèle (S=10 BB)")
print("noeud | main | modèle | simulation | écart")
rows=[]
N=2500000
for name in ['AA','AKo','A5s','T9s','72o','22']:
    h=idx[name]
    tests=[('BTN push',0,btn[h]),('SB open-shove',1,s1[1][h]),('SB call vs BTN',2,sc[1][h]),
           ('BB call vs SB',3,b1[1][h]),('BB call vs BTN+SB',4,b3[1][h])]
    for lab,mode,model in tests:
        t=sim(mode,h,allc,allcls,combos,nc,pB,aS,cS,d1,d2,d3,S,N,mode*100+h)
        rows.append(abs(t-model))
        print(f"{lab:18s} {name:4s} {model:+.4f} {t:+.4f} {t-model:+.4f}")
print("écart absolu moyen : %.4f BB ; max : %.4f BB"%(np.mean(rows),np.max(rows)))

print("\n== TEST 2 : bruit Monte Carlo (données indépendantes a vs b), écart moyen pondéré de fréquence | mains avec écart >50%")
A=pickle.load(open('noise_a.pkl','rb')); B=pickle.load(open('noise_b.pkl','rb'))
nodes=['btn','s1','sc','b1','b2','b3']
for S_ in (6,10,15):
    s=f"S={S_:>2}: "
    for k in nodes:
        d=np.abs(A[S_][k]-B[S_][k]); s+=f"{k} {100*(pm3*d).sum():.1f}%/{int((d>0.5).sum())} | "
    print(s)

print("\n== TEST 3 : convergence (2000 itérations vs 5000), S=10")
g=th.solve(10,iters=2000)
print({k:round(100*float((pm3*np.abs(g[k]-res3[10][k])).sum()),2) for k in nodes},"(% de fréquence moyen)")

print("\n== TEST 4 : cohérence (main plus forte jouée moins souvent que plus faible, écart >0.25)")
def order_pairs():
    pr=[]
    meta=[]
    for row in range(13):
        for col in range(13):
            if row==col: meta.append(('p',12-row,12-row))
            elif row<col: meta.append(('s',12-row,12-col))
            else: meta.append(('o',12-col,12-row))
    where={m:i for i,m in enumerate(meta)}
    for (k,h,l),i in where.items():
        if k=='p' and h<12: pr.append((where[('p',h+1,h+1)],i))   # plus forte, plus faible
        if k in('s','o') and l<h-1: pr.append((where[(k,h,l+1)],i))
        if k in('s','o') and h<12: pr.append((where[(k,h+1,l)],i)) if h+1!=l else None
        if k=='o': pr.append((where[('s',h,l)],i))
    return pr
PR=order_pairs()
tot=0;viol=0;detail=[]
for S_,f in res3.items():
    for k in nodes:
        v=sum(1 for a,b in PR if f[k][b]>f[k][a]+0.25); viol+=v; tot+=len(PR)
        if v: detail.append((S_,k,v))
print(f"{viol} violations sur {tot} comparaisons (6 stacks x 6 noeuds)", detail[:12])

print("\n== TEST 5 : emboîtement entre stacks (range à stack plus petit doit contenir celle du plus grand)")
ss=sorted(res3)
for k in nodes:
    worst=0;cnt=0
    for a,b in zip(ss[:-1],ss[1:]):
        d=res3[b][k]-res3[a][k]   # >0 : joue plus au grand stack -> anomalie
        cnt+=int((d>0.25).sum()); worst=max(worst,float(d.max()))
    print(f"{k}: {cnt} anomalies (plus de 25 pts), pire {100*worst:.0f} pts")

print("\n== TEST 6 : coût de la simplification (arrondi à 0/100 % au seuil 50 %), en mBB/main d'écart à l'équilibre")
for S_ in ss:
    f=res3[S_]
    r=[(f[k]>=0.5).astype(float) for k in nodes]
    u,br=th.values(S_,r)
    print(f"S={S_:>2}: exploitabilité arrondie {1000*(sum(br)-sum(u)):.1f} mBB (stratégie mixte : {1000*f['expl']:.2f})")
