from os import mkdir
from os import listdir
import os
from os.path import splitext

def operations_on_files(path_to_files,lable) :
	files = listdir(path_to_files)
	for current_file in files :
		input_file=path_to_files+current_file
		output_file=path_to_project+"XXD_files/"+lable+"/"
		print(lable+' : '+current_file+"\n converted into BYTE_SEQUENCE")
		var = "xxd "+input_file +" "+output_file+splitext(current_file)[0] +".txt"
		os.system(var)
	print("All files are converted in to Byte Sequences...")
	XXD_Benign_file_path=path_to_project+'XXD_files/Benign/'
	XXD_malicious_file_path=path_to_project+'XXD_files/Malicious/'
	Benign_files=listdir(path_to_project+'XXD_files/Benign/')
	Malicious_files=listdir(path_to_project+'XXD_files/Malicious/')
	print("Collecting n_grams from Benign_files...")
	if lable=='Benign' :
		directory=Benign_files
	else :
		directory=Malicious_files
	for files in directory :
		print(lable+'  :'+files)
		file_opend=open(path_to_project+'XXD_files/'+lable+'/'+files,'r')
		single_line=''
		for line in file_opend:
			current_line=line.split()[1:9]
			for current_word in current_line:
				if '.' and '|' and '@' and '~' not in current_word:
						single_line+=current_word
		file_opend.close()
		for n_size in n_gram_size :
			n_size=2*n_size
			n_gram_list=[]
			for i in range(0,len(single_line),2):
				this_n_gram=single_line[i:i+n_size]
				if len(this_n_gram) == n_size :
					n_gram_list.append(this_n_gram)
			n_gram_set = set(n_gram_list)
			n_gram_list = list(n_gram_set)
			f=open(path_to_project+'n_grams/'+lable+'/'+'n_grams_'+str(int(n_size/2))+'/'+splitext(files)[0]+'.txt','w')
			for n_gram in n_gram_list :
				f.write("%s\n"%n_gram)
			f.close()

def common_feature_based_reduction():
	for size in n_gram_size:
		flag=0
		benign_set=set()
		benign_n_gram_files=listdir(path_to_project+'n_grams/Benign/n_grams_'+str(size))
		for each_file in benign_n_gram_files :
			this_file_set=set()
			print(path_to_project+'n_grams/Benign/n_grams_'+str(size)+'/'+each_file)
			f=open(path_to_project+'n_grams/Benign/n_grams_'+str(size)+'/'+each_file,'r')
			for line in f:
				this_file_set.add(line.strip('\n'))
			if flag==0 :
				benign_set=benign_set.union(this_file_set)
				flag=1
			else :
				benign_set=benign_set.intersection(this_file_set)
			print(size,'  Reduced  ',len(benign_set),len(this_file_set))
		f1 = open(path_to_project+'common_features/Benign/Benign_features_'+str(size)+'.txt','w')
		for each_feature in benign_set:
			f1.write("%s\n"%each_feature)
		f1.close()
		flag=0
		malicious_set=set()
		malicious_n_gram_files=listdir(path_to_project+'n_grams/Malicious/n_grams_'+str(size))
		for each_file in malicious_n_gram_files :
			this_file_set=set()
			print(path_to_project+'n_grams/Malicious/n_grams_'+str(size)+'/'+each_file)
			f=open(path_to_project+'n_grams/Malicious/n_grams_'+str(size)+'/'+each_file,'r')
			for line in f:
				this_file_set.add(line.strip('\n'))
			if flag==0 :
				malicious_set=malicious_set.union(this_file_set)
				flag=1
			else :
				malicious_set=malicious_set.intersection(this_file_set)
			print(size,'  Reduced  ',len(malicious_set),len(this_file_set))
		f2=open(path_to_project+'common_features/Malicious/Malicious_features_'+str(size)+'.txt','w')
		for each_feature in malicious_set:
			f2.write("%s\n"%each_feature)
		f2.close()
	
		final_reduced_set = (benign_set.difference(malicious_set)).union(malicious_set.difference(benign_set))
		f3 = open(path_to_project+'common_features/reduced_set_'+str(size)+'.txt','w')
		for each_feature in final_reduced_set:
			f3.write('%s\n'%each_feature)
		f3.close()
		
