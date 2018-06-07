#!/usr/bin/env python3

import argparse
from yattag import Doc, indent
from pyexcel_ods import get_data


def set_up_argparse():
	parser = argparse.ArgumentParser(description="""
	This tool will generate xml files to submit to ENA repository
	""")
	
	# parser.add_argument()
	
	opts = parser.parse_args()
	
	return opts


def _project(projects):
	doc, tag, text = Doc().tagtext()

	with tag("PROJECT_SET"):

		for a_project in projects:

			project = projects[a_project]

			with tag("PROJECT", alias = a_project):

				with tag("TITLE"):
					text(project["TITLE"])
				with tag("DESCRIPTION"):
					text(project["DESCRIPTION"])
				with tag("SUBMISSION_PROJECT"):
					doc.stag("SEQUENCING_PROJECT")
	
	result = indent(doc.getvalue())
	return(result)


def _sample(samples):
	doc, tag, text = Doc().tagtext()

	with tag("SAMPLE_SET"):

		for sample_alias in samples:
			sample = samples[sample_alias]

			with tag("SAMPLE", alias = sample_alias):

				with tag("TITLE"):
					text(sample["TITLE"])

				with tag("SAMPLE_NAME"):
					with tag("TAXON_ID"):
						text(sample["TAXON_ID"])
					with tag("SCIENTIFIC_NAME"):
						text(sample["SCIENTIFIC_NAME"])
					with tag("COMMON_NAME"):
						text(sample["COMMON_NAME"])

				with tag("SAMPLE_ATTRIBUTES"):

					with tag("SAMPLE_ATTRIBUTE"):
						with tag("TAG"):
							text("strain")
						with tag("VALUE"):
							text(sample["strain"])

					with tag("SAMPLE_ATTRIBUTE"):
						with tag("TAG"):
							text("sample_description")
						with tag("VALUE"):
							text(sample["sample_description"])

					with tag("SAMPLE_ATTRIBUTE"):
						with tag("TAG"):
							text("collected_by")
						with tag("VALUE"):
							text(sample["collected_by"])

					with tag("SAMPLE_ATTRIBUTE"):
						with tag("TAG"):
							text("country")
						with tag("VALUE"):
							text(sample["country"])

					with tag("SAMPLE_ATTRIBUTE"):
						with tag("TAG"):
							text("isolation_source")
						with tag("VALUE"):
							text(sample["isolation_source"])

	result = indent(doc.getvalue())
	return(result)


def _experiment(experiments):
	doc, tag, text = Doc().tagtext()

	with tag("EXPERIMENT_SET"):

		for exp_alias in experiments:
			experiment = experiments[exp_alias]

			with tag("EXPERIMENT", alias = exp_alias):

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
								doc.stag("PAIRED", NOMINAL_LENGTH = experiment["NOMINAL_LENGTH"], NOMINAL_SDEV   = experiment["NOMINAL_SDEV"])
							else:
								doc.stag("UNPAIRED")

						with tag("LIBRARY_CONSTRUCTION_PROTOCOL"):
							text(experiment["LIBRARY_SELECTION"])

				with tag("PLATFORM"):
					with tag("ILLUMINA"):
						with tag("INSTRUMENT_MODEL"):
							text(experiment["INSTRUMENT_MODEL"])

				# with tag("EXPERIMENT_ATTRIBUTES"):
				# 	with tag("EXPERIMENT_ATTRIBUTE"):
				# 		with tag("TAG"):
				# 			text("library_preparation_date")
				# 		with tag("VALUE"):
				# 			text(experiment["library_preparation_date"])

	result = indent(doc.getvalue())
	return(result)


def _run(runs):
	doc, tag, text = Doc().tagtext()

	with tag("RUN_SET"):

		for run_alias in runs:
			run = runs[run_alias]

			with tag("RUN", alias = run_alias):
				doc.stag("EXPERIMENT_REF", refname = run["EXPERIMENT_REF"])
				
				with tag("DATA_BLOCK"):
				
					with tag("FILES"):

						doc.stag("FILE", 
							filename=run["filename_r1"], 
							filetype=run["filetype"],
							checksum_method="MD5",
							checksum=run["checksum_r1"])

						if "filename_r2" in run:
							doc.stag("FILE", 
								filename=run["filename_r2"], 
								filetype=run["filetype"],
								checksum_method="MD5",
								checksum=run["checksum_r2"])
	
	result = indent(doc.getvalue())
	return(result)


def to_dict(data, sheet):
	return_dict = {}
	keys = data[sheet].pop(0)

	for row in data[sheet]:
		row_dict = dict(zip(keys, row))
		return_dict[ row_dict["alias"] ] = row_dict
	
	return(return_dict)


def import_spreadsheet_data(file = "ena_submission_spreadsheet.ods"):
	data = get_data(file)

	for sheet in data:
		print("Processing sheet: {}".format(sheet))
		
		if sheet == "project":
			projects = to_dict(data, sheet)
			with open("project.xml", "w") as file:
				file.write(_project(projects))

		if sheet == "sample":
			samples = to_dict(data, sheet)
			with open("sample.xml", "w") as file:
				file.write(_sample(samples))

		if sheet == "experiment":
			experiments = to_dict(data, sheet)
			with open("experiment.xml", "w") as file:
				file.write(_experiment(experiments))

		if sheet == "run":
			runs = to_dict(data, sheet)
			with open("run.xml", "w") as file:
				file.write(_run(runs))


def main():
	import_spreadsheet_data()


if __name__ == "__main__":
	opts = set_up_argparse()
	main()
