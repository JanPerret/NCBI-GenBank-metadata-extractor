
###############################################################
### To measure the execution time of the program
### Script taken from : https://stackoverflow.com/a/12344609/10890752
import atexit
from time import time, strftime, localtime
from datetime import timedelta

def secondsToStr(elapsed=None):
    if elapsed is None:
        return strftime("%Y-%m-%d %H:%M:%S", localtime())
    else:
        return str(timedelta(seconds=elapsed))

def log(s, elapsed=None):
    line = "="*40
    print(line)
    print(secondsToStr(), '-', s)
    if elapsed:
        print("Elapsed time:", elapsed)
    print(line)
    print()

def endlog():
    end = time()
    elapsed = end-start
    log("End Program", secondsToStr(elapsed))

start = time()
atexit.register(endlog)
log("Start Program")
###############################################################


### reading the GenBank file
### enter the genbank file name from which you want to extract the data (the output file of the "...Genebank_references_selection.py" program or any other genbank file)
gb_file_name = ""
gb_file_name = str(input("Enter your NCBI gene bank file name (including the file extension) : "))


def GB_info_extraction(filename, outf):
	fin = open(filename, "r")
	num_lines = sum(1 for line in open(filename))
	print("File has "+str(num_lines)+" lines.")
	
	line_count = 0
	access_num = ""
	parsing_definition = False
	definition = ""
	species = ""
	parsing_organism = False
	organism = ""
	sub_date = ""
	year = ""
	parsing_address = False
	address = ""
	mol_type = ""
	country = ""
	latlon = ""
	
	### This loop reads a GenBank .seq (or .txt) file line by line
	### every time a given "keyword" is met in the first 10 characters of a line
	### or if the line contain a longer string (if the field name isn't in the firs 10 characters),
	### the associated information is stored in an object
	### when the keyword "LOCUS     " is met again, the GenBank reference is written in the output file.
	### No condition is tested here, so every reference in the input file will figure in the output table.
	for line in fin:
		line_count += 1
		keyword = line[:10]
		if keyword == "LOCUS     ":
			if access_num:
				ref_infos = access_num+','+species+','+year+','+latlon+','+country+','+definition+','+mol_type+','+sub_date+','+address+','+organism
				outf.write('\n'+ref_infos)
			
				definition = ""
				species = ""
				organism = ""
				sub_date = ""
				year = ""
				address = ""
				mol_type = ""
				country = ""
				latlon = ""
			access_num = line[12:21].strip()
		if keyword == "DEFINITION":
			definition = line[12:].strip()
			definition = definition.replace(',','')
			parsing_definition = True
			continue
		if keyword == "ACCESSION ":
			parsing_definition= False
			continue
		if parsing_definition:
			definition = definition + ' ' + line.strip()
			definition = definition.replace(',','')
			continue
		if keyword == "  ORGANISM":
			species = line[11:].strip().replace(',','')
			if " sp." in species:
				species = species.split(".",1)[0]
			parsing_organism = True
			organism = line[11:].strip()			
			continue
		if keyword == "REFERENCE ":
			parsing_organism = False
			continue
		if parsing_organism:
			organism = organism + ' ' + line.strip()
			continue
		if "  JOURNAL   Submitted (" in line:
			sub_date = line[23:34]
			year = line[30:34]
			parsing_address = True
			address = line[35:].strip().replace(',','')
			continue
		if keyword == "FEATURES  " or keyword == "COMMENT   " :
			parsing_address = False
			continue
		if parsing_address:
			address = address + ' ' + line.strip()
			address = address.replace(',','').replace('\n',' ')#.replace('/',' ') # the last replace() is to break the URL links because they seem to be a possible bug source
			continue
		if '                     /mol_type="' in line:
			mol_type = line[31:].strip().replace('"','').replace(',','')
			continue
		if '                     /country="' in line:
			country = line[30:].strip().replace('"','').replace(',','')
			continue
		if '                     /lat_lon="' in line:
			latlon = line[30:].strip().replace('"','').replace(',','')
			continue
		if line_count == num_lines: # to write the infos from the last reference when the end of the file is reached
			ref_infos = access_num+','+species+','+year+','+latlon+','+country+','+definition+','+mol_type+','+sub_date+','+address+','+organism
			outf.write('\n'+ref_infos)

	fin.close()


outf = open('RESULT_GENBANK_'+gb_file_name,'w') # opening a file to write the output
outf.write('access_num'+','+'species'+','+'year'+','+'lat-lon'+','+'country'+','+'definition'+','+'molecule_type'+','+'submission_date'+','+'address'+','+'taxonomy')
GB_info_extraction(gb_file_name, outf)
outf.close()



### to print the execution time of the program
def endlog():
    end = time()
    elapsed = end-start
    log("End Program", secondsToStr(elapsed))
endlog()
