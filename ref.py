import sys
import fileinput
import re
path = "/Users/meow/Desktop/DP/Code/Reference.txt"
num_line = 1
def filter(line):
	pattern=re.compile('“(.*)”')
	title=pattern.findall(line)
	isP = False
	if len(title)>0:
		print(title[0])
	else:
		temp_line = line.split(',')
		for i in range(len(temp_line)):
			if isP:
				break
			if re.match(r'[1-9]|[A-Z]\.', temp_line[i]) or i == 0:
				continue
			else:
				print(temp_line[i])
				isP=True
for line in fileinput.input(path):
	temp_line = line.strip()
	print("Line ", num_line)
	filter(temp_line)
	num_line+=1