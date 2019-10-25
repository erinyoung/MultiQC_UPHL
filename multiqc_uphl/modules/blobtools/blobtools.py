#!/usr/bin/env python

""" MultiQC submodule to parse output from Samtools stats """

import logging
from multiqc.modules.base_module import BaseMultiqcModule
import json

from multiqc import config
from multiqc.plots import bargraph

# Initialise the logger
log = logging.getLogger('multiqc')

class MultiqcModule(BaseMultiqcModule):

    def __init__(self):
        # Initialise the parent object
        super(MultiqcModule, self).__init__(name='BlobTools', anchor='blobtools',
        href="https://blobtools.readme.io/docs",
        info="is a modular command-line solution for visualisation, quality control and taxonomic partitioning of genome datasets")

        # Find and load any Mash reports
        self.blobtools_data = dict()
        for myfile in self.find_log_files('blobtools/json'):
#            print(myfile['s_name'])
            contents_of_file = json.loads(myfile['f'])
            # print(contents_of_file.keys()) # getting all of the keys
            # dict_keys(['title', 'assembly_f', 'lineages', 'order_of_blobs', 'dict_of_blobs', 'length', 'seqs', 'n_count', 'nodesDB_f', 'covLibs', 'hitLibs', 'taxrules', 'version', 'min_score', 'min_diff', 'tax_collision_random'])
            # print(contents_of_file['title']) # title of file
            # print(contents_of_file['assembly_f']) # title of contigs file for reference
            # print(contents_of_file['lineages'].keys()) # taxids
#            for key in contents_of_file['lineages'].keys():
                #print(key['species'])
#                print(contents_of_file['lineages'][key])
#                print(key + " : " + contents_of_file['lineages'][key]['species']) # taxid : species
            # print(contents_of_file['order_of_blobs'].keys()) # an ordered dictionary of blobs from largest to smallest contigs
            # print(contents_of_file['dict_of_blobs'].keys()) - probably for making the blob plots
#            print(contents_of_file['dict_of_blobs']['contig00001'].keys())
#            print(contents_of_file['dict_of_blobs']['contig00001']['hits'])
#            for key in contents_of_file['dict_of_blobs']['contig00001'].keys():
#                print(contents_of_file['dict_of_blobs']['contig00001'][key])
#            print(contents_of_file['dict_of_blobs']['contig00001']['taxonomy']['bestsum']['species']['tax']) # the species information
            # print(contents_of_file['length']) # total length of contigs
            # print(contents_of_file['seqs']) # number of contigs?
            # print(contents_of_file['n_count']) # no idea
            # print(contents_of_file['nodesDB_f']) # None
            # print(contents_of_file['covLibs']) #!!! has reads_total and reads_mapped
            # print(contents_of_file['hitLibs'])
            # print(contents_of_file['taxrules']) # no idea
            # print(contents_of_file['version']) # version
            # print(contents_of_file['min_score']) # no idea
            # print(contents_of_file['min_diff']) # 0.0
            # print(contents_of_file['tax_collision_random']) # False

            self.blobtools_data.update({ myfile['s_name'] : {
                'total': contents_of_file['covLibs']['bam0']['reads_total'],
                'mapped': contents_of_file['covLibs']['bam0']['reads_mapped'],
                'unmapped': contents_of_file['covLibs']['bam0']['reads_total'] - contents_of_file['covLibs']['bam0']['reads_mapped']
                }
                })
        self.write_data_file(self.blobtools_data, 'blobtools_mapping')

        if len(self.blobtools_data) == 0:
            raise UserWarning
        self.blobtools_data = self.ignore_samples(self.blobtools_data)
        log.info("Found {} logs".format(len(self.blobtools_data)))

        self.blobtools_species_data=dict()
        self.blobtools_species_keys=list()
        for myfile in self.find_log_files('blobtools/stats'):
            self.blobtools_species_data[myfile['s_name']]=dict()
            for line in myfile['f'].splitlines():
                if not line.startswith("#") and not line.startswith("all"):
                    self.blobtools_species_data[myfile['s_name']].update({ line.split('\t')[0]: line.split('\t')[11].replace(',','') })
                    if line.split('\t')[0] not in self.blobtools_species_keys:
                        self.blobtools_species_keys.append(line.split('\t')[0])
        self.write_data_file(self.blobtools_species_data, 'blobtools_species')
        self.blobtools_species_data = self.ignore_samples(self.blobtools_species_data)

        self.add_section(
            name = 'Mapping',
            anchor = 'blobtool-mapping',
            description = 'This plot shows the number of reads that map back to the reference',
            plot = self.blobtools_mapping())

        self.add_section(
            name = 'Species',
            anchor = 'blobtool-species',
            description = 'This plot shows the species that were identified in the reads',
            plot = self.blobtools_species())

    def blobtools_mapping(self):
        config = {
            'id': 'blobtools-1',
            'title': 'Blobtools: Read Coverage Mapping',
            'ylab': 'Number of Reads'
            }
        keys =['mapped', 'unmapped',]
        return bargraph.plot(self.blobtools_data, keys, config)

    def blobtools_species(self):
        config = {
            'id': 'blobtools-2',
            'title': 'Blobtools: Species Identification',
            'ylab': 'Number of Reads'
            }
        return bargraph.plot(self.blobtools_species_data, self.blobtools_species_keys, config)
