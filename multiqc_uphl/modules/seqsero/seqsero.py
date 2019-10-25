#!/usr/bin/env python

""" MultiQC module to parse output from seqsero """

import logging
from multiqc.modules.base_module import BaseMultiqcModule
from collections import OrderedDict
from multiqc import config
from multiqc.plots import table

log = logging.getLogger('multiqc')

class MultiqcModule(BaseMultiqcModule):
    def __init__(self):

        # Initialise the parent object
        super(MultiqcModule, self).__init__(name='SeqSero', anchor='seqsero',
        href="https://github.com/denglab/SeqSero",
        info="Salmonella serotyping from genome sequencing data.")

        self.seqsero_data = dict()
        for myfile in self.find_log_files('seqsero'):
            self.get_results(myfile)

        self.seqsero_data = self.ignore_samples(self.seqsero_data)

        if len(self.seqsero_data) == 0:
            raise UserWarning

        self.add_section( plot = self.seqsero_table() )
        self.seqsero_general_stats_table()

        log.info("Found {} logs".format(len(self.seqsero_data)))

    def get_results(self, myfile):
        # Parsing the results file
        for line in myfile['f'].splitlines():
#            print(line.split(":")) # for another day
            if "Input files" in line:
                sample_name = line.split()[2]
                sample_name = sample_name.replace("_clean_PE1.fastq",'')
            elif "O antigen prediction" in line:
                O_antigen = ' '.join(line.split()[3:])
            elif "H1 antigen prediction" in line:
                H1_antigen = ' '.join(line.split()[3:])
            elif "H2 antigen prediction" in line:
                H2_antigen = ' '.join(line.split()[3:])
            elif "Predicted antigenic profile" in line:
                predicted_profile = ' '.join(line.split()[3:])
            elif "Predicted serotype" in line:
                predicted_serotype = ' '.join(line.split()[2:])
                if 'N/A' in predicted_serotype :
                    predicted_serotype = 'N/A'
            else:
                comments=line

        if "O--" not in O_antigen: # ignores non salmonella samples
            self.seqsero_data.update({
                sample_name : {
                    'O antigen' : O_antigen,
                    'H1 antigen' : H1_antigen,
                    'H2 antigen' : H2_antigen,
                    'Predicted Profile' : predicted_profile,
                    'Predicted Serotype' : predicted_serotype,
                    'Comments' : comments
                    }
                    })

    def seqsero_table(self):
        config = {
            'namespace' : 'SeqSero',
            'save_file': True
        }
        headers = OrderedDict()
        headers['Predicted Serotype'] = {
            'title': "Predicted serotype(s)",
            'description': "Predicted serotype(s)"
        }
        headers['O antigen'] = {
            'title': "O antigen prediction",
            'description': "O antigen prediction"
        }
        headers['H1 antigen'] = {
            'title': "H1 antigen prediction(fliC)",
            'description': "H1 antigen prediction(fliC)"
        }
        headers['H2 antigen'] = {
            'title': "H2 antigen prediction(fljB)",
            'description': "H2 antigen prediction(fljB)"
        }
        headers['Predicted Profile'] = {
            'title': "Predicted antigenic profile",
            'description': "Predicted antigenic profile"
        }
        headers['Comments'] = {
            'title': "Comments",
            'description': "Comments",
            'hidden': True
        }
        return table.plot(self.seqsero_data, headers, config)

    def seqsero_general_stats_table(self):
        headers = OrderedDict()
        headers['Predicted Serotype'] = {
            'title': 'Predicted Salmonella Serotype',
            }
        self.general_stats_addcols(self.seqsero_data, headers)
