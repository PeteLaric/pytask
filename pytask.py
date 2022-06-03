# pytask.py
# A simple task manager, written in Python!
# (cc) 2022-04-15 BY Pete Laric / PeteLaric.com
#
# I wrote this ultra-simple task scheduler to automate turning a cryptocurrency mining rig on
# and off to coincide with solar power availability.  Python isn't my favorite language, but I
# chose it for this project because I wanted the resulting product to be cross-platform with
# little to no modification being necessary for use with any modern operating system.
#
# To invoke:
#
#	python3 pytask.py
#
# The example task list, tasks.csv, creates a bot that announces the current time every 15
# minutes.  To get this to work correctly in Linux, you will need to install espeak-ng like so:
#
#	sudo apt-get update
#	sudo apt-get upgrade
#	sudo apt-get install espeak-ng
#
# This example could probably be modified to work with other operating systems as well.  I will
# leave that to others for now.  Again, I wrote this utility for my own use, but I'm sharing it
# with you, because that's just the sort of guy I am!  ;-)
#
# The task list file is a pretty straightforward spreadsheet.  At present, there are three
# columns: hour, minute, and path.  It would be easy to mod this program to perform tasks only
# on certain dates, days of the week, etc., but I don't care about that, so I'm not going to do
# that right now.  As currently implemented, when the current time matches a task's scheduled
# time, the command line statement given by path will execute.  This is essentially the same as
# typing that command into the terminal yourself.  Because it's a CSV file (comma-separated
# values), be careful not to use commas in the path itself, or it will get confused.  Also, note
# that we use military time here: 1PM is 13, 11PM is 23, etc.  This is more elegant and less
# ambiguous than all this "AM/PM" crap.
#
# Enjoy!
# ~Pete


import os
import time
from datetime import datetime
import pandas # from https://realpython.com/python-csv/ 


df = pandas.read_csv('tasks.csv') #df = DataFrame: https://realpython.com/pandas-dataframe/
print(df)

hours = df['hour']
mins = df['min']
paths = df['path']

num_tasks = len(paths)
print("num_tasks: " + str(num_tasks))

# array of flags to keep track of which tasks we've already completed.
# we don't want to execute each task multiple times, just because it's still the same minute!
executed = [False] * num_tasks #use Boolean data type, because why not?

active = True
while (active == True): #loop forever
	for i in range(num_tasks): #check each task against current time
		if (executed[i]):
			print("*", end="")
		print("task " + str(i), end=", ")
		target_hour = hours[i]
		target_minute = mins[i]
		system_command = paths[i] #"ls" "~/mine.sh"
		
		#check_and_exec(target_hour, target_minute, system_command)
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")
		#current_time = now.strftime("%H:%M")
		#print("Current Time =", current_time)
		print("current_time = " + current_time, end=", ")

		#hour = now.strftime("%H")
		hour = int(now.strftime("%H"))
		#print("hour =", hour)

		#minute = now.strftime("%M")
		minute = int(now.strftime("%M"))
		#print("minute =", minute)

		second = now.strftime("%S")
		second = int(now.strftime("%S"))
		#print("second =", second)

		print("target = " + str(target_hour) + ":" + str(target_minute))

		if ((hour == target_hour) and (minute == target_minute) and (executed[i] == False)):
			print("GO, GO, GO!!!")
			os.system(system_command)
			executed[i] = True
		elif (((hour != target_hour) or (minute != target_minute)) and (executed[i] == True)):
			# reset "executed" flag -- we don't need it anymore (because current time no longer aligns with trigger)
			executed[i] = False

	print("\n")

print("pytask exited normally.")

