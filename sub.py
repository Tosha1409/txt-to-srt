import sys,srt, re
from pandas import DataFrame

#slicing string to two without cutting words to pieces. l - is max lenght of string and string - string itself
def lenght_limit(string,l):
	#checking if string is longer then max allowed lenght and that max allowed lenght is still longer then first word
	if ((len(string)>l) and len(string.split(' ',1)[0])<=l):
		#if whitespace symbol is next to maximal lenght, then lenght got increased because last letter of last word
		#still fits required lenght
		if (string[l] == ' '): l=l+1
		#making slicing if last symbol of substring of maximum allowed lenght is not whitespace
		if (string[l-1] != ' '):
			str1 = (string[:l].rsplit(' ',1))[0]
			str2 = string[len(str1)+1:]
		#slicing if it is whitespace
		else:
			str1 = string[:l-1]
			str2 = string[l:]
		#returning result of slicing as two strings
		return (str1,str2)
	#returning result if slicing didnt happened as two strings, where is second of is empty
	else:
		return (string,'')		
	
#checking if line of text fits suppoused template (starting time + subtitle text)
def string_format(string):
	#splitting line into starting time (if there is time) and textitself 
	#if there is no time then it returns first value(time) as empty string
	if (re.match (r'^\d{1,2}(:[\d]{1,2}){1,2}',string)): timer, text = string.split(' ',1)
	else: timer, text = ('',string)
	return(timer,text)

#returns dictonary "elements" that can be added to array
def sub_element(str1,str2,str3):
	return (dict(zip(('StartTime', 'EndTime', 'Text'), (str1, str2, str3))))

#removes extra whitespaces from string
def remove_whitespaces(string): 
	return(re.sub( '\s+', ' ', string).strip())

#converting time(string) to integer(seconds)
def str_time (string):
	timer = string.replace(',', '.').split(':')
	if len(timer)==2: timer = [0]+timer
	return (float(timer[0])*3600+float(timer[1])*60+float(timer[2]))

#converting time(seconds/integer) into string
def time_str (time):
	return ((str(int(time // 3600)).zfill(2)+ ':' + str(int((time % 3600) // 60 )).zfill(2) + ':' + str('{:06.3f}'.format(float((time % 3600) % 60))).replace('.',',')))

#generation of subtitles block/element
def generate_subs(num,time1,time2,text):
	return(str(num)+'\n'+time1+' --> '+time2+'\n'+text+'\n\n')


#program---------------------------------
#settings (will be moved to command line)
pause_time=5
minimum_time=0.001
symbols_in_line=120
txtfile='sub.txt'
subfile='sub.srt'
subtitles_array =[]

#opening and reading file
original_file=open(txtfile,'r')
subs=original_file.readlines()
original_file.close()

#stripping lines from extra whitespaces and adding to array that will be used for pandas
for line in subs:
	time, string = string_format(remove_whitespaces(line))
	#generating extra strings if text part was too long
	while (len(string)>symbols_in_line):
		newstr,string = lenght_limit(string,symbols_in_line)
		subtitles_array.append(sub_element(time, '', newstr))
		time=''
	#adding string to array
	subtitles_array.append(sub_element(time, '', string))
#adding extra for correct handling (used for next code block)
subtitles_array.append(sub_element('10:10:10', '', ''))

#checking if first line have correct time
if (subtitles_array[0]['StartTime']==''):
	print ('Subtitles file is broken (first line doesnt have timemark)')
	sys.exit()

#adding missed starting time, and ending time (must be added cases when real time between subtitles checked and added case when it is less then pause_time
#also saving srt file. and adding parts of second
counter=0
for n in range(0, len(subtitles_array)-1):
	#if next line doesnt have StartTime increasing counter
	if ((subtitles_array[n+1]['StartTime']=='')): counter=counter+1
	else:
		#making time delta equal to pause time as default
		time_delta = pause_time
		#if this and next line have starting time
		if (counter==0):
			#counting time delta (or rather changing time delta if is in reality smaller then pause time)
			if ((str_time(subtitles_array[n+1]['StartTime'])-str_time(subtitles_array[n]['StartTime']))<=pause_time):
				time_delta = str_time(subtitles_array[n+1]['StartTime'])-str_time(subtitles_array[n]['StartTime'])-minimum_time
			#normalizing Time stamps and counting ending time 
			subtitles_array[n]['StartTime'] = time_str(str_time(subtitles_array[n]['StartTime']))
			subtitles_array[n]['EndTime'] = time_str(str_time(subtitles_array[n]['StartTime'])+time_delta)
		#working with block of lines, where is missed timestamps
		if (counter>0):
			#counting time delta (or rather changing time delta if is in reality smaller then pause time)
			if (n!=len(subtitles_array)-1) and (((str_time(subtitles_array[n+1]['StartTime'])-str_time(subtitles_array[n-counter]['StartTime']))/(counter+1))<=pause_time):
				time_delta = ((str_time(subtitles_array[n+1]['StartTime'])-str_time(subtitles_array[n-counter]['StartTime']))/(counter+1))			
			#loop for block of lines that normalizing timestamps and counting EndTime
			for m in range(n-counter, n+1):
				subtitles_array[m]['StartTime']=time_str(str_time(subtitles_array[m]['StartTime']))
				if ((m==n) and not (time_delta<pause_time)):subtitles_array[m]['EndTime']=time_str(str_time(subtitles_array[m]['StartTime'])+time_delta) 
				else:
					subtitles_array[m+1]['StartTime']=time_str(str_time(subtitles_array[m]['StartTime'])+time_delta)
					subtitles_array[m]['EndTime']=time_str(str_time(subtitles_array[m]['StartTime'])+time_delta-minimum_time)
		counter=0
			
#removing extra element (it doesnt needed anymore)
subtitles_array.pop()

#creating subtitles file
ready_file=open(subfile,'w')
for n in range(0,len(subtitles_array)):
	ready_file.write(generate_subs(n+1, subtitles_array[n]['StartTime'], subtitles_array[n]['EndTime'], subtitles_array[n]['Text']))		
ready_file.close()

print ('Done!!!')