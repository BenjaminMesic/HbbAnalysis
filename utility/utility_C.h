#include "TLorentzVector.h"
#include "TMath.h"
#include "TVector2.h"
#include "TVector3.h"	

double deltaPhi(double phi1, double phi2) {
	double result = phi1 - phi2;
	if (result > TMath::Pi()) {
		result -= 2*TMath::Pi();
	} else if (result <= -TMath::Pi()) {
		result += 2*TMath::Pi();
	}
	return result;
}

double deltaR(double eta1, double phi1, double eta2, double phi2) {
	double deta = eta1 - eta2;
	double dphi = deltaPhi(phi1, phi2);
	return TMath::Sqrt(deta*deta + dphi*dphi);
}

double invariant_mass(double pt_1, double eta_1, double phi_1, double mass_1, double pt_2, double eta_2, double phi_2, double mass_2) {
	TLorentzVector v_1;
	TLorentzVector v_2;
	TLorentzVector v;

	v_1.SetPtEtaPhiM( pt_1, eta_1, phi_1, mass_1);
	v_2.SetPtEtaPhiM( pt_2, eta_2, phi_2, mass_2);
	v = v_1 + v_2;

	return v.M();
}