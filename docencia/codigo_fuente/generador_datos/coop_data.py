import numpy as np, pandas as pd

def make_cooperativa_dataset(n=8000, seed=2026):
    """Synthetic micro-credit dataset for a FICTIONAL Ecuadorian savings & credit cooperative.
    Target: mora_30d = 1 if the member fell >30 days behind on the loan."""
    rng = np.random.default_rng(seed)
    provincias = ["Pichincha","Guayas","Azuay","Tungurahua","Chimborazo","Imbabura","Manabí","Loja","Cotopaxi","El Oro"]
    p_prov = np.array([.20,.18,.10,.10,.09,.08,.08,.06,.06,.05])
    sectores = ["comercio","agricultura","servicios","transporte","artesania","manufactura"]
    p_sec = np.array([.32,.22,.18,.10,.10,.08])
    provincia = rng.choice(provincias, n, p=p_prov)
    sector = rng.choice(sectores, n, p=p_sec)
    rural_p = np.where(np.isin(provincia,["Chimborazo","Cotopaxi","Loja","Imbabura"]),0.6,0.3)
    zona = np.where(rng.random(n)<rural_p,"rural","urbana")
    edad = np.clip(rng.normal(41,11,n),19,75).round().astype(int)
    sec_mult = pd.Series({"comercio":1.0,"agricultura":0.8,"servicios":1.15,"transporte":1.25,"artesania":0.85,"manufactura":1.1})
    ingreso = np.round(rng.lognormal(np.log(620),0.45,n)*sec_mult[sector].values*np.where(zona=="rural",0.85,1.0),2)
    plazo = rng.choice([6,12,18,24,36,48], n, p=[.10,.25,.20,.20,.15,.10])
    monto = np.round(np.clip(ingreso*rng.lognormal(np.log(4.5),0.55,n)*(plazo/18)**0.5,300,40000),-1)
    r = 0.18/12  # fictional fixed annual rate 18%
    cuota = np.round(monto*r/(1-(1+r)**(-plazo)),2)
    ratio = cuota/ingreso
    antig = np.round(rng.exponential(40,n)).astype(int)
    previos = rng.poisson(antig/30)
    atrasos = rng.poisson(0.35+0.25*(ratio>0.4),n)
    garante = (rng.random(n)<0.42).astype(int)
    ahorro = np.round(ingreso*rng.lognormal(np.log(0.8),0.8,n)*(1+antig/60),2)
    # latent risk (nonlinear, with interactions)
    logit = (-3.2
        + 3.2*np.tanh(4*np.maximum(ratio-0.32,0))            # saturating hinge: payment burden
        + 0.9*np.minimum(atrasos,2)
        - 1.4*(1-np.exp(-antig/18))                           # saturating seniority effect
        + 0.0025*(edad-44)**2                                 # U-shape in age
        + 1.8*((sector=="agricultura")&(plazo<=12))           # short loans vs harvest cycles
        - 1.4*garante*(ratio<0.45) + 0.8*garante*(ratio>=0.45)# guarantor helps only if burden is sane
        - 0.5*np.log1p(ahorro/ingreso)
        + 0.6*(zona=="rural")*(sector!="agricultura")
        + 0.3*(previos==0))
    p = 1/(1+np.exp(-logit))
    y = (rng.random(n)<p).astype(int)
    return pd.DataFrame(dict(edad=edad,provincia=provincia,zona=zona,sector=sector,ingreso_mensual=ingreso,
        monto_credito=monto,plazo_meses=plazo,cuota_mensual=cuota,
        antiguedad_socio_meses=antig,creditos_previos=previos,atrasos_previos_12m=atrasos,tiene_garante=garante,
        ahorro_promedio=ahorro,mora_30d=y))
