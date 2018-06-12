# Prepare XML submission data to the European Nucleotide Archive (ENA) server

Project presentation.

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

* a spreasheet document to stored submission informations. One sheat for each type of data:
    * PROJECT
    * SAMPLE
    * EXPERIMENT
    * RUN
* a python script `generate_xml.py` to generate the corresponding XML files
* a shell (`bash`) script is used to:
    * upload the run (reads) files to the ftp server
    * generate XML file (using `generate_xml.py`)
    * submit the XML files to ENA submission server
