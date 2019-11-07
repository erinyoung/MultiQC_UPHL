# MultiQC_UPHL

**MultiQC_UPHL is a plugin for MultiQC, providing additional tools which are specific to the Public Health Pipelines at the Utah Public Health Laboratory (UPHL) and related public health entities**

This module provides visualizations for 
* [abricate](https://github.com/tseemann/abricate): produces a heatmap with genes and samples
![alt text](https://uphl.utah.gov/wp-content/uploads/New-UPHL-Logo.png)
* [mash](https://github.com/marbl/Mash): produces a bargraph of p-value = 0 
* [cg-pipeline](https://github.com/lskatz/CG-Pipeline): produces a table
* [roary](https://sanger-pathogens.github.io/Roary/): produces multiqc graphs including QC, unique genes, and total genes
* [guppy]() # not currently included
* [seqsero](https://github.com/denglab/SeqSero): produces a table of seqsero results
* [blobtools](https://blobtools.readme.io/docs/what-is-blobtools): produces a bargraph of observed species and other metrics
* [Unicycler](https://github.com/rrwick/Unicycler) # not currently included
* [nanopolish](https://nanopolish.readthedocs.io/en/latest/) # not currently included

## Installation
To run this tool, you must have MultiQC installed. You can install both
MultiQC and this package with the following command:
***WARNING: Currently does not work***
```
pip install multiqc git+https://github.com/Ikkik/MultiQC_UPHL.git
```
and updating is possible with
```
pip install --upgrade multiqc git+https://github.com/Ikkik/MultiQC_UPHL.git
```

It can also be installed with git:
```
git clone https://github.com/Ikkik/MultiQC_UPHL.git
cd MultiQC_UPHL
git init
python setup.py install
```
and updated with  
```
cd MultiQC_UPHL
git pull
python setup.py install
```
