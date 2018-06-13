#!/bin/bash
set -e 

CREDENDIAL=.credential
FTP="ftp://webin.ebi.ac.uk/"
URL="https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/"
LIBREOFFICE_ODS="new_ena_submission_spreadsheet.ods"
DATA_IN_DIR="data"
XML_OUT_DIR="xml"
ACTION="ADD"


# Upload files to ENA (ftp)
echo
echo "# Upload data to ENA FTP server..."
read user pass < $CREDENDIAL
curl --user $user:$pass \
	-T "{$(find $DATA_IN_DIR -name '*.gz' -printf '%p,' | sed 's/,$//')}" \
  --url $FTP


# Generate XML submission files
echo
echo "# Generate XML submission files..."
./generate_xml.py -d $DATA_IN_DIR -o $XML_OUT_DIR $LIBREOFFICE_ODS

project=$XML_OUT_DIR/project.xml
sample=$XML_OUT_DIR/sample.xml
experiment=$XML_OUT_DIR/experiment.xml
run=$XML_OUT_DIR/run.xml


# ENA submit 
echo
echo "# Submit XML files to ENA server..."

curl -u $user:$pass \
  -F "ACTION=${ACTION}" \
  -F "PROJECT=@${project}" \
  -F "SAMPLE=@${sample}" \
  -F "EXPERIMENT=@${experiment}" \
  -F "RUN=@${run}" \
  --url ${URL} > server-receipt.xml

echo

if grep "RECEIPT" server-receipt.xml &> /dev/null; then
  echo "Server connection was ok."
  success=$(perl -ne 'm/success="(true|false)"/ && print $1' server-receipt.xml)
  
  if [ $success = "true" ]
  then
    echo "Submission was successful."
    echo "See server receipt XML returned: server-receipt.xml."
    echo
  else
    echo "Submission was not successful!"
    echo "See server receipt XML returned: server-receipt.xml."
    echo "Check the receipt for error messages and after making corrections, "
    echo "  try the submission again."
    echo
    exit 2
  fi

else
  echo "Server connection error!"
  echo "See server receipt file: server-receipt.xml."
  echo
  exit 1
fi

# End
echo
echo "Done."
