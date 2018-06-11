#!/bin/bash
set -e

CREDENDIAL=.credential
FTP="ftp://webin.ebi.ac.uk/"
URL="https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/"
LIBREOFFICE_ODS="ena_submission_spreadsheet.ods"
DATA_IN_DIR="data"
XML_OUT_DIR="xml"


# Upload files to ENA (ftp)
echo
echo "Upload data to ENA FTP server..."
read user pass < $CREDENDIAL
curl --url $FTP \
	--user $user:$pass \
	-T "{$(find $DATA_IN_DIR -name '*.gz' -printf '%p,' | sed 's/,$//')}" \


# Generate XML submission files
echo
echo "Generate XML submission files..."
./generate_xml.py -d $DATA_IN_DIR -o $XML_OUT_DIR $LIBREOFFICE_ODS
submit=$XML_OUT_DIR/submission.xml
project=$XML_OUT_DIR/project.xml
sample=$XML_OUT_DIR/sample.xml
experiment=$XML_OUT_DIR/experiment.xml
run=$XML_OUT_DIR/run.xml


# ENA submit 
echo
echo "Submit XML to ENA server..."

curl -u $user:$pass \
  -F "SUBMISSION=@${submit}" \
  -F "PROJECT=@${project}" \
  -F "SAMPLE=@${sample}" \
  -F "EXPERIMENT=@${experiment}" \
  -F "RUN=@${run}" \
  ${URL} > server-receipt.xml

if grep "RECEIPT" server-receipt.xml &> /dev/null; then
  echo "Server connection was ok."
  success=$(perl -ne 'm/success="(true|false)"/ && print $1' server-receipt.xml)
  
  if [ $success = "true" ]
  then
    echo "Submission was successful."
    echo "See server receipt XML returned: server-receipt.xml."
  else
    echo "Submission was not successful!"
    echo "See server receipt XML returned: server-receipt.xml."
    echo "Check the receipt for error messages and after making corrections, "
    echo "  try the submission again."
    exit 2
  fi

else
  echo "Server connection error!"
  echo "See server receipt file: server-receipt.xml."
  exit 1
fi

# End
echo
echo "Done."
