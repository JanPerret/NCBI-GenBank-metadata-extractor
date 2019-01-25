
### creating a list of every file finishing with ".seq" in the folder where the script is located
import glob
file_list=glob.glob('*.seq')

# loop to supress the first 10 lines of every listed file
for i in range(len(file_list)) :
	file=file_list[i]
	with open(file, 'r') as myfile:
		data = myfile.read()
	if data[0:5] != "LOCUS" : # condition : if the first 5 characters of the file are "LOCUS", the file is not shortened
		print(file)
		with open(file, 'r') as fin:
			data = fin.read().splitlines(True)
		with open(file, 'w') as fout:
			fout.writelines(data[10:])
	else :
		print(file, 'has already been shortened')

print("Done !")