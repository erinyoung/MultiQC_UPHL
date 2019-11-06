#!/usr/bin/env python

""" MultiQC submodule to parse output from Roary """

import logging
import statistics
from multiqc.modules.base_module import BaseMultiqcModule
from multiqc import config
from multiqc.plots import bargraph, heatmap, linegraph

log = logging.getLogger('multiqc')

class MultiqcModule(BaseMultiqcModule):
    def __init__(self):
        super(MultiqcModule, self).__init__(name='Roary', anchor='roary',
        href="https://sanger-pathogens.github.io/Roary/",
        info="calculates the pan genome from annotated genome assemblies.")

        """ Part 1. Getting the gene summary counts """
        self.summary_data = dict()
        for myfile in self.find_log_files('roary/summary'):
            directory='_'.join(myfile['root'].split('/')[-4:-1])
            self.summary_data.update({ directory : self.parse_summary(myfile)})

        if len(self.summary_data) == 0:
            raise UserWarning
        self.summary_data = self.ignore_samples(self.summary_data)
        log.info("Found {} logs".format(len(self.summary_data)))
        self.write_data_file(self.summary_data, 'multiqc_roary_summary')

        self.add_section(
            name = 'Summary Statistics',
            anchor = 'roary-summary',
            description = 'This plot shows the number of genes that created the core genome',
            plot = self.summary_plot() )

        """ Part 2. Visualizing the kraken qc report """
        self.kraken_data = dict()
        self.kraken_keys = list()
        for myfile in self.find_log_files('roary/qc'):
            directory='_'.join(myfile['root'].split('/')[-4:-1])
            self.kraken_data.update({directory : self.parse_kraken(myfile)})

        self.kraken_data = self.ignore_samples(self.kraken_data)
        self.write_data_file(self.kraken_data, 'multiqc_roary_qc')

        self.add_section(
            name = 'QC',
            anchor = 'roary-qc',
            description = 'This plot shows the organisms identified by kraken that went into the plot',
            plot = self.kraken_plot() )


        """ Part 3. Gene presence and absence heatmap for each directory """
        self.roary_gene_data = dict()
        self.roary_gene_genes = dict()
        self.roary_gene_samples = dict()
        for myfile in self.find_log_files('roary/gene_presence'):
            directory='_'.join(myfile['root'].split('/')[-4:-1])
            self.getdata(myfile, directory)

            self.add_section(
                name = 'Gene presence heatmap for ' + directory,
                anchor = 'roary-' + directory,
                description = 'This heatmap shows the score for each sample with the genes supplied from ' + directory,
                plot = self.roary_heatmap_plot(directory) )

        """ Part 4. Number of genes and Number of genomes """
        # histogram of the number of genomes and number of genes. I don't think it's necessary at this time.

        """ Part 5. Conserved Genes """
        self.roary_gene_counts = dict()
        self.roary_gene_counts['conserved'] = dict()
        for myfile in self.find_log_files('roary/conserved_genes'):
            directory='_'.join(myfile['root'].split('/')[-4:-1])
            self.roary_gene_counts['conserved'].update({ directory : self.parse_gene_files(myfile) })

        self.add_section(
            name = 'Conserved Genes',
            anchor = 'roary-conserved',
            description = 'This plot shows the number of estimated conserved genes as the number of isolates increases',
            plot = self.roary_gene_line_graph('conserved'))

        """ Part 6. Total genes """
        self.roary_gene_counts['total'] = dict()
        for myfile in self.find_log_files('roary/total_genes'):
            directory='_'.join(myfile['root'].split('/')[-4:-1])
            self.roary_gene_counts['total'].update({ directory : self.parse_gene_files(myfile) })

        self.add_section(
            name = 'Total Genes',
            anchor = 'roary-total',
            description = 'This plot shows the number of estimated total genes as the number of isolates increases',
            plot = self.roary_gene_line_graph('total'))

        """ Part 7. Number of new genes """ # line graph dotted and solid
        self.roary_gene_counts['new'] = dict()
        for myfile in self.find_log_files('roary/new_genes'):
            directory='_'.join(myfile['root'].split('/')[-4:-1])
            self.roary_gene_counts['new'].update({ directory : self.parse_gene_files(myfile) })

        self.add_section(
            name = 'New Genes',
            anchor = 'roary-new',
            description = 'This plot shows the number of new genes as the number of isolates increases',
            plot = self.roary_gene_line_graph('new'))

        """ Part 8. Number of unique genes """
        self.roary_gene_counts['unique'] = dict()
        for myfile in self.find_log_files('roary/unique_genes'):
            directory='_'.join(myfile['root'].split('/')[-4:-1])
            self.roary_gene_counts['unique'].update({ directory : self.parse_gene_files(myfile) })

        self.add_section(
            name = 'Unique Genes',
            anchor = 'roary-unique',
            description = 'This plot shows the number of unique genes as the number of isolates increases',
            plot = self.roary_gene_line_graph('unique'))

    """ Part 1. Getting the gene summary counts """
    def parse_summary(self, myfile):
        parsed_data = dict()
        for line in myfile['f'].splitlines():
            keys = ['Core genes',
                'Soft core genes',
                'Shell genes',
                'Cloud genes',
                'Total genes']
            for key in keys:
                if key in line:
                    parsed_data[key] = line.split('\t')[-1]
        return(parsed_data)

    def summary_plot(self):
        config = {
            'id' : "roary_summary",
            'title': "Roary: Summary Statistics",
            'ylab': "Number of Genes"
        }
        keys = ['Core genes',
            'Soft core genes',
            'Shell genes',
            'Cloud genes'
            ]
        return bargraph.plot(self.summary_data, keys, config)

    """ Part 2. Visualizing the kraken qc report """
    def parse_kraken(self, myfile):
        parsed_data = dict()
        for line in myfile['f'].splitlines():
            if 'Sample,Genus,Species' not in line:
                species=line.split(",")[2]
                if species not in self.kraken_keys:
                    self.kraken_keys.append(species)
                # count each occurent of that organism for each qc result
                if species not in parsed_data:
                    parsed_data[species] = 1
                else:
                    parsed_data[species] = parsed_data[species] + 1
        return(parsed_data)

    def kraken_plot(self):
        config = {
            'id' : "roary_qc",
            'title': "Roary: QC report",
            'xlab': "Sample",
            'ylab': "Organism"
        }
        return bargraph.plot(self.kraken_data, self.kraken_keys, config)

    """ Part 3. Gene presence and absence heatmap for each directory """
    def getdata(self, myfile, directory):
        self.roary_gene_genes[directory] = []
        self.roary_gene_data[directory] = []
        for line in myfile['f'].splitlines():
            if not line.split("\t")[0] == "Gene":
                # gets the sample name
                self.roary_gene_genes[directory].append(line.split("\t")[0])
                self.roary_gene_data[directory].append(line.split("\t")[1:])
            else:
                self.roary_gene_samples[directory] = line.split("\t")[1:]

    def roary_heatmap_plot(self, directory):
        config = {
            'id' : "roary_" + directory,
            'title': "Roary: " + directory,
            'square': False,
            'colstops': [ [0, '#FFFFFF'], [1, '#000000'], ],
            'legend': False,
        }
        return heatmap.plot(self.roary_gene_data[directory], self.roary_gene_samples[directory], self.roary_gene_genes[directory], config)

    """ Part 5-8. Parsing Rtab files Conserved Genes """
    def parse_gene_files(self, myfile):
        line_averages={}
        number_of_lines = len(myfile['f'].splitlines())
        number_of_columns = len(myfile['f'].splitlines()[0].split('\t'))
        for i in range(0, number_of_columns):
            column_numbers=[]
            for j in range(0, number_of_lines):
                result = int(myfile['f'].splitlines()[j].split('\t')[i])
                column_numbers.append(result)
            average=statistics.mean(column_numbers)
            line_averages.update({ i : average })
        return(line_averages)

    def roary_gene_line_graph(self, type):
        config = {
            'id' : "roary_" + type,
            'title': "Roary: Number of " + type + " genes as isolates are included",
        }
        return linegraph.plot(self.roary_gene_counts[type], config)
