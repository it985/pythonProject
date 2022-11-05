import os

folder = input('请输入文件夹名:')
file_folder = os.getcwd()+'\\'+folder

n = 0
for file_name in os.listdir(file_folder):
	n += 1
	#下面我只设置到1000个文件的情况，超出可能会顺序错误，可以自行修改
	if n < 10:
		name = '00'+str(n)
	elif 9 < n < 100:
		name = '0'+str(n)
	elif 99 < n < 1000:
		name = str(n)
	else:
		name = str(n)
	place_number = 0
	place_number_list = []
	for t in file_name:
		if t == '.':
			place_number_list.append(place_number)
		place_number += 1
	Format = file_name[place_number_list[-1]:]
	save_name = name + Format
	oldname = file_folder+'\\'+file_name
	newname = file_folder+'\\'+save_name
	os.rename(oldname,newname)
