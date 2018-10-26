import sys,srt, re
from pandas import DataFrame

#slicing string to two without cutting words to pieces. l - is max lenght of string and str - string itself
def lenght_limit(str,l):
	#checking if string is longer then max allowed lenght and that max allowed lenght is still longer then first word
	if ((len(str)>l) and len(str.split(' ',1)[0])<=l):
		#if whitespace symbol is next to maximal lenght, then lenght got increased because last letter of last word
		#still fits required lenght
		if (str[l] == ' '): l=l+1
		#making slicing if last symbol of substring of maximum allowed lenght is not whitespace
		if (str[l-1] != ' '):
			str1 = (str[:l].rsplit(' ',1))[0]
			str2 = str[len(str1)+1:]
		#slicing if it is whitespace
		else:
			str1 = str[:l-1]
			str2 = str[l:]
		#returning result of slicing as two strings
		return (str1,str2)
	#returning result if slicing didnt happened as two strings, where is second of is empty
	else:
		return (str,'')		
	
#checking if line of text fits suppoused template (starting time + subtitle text)
def string_format(str):
	#splitting line into starting time (if there is time) and textitself 
	#if there is no time then it returns first value as empty string
	if (re.match (r'^\d{1,2}(:[\d]{1,2}){1,2}',str)): timer, text = str.split(' ',1)
	else: timer, text = ('',str)
	return(timer,text)

#removes extra whitespaces from string
def remove_whitespaces(str): 
	return(re.sub( '\s+', ' ', str ).strip()+'\n')

#endtime calculation
def add_endtime():
	return()

#generation of subtitles
def generate_subs():
	return()

#settings (will be moved to command line)
pause_time=5
symbols_in_line=120
txtfile='sub.txt'
subtitles_array =[]

#opening and reading file
original_file=open(txtfile,'r')
subs=original_file.readlines()
original_file.close()

#stripping lines from extra whitespaces and adding to array that will be used for pandas
for line in subs:	
	time, str = string_format(remove_whitespaces(line.rstrip('\n')))
	#generating extra strings if text part was too long
	while (len(str)>symbols_in_line):
		newstr,str = lenght_limit(str,symbols_in_line)
		subtitles_array.append((time, '', newstr))
		time=''
	#adding string to array
	subtitles_array.append((time, '', str))
	
#generating Dataframe
subs = DataFrame(data = subtitles_array, columns=['StartTime', 'EndTime', 'Text'])

#saving to CSV file
subs.to_csv('file.csv', sep='\t', index=False, header=False)

print ('done!!!')