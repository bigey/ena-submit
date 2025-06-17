#!/bin/bash
set -e

#------------------------------------------------------------------------------#
#                     Thank you to adapt information below                     #
#------------------------------------------------------------------------------#

# TEST/SUBMIT YOUR DATA
# One of the following:
# "true": submit to testing server, 
# "false": real data submission
TEST="false"

# EXPECTED ACTION
# One of the following actions:
# "ADD": submit new data,
# "MODIFY": submit updates data
ACTION="ADD"

# CREDENTIAL FILE
# File containing the credentials. 
# One line containing: 
# username password
CREDENDIAL=.credential

# SPREADSHEET FILE
# Name of the spreadsheet file containing your data.
# Start using the giving template
TEMPLATE_XLS="spreadsheet_template.xlsx"

# DIRECTORY CONTAINING THE DATA READS
# The name of the directory where sequencing reads are stored
# Generally fastq.gz files
DATA_IN_DIR="data"

# DIRECTORY CONTAINING THE GENERATED XLM FILES
# This directrory will be used to store the xml files produced 
XML_OUT_DIR="xml"


#------------------------------------------------------------------------------#
#                You should not have to modify the code below                  #
#------------------------------------------------------------------------------#

# ENA SERVERS
FTP="ftp://webin.ebi.ac.uk/"
URL_TEST="https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/"
URL_PROD="https://www.ebi.ac.uk/ena/submit/drop-box/submit/"

echo

# SELECT SERVER
if [ $TEST = "false" ]
then
  URL=$URL_PROD
  echo "This is a real submission..."
else
  URL=$URL_TEST
  echo "This a test submission..."
fi

# IMPORT CREDENTIALS
read user pass < $CREDENDIAL


# UPLOAD FILES TO ENA (FTP)
echo
echo "# Upload data to ENA FTP server..."
echo
# curl --user $user:$pass --upload-file "{$(find $DATA_IN_DIR -name '*.gz' -printf '%p,' | sed 's/,$//')}" --url $FTP

# GENERATE XML FILES
echo
echo "# Generate XML submission files..."
echo
./generate-xml.py -d $DATA_IN_DIR -o $XML_OUT_DIR $TEMPLATE_XLS
echo

project=$XML_OUT_DIR/project.xml
sample=$XML_OUT_DIR/sample.xml
experiment=$XML_OUT_DIR/experiment.xml
run=$XML_OUT_DIR/run.xml
files=""

# CHECK IF XML FILES WERE GENERATED
if [ -f $project ]; then
  echo "Project XML file: $project generated successfully."
  files="$file -F PROJECT=@${project} "
fi
if [ -f $sample ]; then
  echo "Sample XML file: $sample generated successfully."
  files="$files -F SAMPLE=@${sample} "
fi
if [ -f $experiment ]; then
  echo "Experiment XML file: $experiment generated successfully."
  files="$files -F EXPERIMENT=@${experiment} "
fi
if [ -f $run ]; then
  echo "Run XML file: $run generated successfully."
  files="$files -F RUN=@${run} "
else
  echo "Run XML file: $run not found. Skipping run submission."
fi

# ENA SUBMISSION 
echo
echo "# Submit XML files to ENA server..."
echo
curl -u $user:$pass -F "ACTION=${ACTION}" ${files} --url ${URL} > server-receipt.xml
echo

if grep "RECEIPT" server-receipt.xml &> /dev/null; then
  echo "Server connection was ok."
  success=$(perl -ne 'm/success="(true|false)"/ && print $1' server-receipt.xml)
  
  if [ $success = "true" ]
  then
    echo "Submission was successful."

    # PARSE RECEIPT XML RESPONSE
    ./parse-receipt.py -t -o server-receipt.txt server-receipt.xml

    echo "See the server receipts returned: "
    echo "   - server-receipt.xml (original receipt)"
    echo "   - server-receipt.txt (tabular format)" 

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

# END
echo
echo "Done."
