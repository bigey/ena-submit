# A python script to generate XML files used to submit data to the European Nucleotide Archive (ENA) server

Submissions to ENA can be made using programmatic submission service using `cURL`. Submissions of different types (STUDY, SAMPLE, EXPERIMENT, RUN) can be made using XML files. The script `generate_xml.py` is used to generate these files.

Informations used to generate XML are extracted from a more convenient LibreOffice spreadsheet (ODS) template (`ena_submission_spreadsheet.ods`).

## Install

### Requirements

* `cURL`

~~~sh
sudo apt-get install curl
~~~

* python3
  * hashlib
  * yattag
  * pyexcel_ods

~~~sh
pip3 install -r requirements.txt
~~~

### Installation

The easiest option is to clone the repository:

~~~sh
git clone https://github.com/bigey/ena-submit.git
~~~

## Usage

~~~
generate_xml.py [-h] [--data_dir DATA_DIR] [--out_dir OUT_DIR] SPREADSHEET_FILE

This tool will generate xml files to submit to ENA repository

positional arguments:

  SPREADSHEET_FILE      spreadsheet file in libreoffice calc format (ods)

optional arguments:

  -h, --help            show this help message and exit

  --data_dir DATA_DIR, -d DATA_DIR
                        directory containing the data (reads)

                        Default: current dir

  --out_dir OUT_DIR, -o OUT_DIR
                        output directory containing the generated xml files

                        Default: current dir
~~~

## Description

Use LibreOffice/OpenOffice to edit the submission informations in the spreadsheet template file. Use one sheat for each type of data:

### Project

A project (also referred to as a study) is used to group other objects together, so we will look into creating a project as a first step towards to submit ENA objects.

* alias: this is a unique code to refer to your study, *eg* proj_0000
* TITLE: a descriptive short title
* DESCRIPTION: an abstract detailing the project

### Sample

Use one line per sample. ENA provides sample checklists which define all the mandatory and recommended attributes for specific types of samples. We do not define a checklist then the samples will be validated against the ENA default checklist [ERC000011](https://www.ebi.ac.uk/ena/data/view/ERC000011). This checklist has virtually no mandatory fields but contains many optional attributes that can help you to annotate your samples to the highest possible standard. You can find all the sample checklists [here](http://www.ebi.ac.uk/ena/submit/checklists).

Mandatory

* alias: a unique code, *eg*: S288C_bis
* TITLE: sample name *eg*: S288C
* TAXON_ID: *eg*: 4932
* SCIENTIFIC_NAME: *eg*: Saccharomyces cerevisiae
* COMMON_NAME: *eg*: baker's yeast (optional)

Optional

* strain
* sample_description
* collected_by
* geographic location (country and/or sea)
* geographic location (region and locality)
* isolation_source

### Experiment

An experiment object represents the library that is created from a sample and used in a sequencing experiment. The experiment object contains details about the sequencing platform and library protocols.
An experiment is part of a study and is assocated with a sample. It is common to have multiple libraries and sequencing experiments for a single sample. Experiments point to samples to allow sharing of sample information between multiple experiments.

* alias: a unique code, *eg*: exp_0000
* TITLE: a short title
* STUDY_REF: code of the project, *eg*: proj_0000
* SAMPLE_DESCRIPTOR: code of the sample, *eg*: sample_0000
* LIBRARY_NAME: a unique code, *eg*: lib_0000
* LIBRARY_STRATEGY: controlled value fields
* LIBRARY_SOURCE: controlled value fields
* LIBRARY_SELECTION: controlled value fields
* PAIRED: yes|no
* NOMINAL_LENGTH: average insert size
* NOMINAL_SDEV: standard deviation of insert size (optional)
* LIBRARY_CONSTRUCTION_PROTOCOL: detailed protocol
* INSTRUMENT_MODEL: *eg*: Illumina HiSeq 2000

### Run

The run points to the experiment using the experiment’s alias.

* alias: a unique code, *eg*: run_0000
* EXPERIMENT_REF: code of the experiment, *eg*: exp_0000
* filetype: fastq
* filename_r1
* filename_r2

## TODO

Adapt the shell script `ena-submit.sh` to:

* upload the run (reads) files to the ftp server
* generate XML file (using `generate_xml.py`)
* submit the XML files to ENA submission server
