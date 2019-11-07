#!/usr/bin/env python
"""
MultiQC_UPHL is a plugin for MultiQC for Public Health Bioinformatic pipelines.

For more information about MultiQC, see http://multiqc.info
"""

from setuptools import setup, find_packages

setup(
    name = 'multiqc_uphl',
    version = '2019.11.05',
    author = 'Phil Ewels',
    author_email = 'eriny@utah.gov',
    description = "MultiQC plugin for the Utah Public Health Laboratory",
    long_description = __doc__,
    keywords = 'bioinformatics',
    url = 'https://github.com/Ikkik/MultiQC_UPHL',
    download_url = 'https://github.com/Ikkik/MultiQC_UPHL/releases',
    license = 'MIT',
    packages = find_packages(),
    include_package_data = True,
    install_requires = [
        'multiqc'
    ],
    entry_points = {
        'multiqc.modules.v1': [
            'abricate = multiqc_uphl.modules.abricate:MultiqcModule',
            'blobtools = multiqc_uphl.modules.blobtools:MultiqcModule',
            'cgpipeline = multiqc_uphl.modules.cgpipeline:MultiqcModule',
            'mash = multiqc_uphl.modules.mash:MultiqcModule',
#            'minknow = multiqc_uphl.modules.minknow:MultiqcModule',
#            'nanopolish = multiqc_uphl.modules.nanopolish:MultiqcModule',
            'roary = multiqc_uphl.modules.roary:MultiqcModule',
            'seqyclean = multiqc_uphl.modules.seqyclean:MultiqcModule',
            'seqsero = multiqc_uphl.modules.seqsero:MultiqcModule',
#            'unicycler = multiqc_uphl.modules.unicycler:MultiqcModule',
        ],
        'multiqc.hooks.v1': [
            'execution_start = multiqc_uphl.uphl_custom_code:UPHL_plugin_execution_start'
        ]
    },
)
