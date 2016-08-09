Description:  
Hbb analysis code written in Python.  

Instructions:  

1. cmsrel CMSSW_7_1_16 (it should work with any other as well)  
2. cd CMSSW_7_1_16/src/; cmsenv; cd ../python  
3. git clone https://github.com/BenjaminMesic/HbbAnalysis.git  
4. cd HbbAnalysis  
5. In setup.py set path for samples and analysis name  
	samples_directory 	= '/STORE/Hbb/2016_08_VHBBHeppyV21'  
	analysis_name 		= 'Wlv'  
6. python setup.py  