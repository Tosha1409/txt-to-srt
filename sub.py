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
	timer = string.split(':')
	if len(timer)==2: timer = [0]+timer
	return (int(timer[0])*3600+int(timer[1])*60+int(timer[2]))

#converting time(seconds/integer) into string
def time_str (time):
	return (str(time // 3600).zfill(2)+ ':' + str((time % 3600) // 60 ).zfill(2) + ':' + str((time % 3600) % 60).zfill(2))

#generation of subtitles block/element
def generate_subs(num,time1,time2,text):
	return(str(num)+'\n'+time1+' --> '+time2+'\n'+text+'\n\n')


#program---------------------------------
#settings (will be moved to command line)
pause_time=5
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

#adding missed starting time, and ending time (must be added cases when real time between subtitles checked and added case when it is less then pause_time
#also saving srt file. and adding parts of second
counter=0
StartTime= subtitles_array[0]['StartTime']
for n in range(0, len(subtitles_array)):
	if (subtitles_array[n]['StartTime']==''): counter=counter+1
	else:
		subtitles_array[n]['EndTime'] = time_str(str_time(subtitles_array[n]['StartTime'])+pause_time)
		subtitles_array[n]['StartTime'] = time_str(str_time(subtitles_array[n]['StartTime']))
		if (counter>0):
			EndTime=subtitles_array[n]['StartTime']
			for m in range(n-counter, n): 
				subtitles_array[m]['StartTime']=time_str(str_time(subtitles_array[m-1]['StartTime'])+pause_time)
				subtitles_array[m]['EndTime']=time_str(str_time(subtitles_array[m]['StartTime'])+pause_time)
			counter=0
			StartTime=EndTime

#removing extra element (it doesnt needed anymore)
subtitles_array.pop()

#generating Dataframe and saving to CSV file
subs = DataFrame(data = subtitles_array, columns=['StartTime', 'EndTime', 'Text'])
subs.to_csv('file.csv', sep='\t', index=False, header=False)

#test for creating csvfile (will be removed)
#ready_file=open(subfile,'w')
#ready_file.write(generate_subs(1, '00:02:17,440', '00:02:30,375', 'Senator, were making our final approach into Coruscant'))
#ready_file.write(generate_subs(2, '00:02:31,476', '00:02:42,501', 'Very good, Lieutenant.'))
#ready_file.close()

print ('Done!!!')