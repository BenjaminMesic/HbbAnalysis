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