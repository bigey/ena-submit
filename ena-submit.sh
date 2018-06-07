#!/bin/bash
set -e

CREDENDIAL=.credential
FTP="ftp://webin.ebi.ac.uk/"
URL="https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/"
libreoffice_ods="ena_submission_spreadsheet.ods"
data_dir="data"
xml_dir="xml"


# Upload files to ENA (ftp)
read user pass < $CREDENDIAL
echo $user $pass

curl --url $FTP \
	--user $user:$pass \
	-T "{$(find $data_dir -name '*.gz' -printf '%p,' | sed 's/,$//')}" \


# Generate XML submission files
./generate_xml.py -d $data_dir -o $xml_dir $libreoffice_ods


# ENA submit 
submit=$xml_dir/submission.xml
project=$xml_dir/project.xml
sample=$xml_dir/sample.xml
experiment=$xml_dir/experiment.xml
run=$xml_dir/run.xml

curl -u $user:$pass \
  -F "SUBMISSION=@${submit}" \
  -F "PROJECT=@${project}" \
  -F "SAMPLE=@${sample}" \
  -F "EXPERIMENT=@${experiment}" \
  -F "RUN=@${run}" \
  ${URL}
