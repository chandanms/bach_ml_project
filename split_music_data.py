file = "dataset/F.txt"

f = open(file)

lines = f.readlines()

for col in range(0, 4) :
	line_list=[]
	for x in lines:
		line_list.append(x.rstrip("\n").split('\t')[col])
	
	with open("dataset/" + str(col+1) + '.txt', 'w') as filehandle:
		filehandle.writelines("%s\n" % res for res in line_list)
f.close()