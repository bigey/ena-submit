#!/bin/bash
set -e

user="username"
pass="password"

FTP="ftp://webin.ebi.ac.uk/"
URL="https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/"

libreoffice_ods="ena_submission_spreadsheet.ods"
data_dir="."
xml_dir="."

# Upload files to ENA (ftp)
curl --url $FTP \
	-T "{$(find $data_dir -name '*.gz' -printf '%p,' | sed 's/,$//')}" \
	--user $user:$pass

# Generate XML submission files
./generate_xml.py -d $data_dir -o $xml_dir $libreoffice_ods

# ENA submit 
submit=submission.xml
project=project.xml
sample=sample.xml
experiment=experiment.xml
run=run.xml

curl -u $user:$pass \
  -F "SUBMISSION=@${submit}" \
  -F "PROJECT=@${project}" \
  -F "SAMPLE=@${sample}" \
  -F "EXPERIMENT=@${experiment}" \
  -F "RUN=@${run}" \
  ${URL}
