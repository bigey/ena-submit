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

			# Check mandatory fields
			# If any of the mandatory fields are missing, log an error and exit
			# Note: isna() checks if the value is NaN (Not a Number), which is used for missing values in pandas
			if isna(project["Project ID"]):
				log(f"Project ID is a mandatory field, line index: {index}")
				exit(1)
			if isna(project["Title"]):
				log(f"Title is a mandatory field, line index: {index}")
				exit(1)
			if isna(project["Description"]):
				log(f"Description is a mandatory field, line index: {index}")
				exit(1)

			with tag("PROJECT", alias = project["Project ID"]):
				
				with tag("TITLE"):
					text(project["Title"])
				with tag("DESCRIPTION"):
					text(project["Description"])
				
				with tag("SUBMISSION_PROJECT"):
					doc.stag("SEQUENCING_PROJECT")
	
	result = indent(doc.getvalue())
	return(result)


def _sample_xml(samples):
	doc, tag, text = Doc().tagtext()

	with tag("SAMPLE_SET"):

		for index in samples:
			sample = samples[index]

			# Check mandatory fields
			# If any of the mandatory fields are missing, log an error and exit
			# Note: isna() checks if the value is NaN (Not a Number), which is used for missing values in pandas
			if isna(sample["Sample ID"]):
				log(f"Sample ID is a mandatory field, line index: {index}")
				exit(1)
			if isna(sample["Title"]):
				log(f"Title is a mandatory field, line index: {index}")
				exit(1)
			if isna(sample["Taxon ID"]):
				log(f"Taxon ID is a mandatory field, line index: {index}")
				exit(1)
			if isna(sample["Scientific name"]):
				log(f"Scientific name is a mandatory field, line index: {index}")
				exit(1)
			if isna(sample["Sample description"]):
				log(f"Sample description is a mandatory field, line index: {index}")
				exit(1)
			if isna(sample["Collection date"]):
				log(f"Collection date is a mandatory field (YYYY-MM-DD), line index: {index}")
				exit(1)
			if isna(sample["Geographic location (country and/or sea)"]):
				log(f"Geographic location (country and/or sea) is a mandatory field, line index: {index}")
				exit(1)

			with tag("SAMPLE", alias = sample["Sample ID"]):
				
				# mandatory attribute
				with tag("TITLE"):
					text(sample["Title"])

				with tag("SAMPLE_NAME"):

					# mandatory attribute
					with tag("TAXON_ID"):
						text(sample["Taxon ID"])
					
					# mandatory attribute
					with tag("SCIENTIFIC_NAME"):
						text(sample["Scientific name"])

					# mandatory attribute					
					with tag("COMMON_NAME"):
						text(sample["Common name"])

				with tag("SAMPLE_ATTRIBUTES"):

					# madatory attribute
					with tag("SAMPLE_ATTRIBUTE"):
						with tag("TAG"):
							text("collection date")
						with tag("VALUE"):
							text(sample["Collection date"])
					
					# mandatory attribute
					with tag("SAMPLE_ATTRIBUTE"):
						with tag("TAG"):
							text("geographic location (country and/or sea)")
						with tag("VALUE"):
							text(sample["Geographic location (country and/or sea)"])

					# mandatory attribute
					with tag("SAMPLE_ATTRIBUTE"):
						with tag("TAG"):
							text("sample_description")
						with tag("VALUE"):
							text(sample["Sample description"])
					
					# optional attribute
					if not isna(sample["Culture collection"]):
						with tag("SAMPLE_ATTRIBUTE"):
							with tag("TAG"):
								text("culture_collection")
							with tag("VALUE"):
								text(sample["Culture collection"])
					
					# optional attribute
					if not isna(sample["Strain"]):
						with tag("SAMPLE_ATTRIBUTE"):
							with tag("TAG"):
								text("strain")
							with tag("VALUE"):
								text(sample["Strain"])
					
					# optional attribute
					if not isna(sample["Geographic location (region and locality)"]):
						with tag("SAMPLE_ATTRIBUTE"):
							with tag("TAG"):
								text("geographic location (region and locality)")
							with tag("VALUE"):
								text(sample["Geographic location (region and locality)"])
					
					# optional attribute
					if not isna(sample["Isolation source"]):
						with tag("SAMPLE_ATTRIBUTE"):
							with tag("TAG"):
								text("isolation_source")
							with tag("VALUE"):
								text(sample["Isolation source"])
					
					# optional attribute
					if not isna(sample["Collected by"]):
						with tag("SAMPLE_ATTRIBUTE"):
							with tag("TAG"):
								text("collected_by")
							with tag("VALUE"):
								text(sample["Collected by"])
					
	result = indent(doc.getvalue())
	return(result)


