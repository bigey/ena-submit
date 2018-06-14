#!/usr/bin/env python3

import sys
import argparse
import untangle


def set_up_argparse():
	parser = argparse.ArgumentParser(
		description = """
		Parse the XML data received from the submission server
		""")
	
	parser.add_argument("--tsv", "-t", 
		dest = "is_tabular", action='store_true', 
		help = "output in tabular format (space separated value)")

	parser.add_argument("--out", "-o", 
		dest = "out_file", default = sys.stdout,
		help = "optional output file. Default: stdout")

	parser.add_argument("xml_file", metavar = "RECEIPT_XML", 
		help = "receipt xml file from ENA server")
	
	opts = parser.parse_args()
	return opts


def extract(element, store = { "SUBMISSION": [], "PROJECT": [], "SAMPLE": [], 
    "EXPERIMENT": [], "RUN": [], }):

    for child in element.children:
        
        if child._name in ["SUBMIT", "EXPERIMENT", "RUN"]:
            store[child._name].append([child["alias"], child["accession"]])
        
        if child._name in ["PROJECT", "SAMPLE"]:
            store[child._name].append([child["alias"], child["accession"], child.EXT_ID["accession"]])

    return store


def output(data_dict, tabular = True, fh = sys.stdout):
	if tabular == True:
		for key, arrays in data_dict.items():
			for array in arrays:
				string = key + " " + " ".join( array )
				print(string, file = fh)
	else:
		print(data_dict, file = fh)


def main(opts):
	try:
		xml = untangle.parse(opts.xml_file)
		receipt = xml.RECEIPT
	except:
	    print("Probably not a valid XML file!", file = sys.stderr)
	    sys.exit(1)

	if receipt["success"] == "false":
	    print("Submission failed!", file = sys.stderr)
	    sys.exit(1)
		
	# extract receipt data from xml
	data = extract(receipt)

	# output formated data
	if opts.out_file == sys.stdout:
		output(data, tabular = opts.is_tabular)
	else:
		with open(opts.out_file, "a") as fh:
			output(data, tabular = opts.is_tabular, fh = fh)


if __name__ == "__main__":
	opts = set_up_argparse()
	main(opts)
