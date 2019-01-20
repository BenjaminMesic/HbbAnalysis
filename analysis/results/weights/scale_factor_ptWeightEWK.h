// from https://twiki.cern.ch/twiki/bin/view/CMS/VHiggsBBCodeUtils#V_X_QCD_and_EWK_corrections
float scale_factor_ptWeightEWK(int nGenVbosons,float GenVbosons_pt,int Vtype,int GenVbosons_pdgId){
    float SF = 1.;
    if (nGenVbosons ==1){
        if (Vtype == 0 || Vtype == 1 || Vtype == 4 || Vtype == 5){
            if (GenVbosons_pdgId == 23){
                //for Z options
                if (GenVbosons_pt > 100. && GenVbosons_pt < 3000) SF = -0.1808051+6.04146*(TMath::Power((GenVbosons_pt+759.098),-0.242556));
            }
        } else if (Vtype == 2 || Vtype == 3){
            //for W options
            if (GenVbosons_pdgId == 24 || GenVbosons_pdgId == -24){
                if (GenVbosons_pt > 100. && GenVbosons_pt < 3000) SF = -0.830041+7.93714*(TMath::Power((GenVbosons_pt+877.978),-0.213831));
            }
        }
    }
    return SF>0?SF:0;
}