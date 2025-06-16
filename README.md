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

* Project ID: this is a unique code to refer to your study - mandatory, *e.g.* proj_0000 - mandatory
* Title: a descriptive short title - mandatory
* Description: an abstract detailing the project - mandatory

### Sample

Use one line per sample. ENA provides sample checklists which define all the mandatory and recommended attributes for specific types of samples. We do not define a checklist here, then the samples will be validated against the ENA default checklist [ERC000011](https://www.ebi.ac.uk/ena/data/view/ERC000011). This checklist has virtually no mandatory fields but contains many optional attributes that can help you to annotate your samples to the highest possible standard. You can find all the [checklists](http://www.ebi.ac.uk/ena/submit/checklists).

Mandatory:

* Sample ID: a unique code - mandatory, *e.g.*: sam_0000
* Title: sample name *e.g.*: Saccharomyces cerevisiae S288C
* Taxon ID: *e.g.*: 4932
* Scientific name: *e.g.*: Saccharomyces cerevisiae
* Geographic location (country and/or sea): see the list of [countries](http://insdc.org/country.html). Other possible values: ["not applicable", "not collected", "not provided"]
* Collection date: format YYYY-MM-DD, YYYY-MM or YYYY

Optional:

* Common name: free text, *e.g.*: baker's yeast
* Strain: free text
* Culture collection: format COLLECTION:ID, *e.g.*: CBS:512
* Sample description: free text
* Collected by: free text
* Geographic location (region and locality): free text
* Isolation source: free text

### Experiment

An experiment object represents the library that is created from a sample and used in a sequencing experiment. The experiment object contains details about the sequencing platform and library protocols.
An experiment is part of a study and is assocated with a sample. It is common to have multiple libraries and sequencing experiments for a single sample. Experiments point to samples to allow sharing of sample information between multiple experiments.

Mandatory:

* Experiment ID: a unique code, *e.g.*: exp_0000
* Title: a short title, free text
* Project reference: the internal code of the project (*e.g.*: proj_0000) or the accession number of the submitted Project/Study (PRJxxxxxxx)
* Project status: either "internal" (internal code of the project) or "accession" (already submitted project)
* Sample reference: the internal code of the sample (*e.g.*: sample_0000) or the accession number of the submited BioSample (SAMEAxxxxxxx)
* Sample status: either "internal" (internal code of the sample) or "accession" (already submitted sample)
* Library name: a unique code describing the library, *e.g.*: lib_0000
* Library strategy: controlled value describing the sequencing strategy, see this [document](https://ena-docs.readthedocs.io/en/latest/submit/reads/webin-cli.html#permitted-values-for-library-strategy)
* Library source: controlled value describing the source material, see this [document](https://ena-docs.readthedocs.io/en/latest/submit/reads/webin-cli.html#permitted-values-for-library-source)
* Library selection: controlled value describing the selection technics, see [document](https://ena-docs.readthedocs.io/en/latest/submit/reads/webin-cli.html#permitted-values-for-library-selection)
* Paired: is sequencing is paired ("yes") or unpaired/single ("no")
* Library construction protocol: detailed protocol, free text
* Platform: controlled value describing the sequencing platform used, see this [document](https://ena-docs.readthedocs.io/en/latest/submit/reads/webin-cli.html#permitted-values-for-platform)
* Instrument model: controlled value describing the instrument mode, see this [document](https://ena-docs.readthedocs.io/en/latest/submit/reads/webin-cli.html#permitted-values-for-instrument)

Optional:

* Insert size: average insert size (bp) - optional
* Insert size SD: standard deviation of the insert size - optional

### Run

The run points to an experiment using the experiment ID code.

Mandatory:

* Run ID: internal unique code, *e.g.*: run_0000
* Experiment reference: the internal code of the experiment, *e.g.*: exp_0000
* filetype: *e.g.*: fastq
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

If you have not submitted to Webin before, please register a [submission account](https://www.ebi.ac.uk/ena/submit/sra/#home).

Create a file containing the credentials used to connect to the ENA
server: one line with `user` and `password` separated by a space character:

`user password`

Update this line accordingly:

`CREDENDIAL=".credential"`

#### XLS spreadsheet

The name of the spreadsheet file containing your data. You would start using the template spreadsheet given with the project.

`TEMPLATE_XLS="spreadsheet_template.xlsx"`

#### Directory containing data/reads

This directory should contain the sequencing read files. Generally `*.fastq.gz` files.

`DATA_IN_DIR="data"`

#### Directory containing the generated XML files

Update if you want the XMLs to be generated in another directory.

`XML_OUT_DIR="xml"`
