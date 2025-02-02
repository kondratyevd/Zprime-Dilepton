import numpy as np
import math

from python.utils import p4_sum, delta_r, cs_variables


def find_dimuon(objs):
    objs1=objs[objs.charge>0]
    objs2=objs[objs.charge<0]
    objs1['mu_idx'] = objs1.index
    objs2['mu_idx'] = objs2.index
    '''
    px1 = objs1.pt * np.cos(objs1.phi)
    py1 = objs1.pt * np.sin(objs1.phi)
    pz1 = objs1.pt * np.sinh(objs1.eta)
    e1 = np.sqrt(px1**2 + py1**2 + pz1**2 + objs1.mass**2)
    px2 = objs2.pt * np.cos(objs2.phi)
    py2 = objs2.pt * np.sin(objs2.phi)
    pz2 = objs2.pt * np.sinh(objs2.eta)
    e2 = np.sqrt(px2**2 + py2**2 + pz2**2 + objs2.mass**2)

    pairs_m = 2*(0.511**2 + (np.array([e1]).T).dot([e2]) - (np.array([px1]).T).dot([px2]) - (np.array([py1]).T).dot([py2]) - (np.array([pz1]).T).dot([pz2]))
    pairs_m = np.sqrt(pairs_m)
    n = len(e1)+len(e2)
    if n == 2:
        return [objs1.iloc[0].mu_idx, objs2.iloc[0].mu_idx, pairs_m]

    ind = np.argmin(np.abs(pairs_m - 91.1876))
    ind = np.unravel_index(ind, pairs_m.shape)
    mass = pairs_m[ind]
    if abs(mass-91.1876) < 20:
        return [objs1.iloc[ind[0]].mu_idx, objs2.iloc[ind[1]].mu_idx, mass]
    else:
        idx1=objs1.pt.idxmax()
        idx2=objs2.pt.idxmax()
        #mass = pairs_m[(idx1[1],idx)] 
        return [idx1, idx2, mass]
    #if objs1.shape[0]==0:
    #    print("obj1 empty")
    #if objs2.shape[0]==0:
    #    print("obj2 empty")
    '''

    dmass=20.
    for i in range(objs1.shape[0]):
        for j in range(objs2.shape[0]):
            #print(objs1.iloc[i].pt)
            #print(objs2.iloc[j].pt)
            px1_ = objs1.iloc[i].pt * np.cos(objs1.iloc[i].phi) 
            py1_ = objs1.iloc[i].pt * np.sin(objs1.iloc[i].phi) 
            pz1_ = objs1.iloc[i].pt * np.sinh(objs1.iloc[i].eta)
            e1_ = np.sqrt(px1_**2 + py1_**2 + pz1_**2 + objs1.iloc[i].mass**2)
            px2_ = objs2.iloc[j].pt * np.cos(objs2.iloc[j].phi)
            py2_ = objs2.iloc[j].pt * np.sin(objs2.iloc[j].phi)
            pz2_ = objs2.iloc[j].pt * np.sinh(objs2.iloc[j].eta)
            e2_ = np.sqrt(px2_**2 + py2_**2 + pz2_**2 + objs2.iloc[j].mass**2)
            m2 = (e1_+e2_)**2-(px1_+px2_)**2-(py1_+py2_)**2-(pz1_+pz2_)**2
            mass=math.sqrt(max(0,m2))
            if abs(mass-91.1876)<dmass:
                dmass=abs(mass-91.1876)
                obj1_selected=objs1.iloc[i]
                obj2_selected=objs2.iloc[j]
                idx1=objs1.iloc[i].mu_idx
                #print("        idx1=",idx1)
                idx2=objs2.iloc[j].mu_idx
                dimuon_mass=mass
    if dmass==20:
        obj1 = objs1.loc[objs1.pt.idxmax()]         
        obj2 = objs2.loc[objs2.pt.idxmax()]
        px1_ = obj1.pt * np.cos(obj1.phi)    
        py1_ = obj1.pt * np.sin(obj1.phi)  
        pz1_ = obj1.pt * np.sinh(obj1.eta)
        e1_ = np.sqrt(px1_**2 + py1_**2 + pz1_**2 + obj1.mass**2)
        px2_ = obj2.pt * np.cos(obj2.phi)
        py2_ = obj2.pt * np.sin(obj2.phi)
        pz2_ = obj2.pt * np.sinh(obj2.eta)
        e2_ = np.sqrt(px2_**2 + py2_**2 + pz2_**2 + obj2.mass**2)
        m2 = (e1_+e2_)**2-(px1_+px2_)**2-(py1_+py2_)**2-(pz1_+pz2_)**2
        mass=math.sqrt(max(0,m2))
        dimuon_mass=mass
        obj1_selected = obj1
        obj2_selected = obj2
        idx1=objs1.pt.idxmax()
        idx2=objs2.pt.idxmax()
    if obj1_selected.pt>obj2_selected.pt:
        #return pd.Series([idx1,idx2,dimuon_mass],index=['idx1','idx2', 'mass'])
        return [idx1,idx2,dimuon_mass]
    else:
        #return pd.Series([idx2,idx1,dimuon_mass],index=['idx1','idx2', 'mass'])
        return [idx2,idx1,dimuon_mass] 


