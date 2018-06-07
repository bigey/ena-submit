#!/bin/bash
set -e

user=username
pass=password

URL="https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/"

submit=submission.xml
project=project.xml
sample=sample.xml
experiment=experiment.xml
run=run.xml

# submit all
curl -u $user:$pass \
  -F "SUBMISSION=@${submit}" \
  -F "PROJECT=@${project}" \
  -F "SAMPLE=@${sample}" \
  -F "EXPERIMENT=@${experiment}" \
  -F "RUN=@${run}" \
  ${URL}
