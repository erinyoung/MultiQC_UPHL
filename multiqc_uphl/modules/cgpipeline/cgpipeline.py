#!/usr/bin/env python

""" MultiQC submodule to parse output from Samtools stats """

import logging
from multiqc.modules.base_module import BaseMultiqcModule
from collections import OrderedDict
from multiqc import config
from multiqc.plots import table

# Initialise the logger
log = logging.getLogger('multiqc')

class MultiqcModule(BaseMultiqcModule):

    def __init__(self):
        # Initialise the parent object
        super(MultiqcModule, self).__init__(name='CG Pipeline',
        anchor='cgpipeline',
        href="https://github.com/lskatz/CG-Pipeline",
        info=": Genome assembly/prediction/annotation pipeline for the Linux command line")

        # Find and load any Mash reports
        self.cgpipeline_data = dict()
        for myfile in self.find_log_files('cgpipeline'):
            rows = myfile['f'].splitlines()
            headers = rows[0].split("\t")
            cols = rows[1].split("\t")

            self.cgpipeline_data[myfile['s_name']] = dict()
            for header, cols in zip(headers, cols):
                self.cgpipeline_data[myfile['s_name']].update({ header : cols })

        self.cgpipeline_data = self.ignore_samples(self.cgpipeline_data)
        if len(self.cgpipeline_data) == 0:
            raise UserWarning
        log.info("Found {} logs".format(len(self.cgpipeline_data)))

        self.add_section( plot = self.cgpipeline_table() )
        self.cgpipeline_general_stats_table()

    def cgpipeline_table(self):
        config = {
            'namespace' : 'cg-pipeline',
            'save_file': True
        }
        headers = OrderedDict()
        headers['File'] = {
            'title': "File",
            'description': "File name",
            'hidden': True
        }
        headers['avgReadLength'] = {
            'title': "Average Read Length",
            'min': 70,
            'scale': 'Spectral'
        }
        headers['totalBases'] = {
            'title': "Total Bases",
            'min': 0,
            'scale': 'Greens'
        }
        headers['minReadLength'] = {
            'title': "Minimum Read Length",
            'hidden': True
        }
        headers['maxReadLength'] = {
            'title': "Maximum Read Length",
            'hidden': True
        }
        headers['avgQuality'] ={
            'title': "Average Read Quality",
            'min': 20,
            'max': 40,
            'scale': 'Blues'
        }
        headers['numReads'] = {
            'title': "Number of Reads",
            'min': 0,
            'scale': 'Purples'
        }
        headers['PE?'] = {
            'title': "PE",
            'hidden': True
        }
        headers['coverage'] = {
            'title': "Coverage",
            'min': 20,
            'max': 100,
            'scale': 'GnBu'
        }
        headers['readScore'] = {
            'title': "Read Score",
            'hidden': True
        }
        headers['medianFragmentLength'] = {
            'title': "Median Fragment Length",
            'hidden': True
        }
        return table.plot(self.cgpipeline_data, headers, config)

    def cgpipeline_general_stats_table(self):
        headers = OrderedDict()
        headers['coverage'] = {
            'title': 'Coverage',
            'scale': 'YlGn',
            }
        self.general_stats_addcols(self.cgpipeline_data, headers)
