# NCBI-GenBank-metadata-extractor

### General purpose

This suite of programs extracts some meta-data from the .seq files of NCBI GenBank,
with a final output being a table with one line per GenBank reference and the following columns :
accession number, species, submission year, sequencer nationality, sample origin, latitude and longitude of the origin of the sample.
It was made with the files of the 228 release from October 2018, and for animal, fungi and plants files only. Thus, it may need some modification in order to be used for other files.

It was first based on dewshr's NCBI-GenBank-file-parser : https://github.com/dewshr/NCBI-GenBank-file-parser

But because I had to parse a large number of files, I changed the approach into a step by step way in order to have intermediate result files decreasing in size at each step.
I choosed a line by line scanning way of the files that permit to gain in execution time.
The only module to import is the "glob" module that permit to list the files name in a folder.
In addition different modules are needed if you choose to use the same way of measuring the execution time (first 30 lines of each script) but it is not necessary.


### Description of each script

1_supp_10_first_lines_all_.seq_files.py
This program deletes the first 10 lines of every file ending with ".seq" that is located in the folder where the script is.
This first 10 lines correspond to the GenBank release information and could enter in conflict with the following programs so I chose to get rid of them.

2_fungi_ITS_Genebank_references_selection.py
This program scans the .seq files line by line and puts in one .txt file all the references that meet the specified conditions. I made different versions of the program : 
 - fungi_ITS extracts every reference that corresponds to a fungal sequence of the ITS (Internal Transcribed Spacer) gene,
 - animal_COI extracts the animal COI (Cytochrome Oxidase I) sequences
 - plant_MatK extracts the plant MatK (Maturase K) sequences
 - plant_rbcL extracts the plant rbcL (ribulose 1,5-bisphosphate carboxylase L subunit)
It can easily be modified to select references on other conditions (other taxa/gene couples or conditions on other information fields than only the taxonomic group and the gene name).

3_Genebank_file_parser_v6.py
This program opens the file whose name is given by the user at the beginning of the execution of the program (typically the output file of the "..._Genebank_references_selection.py" programs,
or any other file that has the same structure than the .seq GenBank files).
The file is scanned line by line and some information are stored in objects and written into a .txt output file (a comma-separated table).
The information extracted in this version are : accession number, species name, submission year, latitude and longitude of the origin of the sample,
origin country of the sample, definition of the reference (= the title), molecule type, submission date, address of the lab who did the sequencing, taxonomy of the species.

4_Genbank_simple_table_maker.py
This program is meant to be used on the output file of the Genebank_file_parser_v6.py (it splits every line of the input file by commas, so it has to be a comma-separated table).
For each line of the table in input, it keeps only the following fields : the accession number, the species name, the submission year, the origin country of the sample and the lat/lon of the origin place of the sample.
In addition to that it performs a country name search in the address of the lab where the sequencing was done in order to add a column with the "nationality of the sequencer".
The possible country names are taken from the "GenBank_country_v2.txt" file, and some multiple assignation errors are corrected as indicated in the "country_assignation_errors.txt" file (see below).

GenBank_country_v2.txt
A list of the possible country names met in the address field of GenBank. 
The list is based on the official country list for the "/country" qualifier found here : https://www.ncbi.nlm.nih.gov/genbank/collab/country/

I added to the list the common typing/filling errors that I found (for example "U.K" instead of "UK", or "Belgique" instead of "Belgium").
Each  country name is associated to the "final" chosen country name.

country_assignation_errors.txt
A list of the common country multiple-assignation errors I saw. For example, for the EU512160 reference, the address is : 
"Biology, New Mexico State University, Sweet and Horseshoe, Foster Hall, Rm 201, Las Cruces, NM 88001, USA"
So it will be assigned to 2 countries : USA and Mexico. As a correction, every reference associated to these two countries will me corrected to "USA" only.
Of course for new search criteria another you may need to make your own multiple-assignation correction list.


### Program Requirements
- python 3.7
- import glob module


### To download NCBI GeneBank files
ftp://ftp.ncbi.nlm.nih.gov/genbank/


### Funding
These programs were written during a work at the Center for Functional and Evolutionary Ecology (or "Centre d'Ecologie Fonctionnelle et Evolutive") in Montpellier, France : https://www.cefe.cnrs.fr/fr/

This work was funded by the Biodivmex program : http://biodivmex.imbe.fr/


### License
	NCBI-GenBank-metadata-extractor is a program made to extract some metadata
	from NCBI GenBank files in plain text format.
  Copyright (C) 2019 Jan Perret

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
	along with this program. If not, see <https://www.gnu.org/licenses/>.
