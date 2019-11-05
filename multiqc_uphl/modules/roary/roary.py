#!/usr/bin/env python

""" MultiQC submodule to parse output from Roary """

import logging
from multiqc.modules.base_module import BaseMultiqcModule
from multiqc import config
from multiqc.plots import bargraph, linegraph, scatter

# Initialise the logger
log = logging.getLogger('multiqc')

class MultiqcModule(BaseMultiqcModule):
    def __init__(self):
        # Initialise the parent object
        super(MultiqcModule, self).__init__(name='Roary', anchor='roary',
        href="https://sanger-pathogens.github.io/Roary/",
        info="calculates the pan genome from annotated genome assemblies.")

        self.kraken_data = dict()
        self.kraken_keys = list()
        for myfile in self.find_log_files('roary/qc'):
            print(myfile['f'])
            print(myfile['s_name'])
#            self.kraken_data.update({myfile['s_name'] : self.parse_kraken(myfile)})

#        self.kraken_data = self.ignore_samples(self.kraken_data)
#        log.info("Found {} logs".format(len(self.kraken_data)))
#        self.write_data_file(self.kraken_data, 'multiqc_roary_qc')

        # Plot the data
#        self.add_section( plot = self.kraken_plot() )


#organisms=("$(cat $output_directory/*/*/*/Roary_out*/qc_report.csv | grep -v "Sample,Genus,Species" | cut -f 3 -d "," | sort | uniq | tr ' ' '_' )")

#header="tree"
#for organism in ${organisms[@]}
#do
#  header="$header,$organism"
#done
#echo "$header" > $output_directory/logs/Roary_qc_report.csv

#for summary in ${roary_summaries[@]}
#do
#  kraken_results="$summary"
#  for organism in ${organisms[@]}
#  do
#    hit=$(cat $summary | cut -f 3 -d "," | tr ' ' '_' | grep $organism | cut -f 3 -d "," | sort | uniq -c | awk '{ print $1 }' )
#    if [ -z "$hit" ] ; then hit=0 ; fi
#    kraken_results="$kraken_results,$hit"
#  done
#  echo "$kraken_results" >> $output_directory/logs/Roary_qc_report.csv
#done

#output_directory=$1
#roary_summaries=($(ls $output_directory/*/*/*/Roary_out/summary_statistics.txt ))

#echo -e "tree\tcore_genes\tsoft_core_genes\tshell_genes\tcloud_genes" > $output_directory/logs/Roary_summary_statistics.txt

#for summary in ${roary_summaries[@]}
#do
#  core_genes=$(grep "Core genes" $summary | cut -f 3 )
#  soft_core_genes=$(grep "Soft core genes" $summary | cut -f 3 )
#  shell_genes=$(grep "Shell genes" $summary | cut -f 3 )
#  cloud_genes=$(grep "Cloud genes" $summary | cut -f 3 )
#  echo -e "$summary\t$core_genes\t$soft_core_genes\t$shell_genes\t$cloud_genes" >> $output_directory/logs/Roary_summary_statistics.txt
#done

    def parse_kraken(self, myfile):
        parsed_data = dict()
        for line in myfile['f'].splitlines():
            print(line)
        return(parsed_data)