def fill_muons(processor, output, mu1, mu2, dimuon_mass, is_mc):
    mu1_variable_names = [
        'mu1_pt', 'mu1_pt_over_mass', 'mu1_ptErr',
        'mu1_eta', 'mu1_phi', 'mu1_iso'
    ]
    mu2_variable_names = [
        'mu2_pt', 'mu2_pt_over_mass', 'mu2_ptErr',
        'mu2_eta', 'mu2_phi', 'mu2_iso'
    ]
    dimuon_variable_names = [
        'dimuon_mass',
        'dimuon_mass_res', 'dimuon_mass_res_rel',
        'dimuon_ebe_mass_res', 'dimuon_ebe_mass_res_rel',
        'dimuon_pt', 'dimuon_pt_log',
        'dimuon_eta', 'dimuon_phi',
        'dimuon_dEta', 'dimuon_dPhi',
        'dimuon_dR', 'dimuon_rap', 'bbangle',
        'dimuon_cos_theta_cs', 'dimuon_phi_cs', 'wgt_nominal'
    ]
    v_names = (
        mu1_variable_names +
        mu2_variable_names +
        dimuon_variable_names
    )
    
    # Initialize columns for muon variables

    for n in (v_names):
        output[n] = 0.0

    # Fill single muon variables

    for v in ['pt', 'ptErr', 'eta', 'phi']:
        output[f'mu1_{v}'] = mu1[v]
        output[f'mu2_{v}'] = mu2[v]
    output['mu1_iso'] = mu1.tkRelIso
    output['mu2_iso'] = mu2.tkRelIso
    output.dimuon_mass=dimuon_mass
    output['mu1_pt_over_mass'] = output.mu1_pt.values / output.dimuon_mass.values
    output['mu2_pt_over_mass'] = output.mu2_pt.values / output.dimuon_mass.values

    # Fill dimuon variables

    mm = p4_sum(mu1, mu2)
    for v in ['pt', 'eta', 'phi', 'mass', 'rap']:
        name = f'dimuon_{v}'
        output[name] = mm[v]
        output[name] = output[name].fillna(-999.)

    output['dimuon_pt_log'] = np.log(output.dimuon_pt[output.dimuon_pt>0])
    output.loc[output.dimuon_pt<0, 'dimuon_pt_log']=-999.

    mm_deta, mm_dphi, mm_dr = delta_r(
        mu1.eta, mu2.eta,
        mu1.phi, mu2.phi
    )
    output['dimuon_pt'] = mm.pt
    output['dimuon_eta'] = mm.eta
    output['dimuon_phi'] = mm.phi
    output['dimuon_dEta'] = mm_deta
    output['dimuon_dPhi'] = mm_dphi
    output['dimuon_dR'] = mm_dr

    output['dimuon_ebe_mass_res'] = mass_resolution(
        is_mc,
        processor.evaluator,
        output,
        processor.year
    )
    output['dimuon_ebe_mass_res_rel'] = (
        output.dimuon_ebe_mass_res / output.dimuon_mass
    )
    output['dimuon_cos_theta_cs'],\
        output['dimuon_phi_cs'] = cs_variables(mu1, mu2)


def mass_resolution(is_mc, evaluator, df, year):
    # Returns absolute mass resolution!
    dpt1 = (df.mu1_ptErr * df.dimuon_mass) / (2 * df.mu1_pt)
    dpt2 = (df.mu2_ptErr * df.dimuon_mass) / (2 * df.mu2_pt)

    if is_mc:
        label = f"res_calib_MC_{year}"
    else:
        label = f"res_calib_Data_{year}"
    calibration = np.array(
        evaluator[label](
            df.mu1_pt.values,
            abs(df.mu1_eta.values),
            abs(df.mu2_eta.values)
        )
    )

    return np.sqrt(dpt1 * dpt1 + dpt2 * dpt2) * calibration
