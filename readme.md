# Welcome to Hbb Code :)

Description:  
Hbb analysis code written in Python.  

Instructions:  

1. cmsrel CMSSW_7_1_16 (it should work with any other as well)  
2. cd CMSSW_7_1_16/src/; cmsenv
3. git clone https://github.com/BenjaminMesic/HbbAnalysis.git  
4. cd HbbAnalysis 

If you just got the Hbb code:

	5. source setup_environment.sh

	6. In install.py set path for samples and analysis name  
		samples_directory 	= '/STORE/Hbb/2016_08_VHBBHeppyV21'  
		analysis_name 		= 'Wlv'  

	   python install.py

Else just:
	5. source setup_environment.sh


Note:
- If DAS needed: voms-proxy-init --voms cms --valid 168:00