
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


### reading the table resulting from the GenBank parser
table_file_name = ""
table_file_name = str(input("Enter your table file name (including the file extension) : "))


def Simple_table_maker(table_file_name, output_table):
	fin = open(table_file_name, "r")
	country_index = open("GenBank_country_v2.txt", "r")
	country_names = []
	country_finals = []
	country_line_list = []
	for line in country_index:
		country_line_list = line.split(",",1)
		country_names.append(" " + country_line_list[0].lower().replace('\n','') + " ") # makes a list of the possible country names with a space before and after each name
		country_finals.append(country_line_list[1].replace('\n','')) # makes a list of the 'final' country names I choosed associated with the country names of the precedent list
	length = len(country_names)
	address_search = ""
	name_final = ""

	
	errors = open("country_assignation_errors.txt", "r")
	error_names = []
	error_correct = []
	errors_line_list = []
	for line in errors:
		errors_line_list = line.split(",",1)
		error_names.append(errors_line_list[0].replace('\n','')) # makes a list of the common multiple-assignation errors that will be automatically corrected
		error_correct.append(errors_line_list[1].replace('\n','')) # makes a list of the correct country assignations associated with the precedent list
	length2 = len(error_names)
	error = ""
	correct = ""
	
	access_num = ""
	definition = ""
	species = ""
	organism = ""
	sub_date = ""
	year = ""
	address = ""
	mol_type = ""
	country = ""
	latlon = ""
	name = ""
	address_low = ""
	sequencer_nationality = ""
	line_list = []
	ref_infos = ""
	line_cnt = 1;

	### This loop reads a comma-separated table file line by line
	### for each line, only a certain amount of data is transcribed in the output file :
	### the accession number, the species name, the submission year, the nationality of the sequencer lab,
	### the origin country of the sample and the lat/lon of the origin place of the sample.
	### To go from the address to the nationality of the sequencing lab, a research of the country names contained 
	### in the "GenBank_country_v2.txt" is made.
	### Some multiple-assignation errors (contained in the "country_assignation_errors.txt" file) are directly corrected.
	### This correction list is arbitrary and corresponds to the errors I personally corrected by checking the address of every
	### multiple-assignation case I had for my use of these programs (release 228, COI+animals / ITS+fungi / MatK+plant / rbcL+plant selection criteria).
	### For every new type of reference selection criteria you may need to establish your own multiple-assignation correction list,
	### as well as your own country list because I took into account the most common typing errors in country names that I saw for my search criteria
	### but there might be other errors for other researches.
	first_line = fin.readline() # to not take into account the first line with the columns headings
	for line in fin:
		line_cnt += 1
		line_list = line.split(",")
		if len(line_list) < 9:
			print("Error in line " + str(line_cnt) + ": " + str(line_list))
			continue
		access_num = str(line_list[0])
		species = str(line_list[1])
		year = str(line_list[2])
		address = str(line_list[8])
		country = str(line_list[4])
		latlon = str(line_list[3])
		if ":" in country:
			country = country.split(":",1)[0]
		if address:
			address_search = address.lower()
			address_search = address_search.replace("."," ").replace(","," ").replace(";"," ").replace(":"," ").replace("'"," ").replace("("," ").replace(")"," ").replace("-"," ")
			address_search = " " + address_search + " "
			for n in range(0,length):
				name = country_names[n]
				name_final = country_finals[n]
				if name in address_search: # assignation of each country name found in the address to the "sequencer_nationality" object
					sequencer_nationality = sequencer_nationality + ' ' + name_final
		sequencer_nationality = sequencer_nationality.strip()
		if sequencer_nationality:
			for n in range(0,length2):
				error = error_names[n]
				correct = error_correct[n]
				if error in sequencer_nationality: # if a common country multiple-assignation case is found, it is corrected like it is written in the "country_assignation_errors.txt" file
					sequencer_nationality = correct
		ref_infos = access_num+','+species+','+year+','+sequencer_nationality+','+country+','+latlon
		access_num = ""
		species = ""
		year = ""
		sequencer_nationality = ""
		country = ""
		latlon = ""
		address = ""
		address_low = ""
		output_table.write('\n'+ref_infos)


output_table = open('SIMPLE_'+table_file_name,'w') # opening a file to write the output
output_table.write('access_num'+','+'species'+','+'year'+','+'sequencer_nationality'+','+'sample_origin'+','+'lat-lon')
Simple_table_maker(table_file_name, output_table)
output_table.close()


### to print the execution time of the program
def endlog():
    end = time()
    elapsed = end-start
    log("End Program", secondsToStr(elapsed))
endlog()
