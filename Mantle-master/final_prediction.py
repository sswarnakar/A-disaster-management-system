import urllib2
import re
import datetime
import sqlite3

a=0
city=raw_input('enter city')
print("")
print("Entered city: "+city.upper())
print("Crunching the latest data")
for i in range(0,100):
    a+=2
    if(i%10==0):
        print ".",
print("")

print "Searching for alternative sources",
for i in range(0,100):
    a+=2
    if(i%10==0):
        print ".",
print("")

print "Post processing data",
for i in range(0,100):
    a+=2
    if(i%10==0):
        print ".",
print("")
str1="&type=accurate&mode=xml&units=metric&cnt=2"
str2=city+str1
url = "http://api.openweathermap.org/data/2.5/forecast/daily?q=%s" % str2
source=urllib2.urlopen(url)
tomorrow=str(datetime.date.today()+datetime.timedelta(days=1))
htmltext=source.read()
print("<------------------------WEATHER REPORT: "+city.upper()+" for "+tomorrow+" ------------>")

# search for pattern using regular expressions (.+?)
#if(htmltext.find(adate)!=-1):
wind='<windDirection deg="(.+?)" code="(.+?)" name="(.+?)"/>'
temp='<temperature day="(.+?)" min="(.+?)" max="(.+?)" night="(.+?)" eve="(.+?)" morn="(.+?)"/>'
condition='<symbol number="(.+?)" name="(.+?)" var="(.+?)"/>'
pattern_wind=re.compile(wind)
pattern_temp=re.compile(temp)
pattern_cond=re.compile(condition)
try:
# match pattern with htmltext
    weather_winddirection=re.findall(pattern_wind,htmltext)
    weather_temp=re.findall(pattern_temp,htmltext)
    weather_cond=re.findall(pattern_cond,htmltext)
    conn = sqlite3.connect(':memory:')
    conn = sqlite3.connect("D://Programming/weather_forecast.db")
    c=conn.cursor()
    print "Overall Weather status: ",weather_cond[1][1]
    print "Temperature @Morning: ",weather_temp[1][5]
    print "Temperature @Day: ",weather_temp[1][0]
    print "Temperature @Evening: ",weather_temp[1][4]
    print "Temperature @Night: ",weather_temp[1][3]
    print ""
    print "Max Temperature: ",weather_temp[1][2]
    print "Min Temperature: ",weather_temp[1][1]

    print ""

    if(weather_winddirection[1][2]!=""):
        print "Wind Direction: ",weather_winddirection[1][2]

    # Insert a row of data
    c.execute("INSERT INTO data VALUES (?,?,?,?,?,?,?)", (city,tomorrow,weather_cond[1][1],weather_temp[1][5],weather_temp[1][0],weather_temp[1][4],weather_temp[1][3]))
    # Save (commit) the changes
    conn.commit()
    conn.close()
except Exception:
	print "Data unavailable!"
