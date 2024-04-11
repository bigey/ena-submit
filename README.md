# Scripts to generate XML files and to submit them to the European Nucleotide Archive (ENA) server

Submissions to ENA can be made using programmatic submission service using `cURL`. Submissions of different types (STUDY, SAMPLE, EXPERIMENT, RUN) can be made using XML files. The script `generate_xml.py` is used to generate these files. Informations used to generate XML are extracted from a more convenient Excel spreadsheet template (`spreadsheet_template.xlsx`). The XML receipt is further parsed using `parse-receipt.py` to
extract accession numbers assigned by the service.

We encourage you to read the [ENA training modules](http://ena-docs.readthedocs.io/en/latest/index.html).

## Installation

### Requirements

* cURL:

install:

```sh
sudo apt-get install curl
```

* python3:

  * hashlib
  * yattag
  * untangle
  * pandas

install:

```sh
pip3 install -r requirements.txt
```

### Clone the project

The easiest option is to clone the repository:

```{}
git clone https://github.com/bigey/ena-submit.git
```

## Usage

### Generate XML files

```{}
generate_xml.py [-h] [--data_dir DATA_DIR] [--out_dir OUT_DIR] SPREADSHEET_FILE

Generate xml files to submit to ENA server

positional arguments:

  SPREADSHEET_FILE      Excel spreadsheet file (xls, xlsx, ods)

optional arguments:

  -h, --help            show this help message and exit

  --data_dir DATA_DIR, -d DATA_DIR
                        directory containing the data (reads)
                        Default: current dir

  --out_dir OUT_DIR, -o OUT_DIR
                        output directory containing the generated xml files
                        Default: current dir
```

### Parse the XML receipt of the server

```{}
parse-receipt.py [-h] [--tsv] [--out OUT_FILE] RECEIPT_XML

Parse the XML data received from the submission server

positional arguments:

  RECEIPT_XML           receipt xml file from ENA server

optional arguments:

  -h, --help            show this help message and exit

  --tsv, -t             output in tabular format (space separated value)

  --out OUT_FILE, -o OUT_FILE
                        optional output file
                        Default: stdout
```

## Description

Use Excel to edit the submission informations in the spreadsheet template file (`spreadsheet_template.xlsx`). Use one sheat for each type of data:

### Project

A project (also referred to as a study) is used to group other objects together, so we will look into creating a project as a first step towards to submit ENA objects.

* alias: this is a unique code to refer to your study, *eg* proj_0000
* TITLE: a descriptive short title
* DESCRIPTION: an abstract detailing the project

### Sample

Use one line per sample. ENA provides sample checklists which define all the mandatory and recommended attributes for specific types of samples. We do not define a checklist here, then the samples will be validated against the ENA default checklist [ERC000011](https://www.ebi.ac.uk/ena/data/view/ERC000011). This checklist has virtually no mandatory fields but contains many optional attributes that can help you to annotate your samples to the highest possible standard. You can find all the checklists [here](http://www.ebi.ac.uk/ena/submit/checklists).

Mandatory

* alias: a unique code, *eg*: sam_0000
* TITLE: sample name *eg*: Saccharomyces cerevisiae S288C
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
* filetype: *eg*: fastq
* filename_r1: path to read file 1
* filename_r2: path to read file 2 (optional if single)

## Using the script `ena-submit.sh`

### Utility

This script can be used to:

1. upload run files (reads) to the ftp server (using `curl`),
2. generate XML files (using `generate_xml.py`),
3. submit the XML files to server (using `curl`),
4. parse the XML receipt (using `parse-receipt.py`)

### Customization

Please give the following parameters:

#### Type of submission

Select:

* `TEST="true"` for testing. You'll use the testing server. We encourage you to first validate your data using this server,
* `TEST="false"` to submit your data. You'll use the production server. This is a **real** submission!

#### Select the appropriate action

* `ACTION="ADD"` is used to submit new data,
* `ACTION="MODIFY"` is used to update submited data

#### ENA credentials

If you have not submitted to Webin before, please register a submission account [here](https://www.ebi.ac.uk/ena/submit/sra/#home).

Create a file containing the credentials used to connect to the ENA
server: one line with `user` and `password` separated by a space character:

`user password`

Update this line accordingly:

`CREDENDIAL=".credential"`

#### LibreOffice spreadsheet

The name of the spreadsheet file containing your data. You would start using the template spreadsheet given with the project.

`LIBREOFFICE_ODS="spreadsheet_template.xlsx"`

#### Directory containing data/reads

This directory should contain the sequencing read files. Generally `*.fastq.gz` files.

`DATA_IN_DIR="data"`

#### Directory containing the generated XML files

Update if you want the XMLs to be generated in another directory.

`XML_OUT_DIR="xml"`