def generate_training_arff_file() :
	for size in n_gram_size :
		f=open(path_to_project+'ARFF/n_grams_'+str(size)+'/'+'train.arff','w')
		f.write('@RELATION training\n\n')
		header_arff={}
		count=1
		f1=open(path_to_project+'common_features/reduced_set_'+str(size)+'.txt','r')
		final_reduced_set = []
		for each_line in f1:
			final_reduced_set.append(each_line.strip('\n'))
		f1.close()
		for each_feature in final_reduced_set :
			header_arff[each_feature] = 'a'+str(count)
			count+=1
		for each_header in header_arff:
			f.write('@ATTRIBUTE %s {0,1}\n'%header_arff[each_header])
		f.write('@ATTRIBUTE class {Benign,Malicious}\n\n')
		f.write('@DATA\n')
		benign_train_n_grams=listdir(path_to_project+'n_grams/Benign/n_grams_'+str(size)+'/')
		for each_benign_file in benign_train_n_grams :
			current_data_line=[0 for i in range(len(header_arff))]
			for header in header_arff :
				#print(each_benign_file,header,size,path_to_project+'n_grams/Benign/n_grams_'+str(size)+'/'+each_benign_file)
				if header in open(path_to_project+'n_grams/Benign/n_grams_'+str(size)+'/'+each_benign_file,'r').read():
					current_data_line[int(header_arff[header][1:])-1]=1
			for key in current_data_line:
				f.write('%s,'%key)
			f.write('Benign\n')
		malicious_train_n_grams=listdir(path_to_project+'n_grams/Malicious/n_grams_'+str(size)+'/')
		for each_benign_file in malicious_train_n_grams :
			current_data_line=[0 for i in range(len(header_arff))]
			for header in header_arff :
				#print(each_benign_file,header,size,path_to_project+'n_grams/Malicious/n_grams_'+str(size)+'/'+each_benign_file)
				if header in open(path_to_project+'n_grams/Malicious/n_grams_'+str(size)+'/'+each_benign_file,'r').read():
					current_data_line[int(header_arff[header][1:])-1]=1
			for key in current_data_line:
				f.write('%s,'%key)
			f.write('Malicious\n')
		
if __name__ == '__main__' :
	global path_to_project
	path_to_project = '/home/sandhya/Documents/Project/'
	try :
		mkdir(path_to_project+'XXD_files')
	except IOError :
		pass
	print("Path created for XXD_files...")
	try :
		mkdir(path_to_project+'XXD_files/Benign/')
	except IOError :
		pass
	try :
		mkdir(path_to_project+'XXD_files/Malicious/')
	except IOError :
		pass
	try :
		mkdir(path_to_project+'n_grams/')
	except IOError :
		pass
	try :
		mkdir(path_to_project+'n_grams/Benign/')
	except IOError :
		pass
	try :
		mkdir(path_to_project+'n_grams/Malicious/')
	except IOError :
		pass

	n_gram_size=[4,5,6]
	try :
		for size in n_gram_size:
				mkdir(path_to_project+'n_grams/Benign/n_grams_'+str(size))
	except IOError :
		pass
	try :
		for size in n_gram_size:
				mkdir(path_to_project+'n_grams/Malicious/n_grams_'+str(size))
	except IOError :
		pass
	print("path created for n_grams")

	try:
		mkdir(path_to_project+'common_features/')
	except IOError:
		pass
	try :
		mkdir(path_to_project+'common_features/Benign/')
	except IOError :
		pass
	try :
		mkdir(path_to_project+'common_features/Malicious/')
	except IOError:
		pass
	try :
		mkdir(path_to_project+'ARFF/')
	except IOError:
		pass
	for size in n_gram_size :

		try :
			mkdir(path_to_project+'ARFF/n_grams_'+str(size))
		except IOError :
			pass
	operations_on_files(path_to_project+'DataSet/BenignDrivers/Benign/','Benign')
	operations_on_files(path_to_project+'DataSet/Malicious/','Malicious')
	common_feature_based_reduction()
	generate_training_arff_file()




