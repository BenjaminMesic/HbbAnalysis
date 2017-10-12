# Hbb tool

Tool developed and used for my analysis/disertation in WHbb channel (boosted topology).
Following instructions will get you a copy of the project up and running on your machine.

Features:
* Copying data/ntuples from any location on the grid and preserving their directory structure while being copied. Option to check if some files are missing in original location by doing binary search.
* Easy addition of new variables (int, float, list, ...) both for C++ and PYTHON function or just removal of not used variables in the ntuples.
* Skimming data in layers.
* Batch (condor for now but easy to add lxbatch if needed) for all the tasks: copying, skimming, making new ntuples.
* Possible to work on merged or unmerged files separately.
* Making plots, datacards

## Getting Started

### Prerequisites

You need to install at least CMSSW_9_4_0_pre1 since it has installed [Keras](https://github.com/fchollet/keras). Hbb tool (for now) doesn't contain tool/scripts for doing training itself but only for deploying already trained networks.


```
cmsrel CMSSW_9_4_0_pre1
cd CMSSW_9_4_0_pre1/src/; cmsenv
git clone https://github.com/BenjaminMesic/HbbAnalysis.git  
cd HbbAnalysis 

Note: 
If DAS needed: voms-proxy-init --voms cms --valid 168:00
```

### Installing

A step by step series of examples that tell you have to get a environment running.

You need to always setup environment by running one of the shell scripts.
```
source setup_environment.sh
source setup_environment.csh
```

Only when using first time (or want to add another analysis) open [setup.py](https://github.com/BenjaminMesic/HbbAnalysis/blob/master/setup.py#L18-L19) and give
the analysis name and location of samples. By default they are set to

```
  analysis_name             = 'Wlv'
  path_samples              = '/STORE/Hbb/2017_04_VHBBHeppyV25'
```
By running this script you will create a folder called 'Wlv' (or any other name you give)
in [analysis directory](https://github.com/BenjaminMesic/HbbAnalysis/tree/master/analysis) which will contain all the necessary config files for the analysis. Also, all the results
will be automatically stored inside. Config files are pulled from [templates](https://github.com/BenjaminMesic/HbbAnalysis/tree/master/utility/templates/configuration).

## Running the code

### Configuration

If you open configuration files you will see that there are a lot of comments
and that the configs are self explanatory.

But anyway, more detailed explanation coming soon.

### Aux

All the auxilary files required for the code working properly.
It contains folder with the weights and scale factors and also 
neural networks which are necessary for additional variables in my analysis.
Other aux files should be added here.

### Steps
In this folder are scripts which run the code. For now
each step has its own script. Each script has different options
which need to be uncommented manually depending on what you need.
After you setup all the configuration files you can run the first step which will
look for all the files, check if the structure is ok, etc.

```
python step/_1_copy_samples.py 
```
NOTE: All the tasks in each step are by default commented so you won't get any output results.


### Utils
 More detailed explanation (if requested) coming soon.

## Built With
* [CMSSW](https://github.com/cms-sw/cmssw) - Heart of our experiment.

## Contributing
If you want to contribute please send me message :)

## Versioning
No versioning yet.

## Authors
* **Benjamin Mesic**

## License
No license.

## Acknowledgments
Some functions and workflow borrowed from 
* [PrincetonAnalysisTools](https://github.com/scooperstein/PrincetonAnalysisTools/tree/master/VHbbAnalysis)
* [Xbb](https://github.com/perrozzi/Xbb)
