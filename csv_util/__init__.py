import csv
from os import listdir
from os import isfile, join
class CSVDirectory:
	def __init__(self, directory = ""):
		self.directory = directory
		if len(self.directory) > 0:
			self.ls = [f for f in listdir(self.directory) if isfile(join(self.directory, f)) and f.endswith(".csv")]
		print("Note : It's better to make use of pandas.\n\n\tpd.read_csv(\"actors.csv\").to_dict(orient=\"row\")\n")
	def get_csv_records(self, filename):#loads a horizontally loaded file record 
		records = []
		with open(filename) as csvfile:
			reader = csv.reader(csvfile)
			records.extend([r for r in reader])
		return records

	def get_csv_records_with_keys(self, filename):
		records = []
		with open(filename) as csvfile:
			reader = csv.DictReader(csvfile)
			records.extend([r for r in reader])
		return records

	def get_csv_with_headers(self, filename):
		records = {}
		csvfile = open(filename)
		reader = csv.reader(csvfile)
		headers = next(reader)
		for i in headers:
			records[i] = []
		for record in reader:
			for i in range(len(headers)):
				try:
					records[headers[i]].append(record[i])
				except:
					records[headers[i]].append("")
		return records 