def _experiment_xml(experiments):
	doc, tag, text = Doc().tagtext()

	with tag("EXPERIMENT_SET"):

		for index in experiments:
			experiment = experiments[index]

			# Check mandatory fields
			# If any of the mandatory fields are missing, log an error and exit
			# Note: isna() checks if the value is NaN (Not a Number), which is used for missing values in pandas
			if isna(experiment["Experiment ID"]):
				log(f"Experiment ID is a mandatory field, line index: {index}")
				exit(1)
			if isna(experiment["Title"]):
				log(f"Title is a mandatory field, line index: {index}")
				exit(1)
			if isna(experiment["Project status"]):
				log(f"Project status is a mandatory field, line index: {index}")
				exit(1)
			if isna(experiment["Project reference"]):
				log(f"Project reference is a mandatory field, line index: {index}")
				exit(1)
			if isna(experiment["Sample status"]):
				log(f"Sample status is a mandatory field, line index: {index}")
				exit(1)
			if isna(experiment["Sample reference"]):
				log(f"Sample reference is a mandatory field, line index: {index}")
				exit(1)
			if isna(experiment["Library name"]):
				log(f"Library name is a mandatory field, line index: {index}")
				exit(1)
			if isna(experiment["Library strategy"]):
				log(f"Library strategy is a mandatory field, line index: {index}")
				exit(1)
			if isna(experiment["Library source"]):
				log(f"Library source is a mandatory field, line index: {index}")
				exit(1)
			if isna(experiment["Library selection"]):
				log(f"Library selection is a mandatory field, line index: {index}")
				exit(1)
			if isna(experiment["Platform"]):
				log(f"Platform is a mandatory field, line index: {index}")
				exit(1)
			if isna(experiment["Instrument model"]):
				log(f"Instrument model is a mandatory field, line index: {index}")
				exit(1)
			if isna(experiment["Paired"]):
				log(f"Paired is a mandatory field, line index: {index}")
				exit(1)
			if isna(experiment["Library construction protocol"]):
				log(f"Library construction protocol is a mandatory field, line index: {index}")
				exit(1)

			with tag("EXPERIMENT", alias = experiment["Experiment ID"]):

				with tag("TITLE"):
					text(experiment["Title"])

				if experiment["Project status"] == "internal":
					# If the project is internal, we need to use the project ID
					doc.stag("STUDY_REF", refname = experiment["Project reference"])
				elif experiment["Project status"] == "accession":
					# If the project is existing, we need to use the ENA accession number
					doc.stag("STUDY_REF", accession = experiment["Project reference"])
				else:
					# This is a fallback, but it should not happen if the spreadsheet is well-formed
					log(f"Project status should be either 'internal' or 'accession' for experiment {experiment['Experiment ID']}, line index: {index}")
					exit(1)
				
				with tag("DESIGN"):
					doc.stag("DESIGN_DESCRIPTION")

					if experiment["Sample status"] == "internal":
						# If the sample is internal, we need to use the sample ID
						doc.stag("SAMPLE_DESCRIPTOR", refname = experiment["Sample reference"])
					elif experiment["Sample status"] == "accession":
						# If the sample is existing, we need to use the ENA accession number
						doc.stag("SAMPLE_DESCRIPTOR", accession = experiment["Sample reference"])
					else:
						# This is a fallback, but it should not happen if the spreadsheet is well-formed
						log(f"Sample status should be either 'internal' or 'accession' for experiment {experiment['Experiment ID']}, line index: {index}")
						exit(1)

					with tag("LIBRARY_DESCRIPTOR"):

						with tag("LIBRARY_NAME"):
							text(experiment["Library name"])
						with tag("LIBRARY_STRATEGY"):
							text(experiment["Library strategy"])
						with tag("LIBRARY_SOURCE"):
							text(experiment["Library source"])
						with tag("LIBRARY_SELECTION"):
							text(experiment["Library selection"])
						
						with tag("LIBRARY_LAYOUT"):

							if experiment["Paired"] == "yes":
								if isna(experiment["Insert size"]) or isna(experiment["Insert size SD"]):
									# If the insert size or standard deviation is not provided, we do not include them
									doc.stag("PAIRED")
								else:
									doc.stag("PAIRED", NOMINAL_LENGTH = experiment["Insert size"], NOMINAL_SDEV = experiment["Insert size SD"])
							else:
								doc.stag("UNPAIRED")

						with tag("LIBRARY_CONSTRUCTION_PROTOCOL"):
							text(experiment["Library construction protocol"])

				with tag("PLATFORM"):
					platforms = ["ILLUMINA", "BGISEQ", "OXFORD_NANOPORE", "PACBIO_SMRT", "ION_TORRENT", "CAPILLARY", "DNBSEQ"]
					platform = experiment["Platform"].upper()
					if platform not in platforms:
						log(f"Platform should be one of {platforms} for experiment {experiment['Experiment ID']}, line index: {index}")
						exit(1)
					else:
						with tag(platform):
							with tag("INSTRUMENT_MODEL"):
								text(experiment["Instrument model"])

	result = indent(doc.getvalue())
	return(result)


