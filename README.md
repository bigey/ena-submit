# ENA Submission Tool: Spreadsheet-Based Workflow for Genomic Data Submission

This repository provides a streamlined workflow for submitting genomic sequencing data to the European Nucleotide Archive (ENA). Rather than manually creating XML files for ENA's programmatic submission service, users can fill out a convenient spreadsheet template with their project, sample, experiment, and run metadata. The included Python script (`generate_xml.py`) automatically generates the required XML files. After submitting, the XML receipt is further parsed using `parse-receipt.py` to extract accession numbers assigned by the service.

We propose the `ena-submit.sh` script that automates the process:

1. upload run files (fastq-reads files) to the ftp server (using `curl`),
2. generate XML files (using `generate_xml.py`),
3. submit the XML files to server (using `curl`),
4. finally, parse the XML receipt (using `parse-receipt.py`)

This approach simplifies the submission process while maintaining compatibility with ENA's standards and validation requirements.

We encourage you to read the [ENA training modules](http://ena-docs.readthedocs.io/en/latest/index.html).

## Installation

### Requirements

* cURL:

install:

```sh
sudo apt-get install curl
```

* python3 modules:

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

## Collects the submission metadata

Use LibreOffice/MS-Excel to edit the submission metadata in the spreadsheet template file (`spreadsheet_template.xlsx`). 

Use one sheet for each type of metadata (Study/Project, Sample, Experiment, Run):

### Study/Project metadata

A project (also referred to as a study) is used to group other objects together, so we will look into creating a project as a first step towards to submit ENA objects.

* Project ID: this is a unique code to refer to your study - **mandatory**, *e.g.* proj_0000
* Title: a descriptive short title - **mandatory**
* Description: an abstract detailing the project - **mandatory**

### Sample metadata

Use one line per sample. ENA provides sample checklists which define all the mandatory and recommended attributes for specific types of samples. We do not define a checklist here, then the samples will be validated against the ENA default checklist [ERC000011](https://www.ebi.ac.uk/ena/data/view/ERC000011). This checklist contains many optional attributes that can help you to annotate your samples to the highest possible standard. You can find all the [checklists](http://www.ebi.ac.uk/ena/submit/checklists).

Mandatory metadata:

* Sample ID: an internal unique code - mandatory, *e.g.*: `sam_0000`
* Title: sample name *e.g.*: Saccharomyces cerevisiae S288C
* Scientific name: *e.g.*: Saccharomyces cerevisiae
* Taxon ID: obtained from [NCBI taxonomy](https://www.ncbi.nlm.nih.gov/taxonomy), *e.g.*: 4932
* Geographic location (country and/or sea): see the list of [countries](http://insdc.org/country.html). Other possible values: ["not applicable", "not collected", "not provided"]
* Collection date: format YYYY-MM-DD, YYYY-MM or YYYY. Other possible values: ["not applicable", "not collected", "not provided"]

Optional metadata:

* Common name: free text, *e.g.*: baker's yeast
* Strain: free text
* Culture collection: format `COLLECTION:ID`, *e.g.*: `CBS:512`
* Sample description: free text
* Collected by: free text
* Geographic location (region and locality): free text
* Isolation source: free text

### Experiment metadata

An experiment object represents both a library that is created from a sample and a sequencing experiment that has produced the sequencing reads. The experiment object contains details about the library protocols and sequencing experiment.

An experiment is part of a study and is associated with a sample. It is common to have multiple libraries and sequencing experiments for a single sample. Experiments point to samples to allow sharing of sample information between multiple experiments.

Mandatory metadata:

* Experiment ID: an internal unique code, *e.g.*: `exp_0000`
* Title: a short title, free text
* Project reference: the internal code of the project (*e.g.*: `proj_0000`) or the accession number of the submitted Project/Study (`PRJEBxxxxxx`)
* Project status: either "internal" (internal code of the project) or "accession" (already submitted project)
* Sample reference: the internal code of the sample (*e.g.*: `sample_0000`) or the accession number of the submited BioSample (`SAMEAxxxxxx`)
* Sample status: either "internal" (internal code of the sample) or "accession" (already submitted sample)
* Library name: an internal unique code describing the library, *e.g.*: `lib_0000`
* Library strategy: controlled value describing the sequencing strategy, see this [document](https://ena-docs.readthedocs.io/en/latest/submit/reads/webin-cli.html#permitted-values-for-library-strategy), *e.g.*: `WGS`
* Library source: controlled value describing the source material, see this [document](https://ena-docs.readthedocs.io/en/latest/submit/reads/webin-cli.html#permitted-values-for-library-source), *e.g.*: `genomic DNA`
* Library selection: controlled value describing the selection technics, see [document](https://ena-docs.readthedocs.io/en/latest/submit/reads/webin-cli.html#permitted-values-for-library-selection), *e.g.*: `RANDOM`
* Paired: is sequencing is paired ("yes") or unpaired/single ("no")
* Library construction protocol: detailed protocol, free text
* Platform: controlled value describing the sequencing platform used, see this [document](https://ena-docs.readthedocs.io/en/latest/submit/reads/webin-cli.html#permitted-values-for-platform), *e.g.*: `ILLUMINA`
* Instrument model: controlled value describing the instrument model, see this [document](https://ena-docs.readthedocs.io/en/latest/submit/reads/webin-cli.html#permitted-values-for-instrument), *e.g.*: `Illumina HiSeq 2500`

Optional metadata:

* Insert size: average insert size (bp) - optional
* Insert size SD: standard deviation of the insert size - optional

### Run metadata

The run points to an experiment using the experiment ID code (above, *e.g.*: `exp_0000`).

Mandatory metadata:

* Run ID: an internal unique code, *e.g.*: `run_0000`
* Experiment reference: the internal code of the experiment, *e.g.*: `exp_0000`
* filetype: one of fastq, bam or cram, *e.g.*: fastq
* filename_r1: path to read file 1
* filename_r2: path to read file 2 (optional if single)

## Generate XML files (command line option)

To generate the XML files from the spreadsheet metadata file use the following command:

```sh
./generate_xml.py --data_dir DATA_DIR --out_dir OUT_DIR spreadsheet_template.xlsx
```

where `DATA_DIR` is the directory containing the data (sequencing-reads) and `OUT_DIR` is the output directory containing the generated XML files.

## Upload your sequencing reads files to the ENA server (command line option)

You must upload your sequencing reads files to the ENA ftp server using your ENA credentials (login:`Webin-XXXXX`, password:`YYYYYYYY`).

Imagine you have your sequencing files present in the `DATA_DIR` directory.

* Using ftp

```sh
ftp "ftp://Webin-XXXXX:YYYYYYYY@webin.ebi.ac.uk"
mput DATA_DIR/*.fastq.gz
bye
```

* Using curl, with parallel upload (`-P 4`, 4 parallel threads)

```sh
ls DATA_DIR/*.gz | xargs -n1 -P4 -I{} curl -T "{}" ftp://webin.ebi.ac.uk --user "Webin-XXXXX:YYYYYYYY"
```

## Submit the XML files to the ENA server (command line option)

Using your ENA credentials (login:`Webin-XXXXX`, password:`YYYYYYYY`), submit your files to the server.

Two servers are available for validation and submission, respectively:

* Validation server: `https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/`
* Submission server: `https://www.ebi.ac.uk/ena/submit/drop-box/submit/`

First for testing/validation using the validation server:

```sh
curl --user "Webin-XXXXX:YYYYYYYY" \
    -F "ACTION=ADD" \
    -F "PROJECT=@data/project.xml" \
    -F "SAMPLE=@data/sample.xml" \
    -F "EXPERIMENT=@data/experiment.xml" \
    -F "RUN=@data/run.xml" \
    --url "https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/" > server-receipt.xml
```

Look at the server receipt file to check the status of the validation:

```sh
cat server-receipt.xml
```

Then if validation is successful you should observe the `success="true"` in the following line:

```xml
<RECEIPT receiptDate="2018-06-18T09:50:23.984+01:00" submissionFile="submission-XXXX_1529311823984.xml" success="true">
```

You can now submit the files to the submission server:

```sh
curl --user "Webin-XXXXX:YYYYYYYY" \
    -F "ACTION=ADD" \
    -F "PROJECT=@data/project.xml" \
    -F "SAMPLE=@data/sample.xml" \
    -F "EXPERIMENT=@data/experiment.xml" \
    -F "RUN=@data/run.xml" \
    --url "https://www.ebi.ac.uk/ena/submit/drop-box/submit/" > server-receipt.xml
```

Look at the server receipt file (`server-receipt.xml`) to check the submission status:

```sh
cat server-receipt.xml
```

If successful, this file contains the accession numbers returned from the server.

## Extract the accession numbers (command line option)

You can obtain the accession numbers in more convenient tab-separated format (TSV) as follows:

```sh
./parse-receipt.py --tsv --out acc-numbers.tsv server-receipt.xml
```

## Using the `ena-submit.sh` script (alternative, automatic)

This script automatises the following actions:

1. upload run files (reads) to the ftp server (using `curl`),
2. generate XML files (using `generate_xml.py`),
3. submit the XML files to server (using `curl`),
4. parse the XML receipt (using `parse-receipt.py`)

Please give the following information at the beginning of the script:

### Type of submission

+ `SUBMISSION="false"`, for testing. You'll use the testing server. We encourage you to first validate your data using this server,
+ `SUBMISSION="true"`, to submit your data. You'll use the submission server. This is a **real** submission!

### Select the appropriate action

+ `ACTION="ADD"` is used to submit new data,
+ `ACTION="MODIFY"` is used to update submitted data

### Create a credentials file

If you have not submitted to Webin before, please create a [submission account](https://www.ebi.ac.uk/ena/submit/sra/#home).

Create a file containing your ENA credentials. One line with your login (`Webin-XXXXX`) and password (`YYYYYY`) separated by a **blank** space.

e.g. `Webin-XXXXX<blank>YYYYYY`

Update this line accordingly in the script:

`CREDENTIAL="credential_file"`

### Give the name of the spreadsheet file

Give the name of the spreadsheet file containing your metadata:

`TEMPLATE_XLS="spreadsheet_template.xlsx"`

### Give the name of the directory containing data/sequencing reads

This directory should contain the sequencing read files. This not mandatory but we recommend to place the read files in a subdirectory.

`DATA_IN_DIR="data"`

### Give the name of the directory containing the generated XML files

Update if you want the XML files to be generated in another directory.

`XML_OUT_DIR="xml"`

### Submit your data

Use the following command to validate or submit your data:

```sh
./ena-submit.sh
```

If everything is ok, you will see the message: `Submission was successful`. Otherwise, you will see an error message: `Submission failed!`. Open the file `server-receipt.xml` to see the details and fix the errors.

The returned accession numbers are available in the file `server-receipt.txt`.

## Usage

### `generate_xml.py`

```sh
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

### `parse-receipt.py`

```sh
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

## How to report issues?

We welcome you to report any [issues](https://github.com/bigey/ena-submit/issues) in this document or script.

## Citing

If you use this document or script in your research, please cite:

BibTeX

```bibtex
@misc{bigey2026,
  author       = {Bigey, Frédéric},
  title        = {ENA Submission Tool: Spreadsheet-Based Workflow for Genomic Data Submission},
  year         = {2026},
  howpublished = {\url{https://github.com/bigey/ena-submit}},
  note         = {accessed 2026-02-11}
}
```
Biblatex

```biblatex
@software{bigey2026,
  author       = {Bigey, Frédéric},
  title        = {ENA Submission Tool: Spreadsheet-Based Workflow for Genomic Data Submission},
  year         = {2026},
  version      = {v1.0.0},
  url          = {https://github.com/bigey/ena-submit},
  note         = {accessed 2026-02-11}
}
```
