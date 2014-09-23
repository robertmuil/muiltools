import calendar, random, pdb
import numpy as np

msg='well hallelujah'

holiday = {'2011':[[1],[],[],[22,25],[1],[2,13],[],[],[],[3],[],[25,26]], 
           '2012':[[1],[],[],[6,9],[1,17,28],[],[],[],[],[3],[],[25,26]],
           '2013':[[1],[],[29],[1],[1,9,20],[],[],[],[],[3],[],[25,26]]}

year = int(raw_input("Generate data for what year? "))
month = int(raw_input("Generate data for what month? "))
hours_to_spend = int(raw_input("How many hours do you want to spend? "))
minhours = raw_input("Is there a minimum of hours you want to spend every day? ")
if not minhours: minhours = 0
else: minhours = int(minhours)

notuse = raw_input("Type in all the days you want to keep free, e.g. \"11,12,14,23,24,25\": ")
if notuse:
    notuse = np.array(notuse.split(',')).astype(np.int)
else: notuse=[]

a = raw_input("Optional: Type in min and max of noise factor, default = \"0.5,1.5\": ")
if a:
    [gaussmin, gaussmax] = np.array((a).split(',')).astype(np.float)
else:
    gaussmin = 0.5
    gaussmax = 1.5
#global diff
diff = 0 

myCal = calendar.Calendar()

days = np.array(myCal.monthdayscalendar(year,month))
used_days = np.ones(days.shape)
used_days[days==0] = 0


def add_to_random_workday(amount, spent_hours):
    while True:
        ind = int(random.random()*len(spent_hours))
        if (spent_hours[ind] == 0):
            continue
        else:
            spent_hours[ind] += amount
            return spent_hours

for i in range(len(used_days)):
    # Weekend
    used_days[i][-2:] = 0
    for j in range(len(used_days[i])):
        # Remove those days that are holidays or in notuse list.
        if (days[i][j] in notuse) or (days[i][j] in holiday[str(year)][month-1]):
            used_days[i][j] = 0
            
used_days = used_days.astype(np.bool)             
no_days = len(days[used_days])

spent_hours = (used_days * (hours_to_spend / float(no_days))).flatten()

for i in range(len(spent_hours)):
    if (spent_hours[i] == 0):
        continue
    else:
        #pdb.set_trace()
        tmp2 = diff # difference from last loop
        randomfact = random.random()*(gaussmax-gaussmin)+gaussmin
        diff = spent_hours[i] - int(np.round(spent_hours[i] * randomfact))
        spent_hours[i] = int(np.round(spent_hours[i] * randomfact))
        
        spent_hours[i] += int(tmp2) # add diff from last loop
        diff = diff + tmp2-int(tmp2)

spent_hours = add_to_random_workday(int(diff)+1,spent_hours)

#pdb.set_trace()
if np.sum(spent_hours) > hours_to_spend:
    for x in range(int(np.sum(spent_hours) - hours_to_spend)):
        spent_hours = add_to_random_workday(-1, spent_hours)

        
for i in range(len(spent_hours)):
    if (spent_hours[i] < minhours) and not (spent_hours[i] == 0):
        tmp = spent_hours[i]
        spent_hours[i] = 0
        for i in range(int(tmp)):
            spent_hours = add_to_random_workday(1, spent_hours)

#print np.sum(spent_hours)

days = days.flatten()

    
import sys
for i in range(len(days)):
    if not (days[i] == 0):
        sys.stdout.write(str(int(spent_hours[i])) + "\t")
        

for i in range(len(days)):
    if not (days[i] == 0):
        print str(days[i]) + ": " + str(spent_hours[i])
print "========"
print "      "+str(int(np.sum(spent_hours)))

import pylab as pp
pp.ion()
pp.plot(range(len(spent_hours)),spent_hours,'ob-')
raw_input("Enter for end:")

