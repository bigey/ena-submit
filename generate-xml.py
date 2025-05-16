#!/usr/bin/env python3

import os, sys, argparse, hashlib
from yattag import Doc, indent
from pandas import read_excel, isna


def set_up_argparse():
	parser = argparse.ArgumentParser(
		description = """
		Generate xml files to submit to ENA submission server
		""")
	
	parser.add_argument("--data_dir", "-d", 
		dest = "data_dir", default = os.getcwd(),
		help = "directory containing the data (reads, assembly, ...). Default: current dir")

	parser.add_argument("--out_dir", "-o", 
		dest = "out_dir", default = os.getcwd(), 
		help = "output directory containing the generated xml files. Default: current dir")

	parser.add_argument("spreadsheet_file", metavar = "SPREADSHEET_FILE", 
		help = "Excel spreadsheet file (xls, xlsx, ods)")
	
	opts = parser.parse_args()
	return opts


def log(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def check_file_exists(filepath, file_description):
	"""
	A function to check if a file exists.
	It will print out an error message and exit if the file is not found
	Params
	----------
	filepath : String, the path to the file to be checked
	file_description : String, description of the file to be checked
	"""

	if not os.path.exists(filepath):
		log("The " + file_description + " (" + filepath + ") does not exist!")
		sys.exit(1)


def make_dir_if_not_exist(dir_name):
	if not os.path.exists(dir_name):
		os.makedirs(dir_name)


def _project_xml(projects):
	doc, tag, text = Doc().tagtext()

	with tag("PROJECT_SET"):

		for index in projects:

			project = projects[index]

			with tag("PROJECT", alias = project["alias"]):

				with tag("TITLE"):
					text(project["TITLE"])
				with tag("DESCRIPTION"):
					text(project["DESCRIPTION"])
				with tag("SUBMISSION_PROJECT"):
					doc.stag("SEQUENCING_PROJECT")
	
	result = indent(doc.getvalue())
	return(result)


def _sample_xml(samples):
	doc, tag, text = Doc().tagtext()

	with tag("SAMPLE_SET"):

		for index in samples:
			sample = samples[index]

			with tag("SAMPLE", alias = sample["alias"]):

				with tag("TITLE"):
					text(sample["TITLE"])

				with tag("SAMPLE_NAME"):
					with tag("TAXON_ID"):
						text(sample["TAXON_ID"])
						sample.pop("TAXON_ID")
					with tag("SCIENTIFIC_NAME"):
						text(sample["SCIENTIFIC_NAME"])
						sample.pop("SCIENTIFIC_NAME")
					
					if not isna(sample["COMMON_NAME"]):
						with tag("COMMON_NAME"):
							text(sample["COMMON_NAME"])
							sample.pop("COMMON_NAME")

				with tag("SAMPLE_ATTRIBUTES"):

					for key in sample:

						with tag("SAMPLE_ATTRIBUTE"):
							with tag("TAG"):
								text(key)
							with tag("VALUE"):
								text(sample[key])

	result = indent(doc.getvalue())
	return(result)


def _experiment_xml(experiments):
	doc, tag, text = Doc().tagtext()

	with tag("EXPERIMENT_SET"):

		for index in experiments:
			experiment = experiments[index]

			with tag("EXPERIMENT", alias = experiment["alias"]):

				with tag("TITLE"):
					text(experiment["TITLE"])
				doc.stag("STUDY_REF", refname = experiment["STUDY_REF"])
				
				with tag("DESIGN"):
					doc.stag("DESIGN_DESCRIPTION")
					doc.stag("SAMPLE_DESCRIPTOR", refname = experiment["SAMPLE_DESCRIPTOR"])

					with tag("LIBRARY_DESCRIPTOR"):

						with tag("LIBRARY_NAME"):
							text(experiment["LIBRARY_NAME"])
						with tag("LIBRARY_STRATEGY"):
							text(experiment["LIBRARY_STRATEGY"])
						with tag("LIBRARY_SOURCE"):
							text(experiment["LIBRARY_SOURCE"])
						with tag("LIBRARY_SELECTION"):
							text(experiment["LIBRARY_SELECTION"])
						
						with tag("LIBRARY_LAYOUT"):

							if experiment["PAIRED"] == "yes":
								if isna(experiment["NOMINAL_LENGTH"]) or isna(experiment["NOMINAL_SDEV"]):
									doc.stag("PAIRED")
								else:
									doc.stag("PAIRED", NOMINAL_LENGTH = experiment["NOMINAL_LENGTH"], NOMINAL_SDEV = experiment["NOMINAL_SDEV"])
							else:
								doc.stag("UNPAIRED")

						with tag("LIBRARY_CONSTRUCTION_PROTOCOL"):
							text(experiment["LIBRARY_SELECTION"])

				with tag("PLATFORM"):
					with tag("ILLUMINA"):
						with tag("INSTRUMENT_MODEL"):
							text(experiment["INSTRUMENT_MODEL"])

	result = indent(doc.getvalue())
	return(result)


def _run_xml(runs, data_dir):
	doc, tag, text = Doc().tagtext()

	with tag("RUN_SET"):

		for index in runs:
			run = runs[index]

			with tag("RUN", alias = run["alias"]):

				doc.stag("EXPERIMENT_REF", refname = run["EXPERIMENT_REF"])
				
				with tag("DATA_BLOCK"):
				
					with tag("FILES"):

						doc.stag("FILE", 
							filename = run["filename_r1"],
							filetype = run["filetype"],
							checksum_method = "MD5",
							checksum = md5sum(data_dir+"/"+run["filename_r1"]))

						if "filename_r2" in run:
							doc.stag("FILE", 
								filename = run["filename_r2"], 
								filetype = run["filetype"],
								checksum_method = "MD5",
								checksum = md5sum(data_dir+"/"+run["filename_r2"]))
	
	result = indent(doc.getvalue())
	return(result)


def to_dict(in_file, sheet):
	df = read_excel(io=in_file, sheet_name=sheet)
	return_dict = df.to_dict("index")

	return(return_dict)


def generate_xml_files(in_file, data_dir, out_dir):
	out_dir = os.path.normpath(out_dir)
	log("Generating XML files...")

	for sheet in ["project","sample","experiment","run"]:
		log("  Processing {}...".format(sheet))

		if sheet == "project":
			projects = to_dict(in_file, "project")
            
			with open(out_dir+"/project.xml", "w") as file:
				file.write(_project_xml(projects))

		if sheet == "sample":
			samples = to_dict(in_file, "sample")
			with open(out_dir+"/sample.xml", "w") as file:
				file.write(_sample_xml(samples))

		if sheet == "experiment":
			experiments = to_dict(in_file, "experiment")
			with open(out_dir+"/experiment.xml", "w") as file:
				file.write(_experiment_xml(experiments))

		if sheet == "run":
			runs = to_dict(in_file, "run")
			with open(out_dir+"/run.xml", "w") as file:
				file.write(_run_xml(runs, data_dir))


def md5sum(filename, blocksize = 65536):
	hash = hashlib.md5()
	with open(filename, "rb") as f:
		for block in iter(lambda: f.read(blocksize), b""):
			hash.update(block)

	return hash.hexdigest()


def main(opts):

	# are files exist 
	check_file_exists(opts.data_dir, "data directory")
	check_file_exists(opts.spreadsheet_file, "spreadsheet file")
	make_dir_if_not_exist(opts.out_dir)

	# process data
	generate_xml_files(opts.spreadsheet_file, opts.data_dir, opts.out_dir)


if __name__ == "__main__":
	opts = set_up_argparse()
	main(opts)