def _run_xml(runs, data_dir):
	doc, tag, text = Doc().tagtext()

	with tag("RUN_SET"):

		for index in runs:
			run = runs[index]

			# Check mandatory fields
			# If any of the mandatory fields are missing, log an error and exit
			# Note: isna() checks if the value is NaN (Not a Number), which is used for missing values in pandas
			if isna(run["Run ID"]):
				log(f"Run ID is a mandatory field, line index: {index}")
				exit(1)
			if isna(run["Experiment reference"]):
				log(f"Experiment reference is a mandatory field, line index: {index}")
				exit(1)
			if isna(run["filetype"]):
				log(f"filetype is a mandatory field, line index: {index}")
				exit(1)
			if isna(run["filename_r1"]):
				log(f"filename_r1 is a mandatory field, line index: {index}")
				exit(1)
			if not os.path.exists(data_dir+"/"+run["filename_r1"]):
				log(f"File {run['filename_r1']} does not exist in the data directory ({data_dir}), line index: {index}")
				exit(1)

			with tag("RUN", alias = run["Run ID"]):

				doc.stag("EXPERIMENT_REF", refname = run["Experiment reference"])
				
				with tag("DATA_BLOCK"):
				
					with tag("FILES"):

						doc.stag("FILE", 
							filename = run["filename_r1"],
							filetype = run["filetype"],
							checksum_method = "MD5",
							checksum = md5sum(data_dir+"/"+run["filename_r1"]))

						if not isna(run["filename_r2"]):
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
			if len(projects) == 0:
				log("  No projects found in the spreadsheet. Skipping project XML generation.")
				continue
            
			with open(out_dir+"/project.xml", "w") as file:
				file.write(_project_xml(projects))

		if sheet == "sample":
			samples = to_dict(in_file, "sample")
			if len(samples) == 0:
				log("  No samples found in the spreadsheet. Skipping sample XML generation.")
				continue

			with open(out_dir+"/sample.xml", "w") as file:
				file.write(_sample_xml(samples))

		if sheet == "experiment":
			experiments = to_dict(in_file, "experiment")
			if len(experiments) == 0:
				log("  No experiments found in the spreadsheet. Skipping experiment XML generation.")
				continue
			with open(out_dir+"/experiment.xml", "w") as file:
				file.write(_experiment_xml(experiments))

		if sheet == "run":
			runs = to_dict(in_file, "run")
			if len(runs) == 0:
				log("  No runs found in the spreadsheet. Skipping run XML generation.")
				continue
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
