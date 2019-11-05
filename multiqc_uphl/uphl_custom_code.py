#!/usr/bin/env python
""" MultiQC example plugin functions
We can add any custom Python functions here and call them
using the setuptools plugin hooks.
"""

from __future__ import print_function
from pkg_resources import get_distribution
import logging

from multiqc.utils import report, util_functions, config

# Initialise the main MultiQC logger
log = logging.getLogger('multiqc')

# Save this plugin's version number (defined in setup.py) to the MultiQC config
config.multiqc_uphl_version = get_distribution("multiqc_uphl").version

# Add default config options for the things that are used in MultiQC_NGI
#def multiqc_uphl_execution_start():
def UPHL_plugin_execution_start():
    """ Code to execute after the config files and
    command line flags have been parsedself.
    This setuptools hook is the earliest that will be able
    to use custom command line flags.
    """

    # Halt execution if we've disabled the plugin
    if config.kwargs.get('disable_plugin', True):
        return None

    log.info("Running MultiQC UPHL Plugin v{}".format(config.multiqc_uphl_version))

    # Add to the main MultiQC config object.
    # User config files have already been loaded at this point
    #   so we check whether the value is already set. This is to avoid
    #   clobbering values that have been customised by users.

    # Add to the search patterns used by modules
#    if 'my_example/key_value_pairs' not in config.sp:
#        config.update_dict( config.sp, { 'my_example/key_value_pairs': { 'fn': 'my_plugin_output.tsv' } } )
#    if 'my_example/plot_data' not in config.sp:
#        config.update_dict( config.sp, { 'my_example/plot_data': { 'fn': 'my_plugin_plotdata.tsv' } } )
    if 'mash' not in config.sp:
        config.update_dict( config.sp, { 'mash': {'fn' : '*_mashdist.txt' }})
    if 'abricate' not in config.sp:
        config.update_dict( config.sp, { 'abricate': { 'fn' : '*abricate_summary.txt' }})
    if 'seqyclean' not in config.sp:
        config.update_dict( config.sp, { 'seqyclean': { 'fn' : '*SummaryStatistics.tsv' }})
    if 'cgpipeline' not in config.sp:
        config.update_dict( config.sp, { 'cgpipeline': { 'fn' : '*cgpipeline.txt' }})
    if 'blobtools/json' not in config.sp:
        config.update_dict( config.sp, { 'blobtools/json': { 'fn' : '*.blobDB.json' }})
    if 'blobtools/stats' not in config.sp:
        config.update_dict( config.sp, { 'blobtools/stats': { 'fn' : '*.blobplot.stats.txt' }})
    if 'blobtools/table' not in config.sp:
        config.update_dict( config.sp, { 'blobtools/table': { 'fn' : '*.blobDB.table.txt' }})
    if 'seqsero' not in config.sp:
        config.update_dict( config.sp, { 'seqsero': { 'fn' : 'Seqsero_result.txt' }})
    if 'roary/qc' not in config.sp:
        config.update_dict( config.sp, { 'roary/qc': { 'fn' : 'qc_report.csv' }})
    if 'roary/summary' not in config.sp:
        config.update_dict( config.sp, { 'roary/summary': { 'fn' : 'summary_statistics.txt' }})

    # Some additional filename cleaning
    config.fn_clean_exts.extend([
        '_SummaryStatistics',
        '.abricate_summary',
        '_mashdist',
        'cgpipeline',
        '.blobplot.stats',
        '.blobDB',
        '_clean_PE1.fastq',
#        '.my_tool_extension',
#        '.removeMetoo'
    ])

#    # Ignore some files generated by the custom pipeline
#    config.fn_ignore_paths.extend([
#        '*/my_awesome_pipeline/fake_news/*',
#        '*/my_awesome_pipeline/red_herrings/*',
#        '*/my_awesome_pipeline/noisy_data/*',
#        '*/my_awesome_pipeline/rubbish/*'
#    ])
