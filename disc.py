from flask import Flask, render_template, request, redirect
import calendar, time, datetime
from datetime import date
from pymongo import Connection

conn = Connection()
db = conn['disc']
app = Flask(__name__)
@app.route("/")
def home():
    q = db.reports.find()
    reports = {}
    #db.reports.remove()
    for r in q:
        d = r['date']
        #print "date: " + str(r)
        rep = r['report']
        #print "report: " + str(rep)
        if d in reports:
            #print "d in reports: " + str(reports[d])
            reports[d].append(rep)
        else:
            #print "else"
            reports[d] = [rep]
        print str(reports)
    print datetime.datetime.today().weekday()
    year = time.strftime("%Y")
    print "year: " + year
    month = time.strftime("%m")
    return redirect("/"+month+"/"+year)

@app.route("/<m>/<y>", methods=["GET", "POST"])
def showCalendar(m, y):
    q = db.reports.find()
    reports = {}
    #db.reports.remove()
    for r in q:
        d = r['date']
        #print "date: " + str(r)
        rep = r['report']
        #print "report: " + str(rep)
        if d in reports:
            #print "d in reports: " + str(reports[d])
            reports[d].append(rep)
        else:
            #print "else"
            reports[d] = [rep]
        #print str(reports)
    print datetime.datetime.today().weekday()
    year = y
    print "year: " + year
    month = m
    print "month: " + month
    day = time.strftime("%d")
    print "day: " + day
    firstDayOfMonth = date(int(y), int(month), 1).strftime("%w")
    print "first day of month: " + firstDayOfMonth
    firstWeek=[]
    secondWeek=[]
    thirdWeek=[]
    fourthWeek=[]
    fifthWeek=[]
    sixthWeek=[]
    dayCount = 1
    numDays = numDaysInMonth(int(month), int(year))
    for day in range(7-int(firstDayOfMonth)):
        firstWeek.append("0"+str(dayCount))
        dayCount = dayCount+1
    print numDays
    for day in range(7):
        if dayCount<10:
            secondWeek.append("0"+str(dayCount))
        else:
            secondWeek.append(str(dayCount))
        dayCount = dayCount+1
    for day in range(7):
        thirdWeek.append(str(dayCount))
        dayCount = dayCount+1
    for day in range(7):
        if dayCount <= numDays:
            fourthWeek.append(str(dayCount))
            dayCount = dayCount+1
    for day in range(7):
        if dayCount <= numDays:
            fifthWeek.append(str(dayCount))
            dayCount = dayCount+1
    while dayCount <= numDays:
        sixthWeek.append(str(dayCount))
        dayCount = dayCount+1
    print "firstWeek: " + str(firstWeek)
    print "2nd: " + str(secondWeek)
    print "3rd: " + str(thirdWeek)
    print "4th: " + str(fourthWeek)
    print "5th: " + str(fifthWeek)
    print "6th: " + str(sixthWeek)
    return render_template("disc.html", reports=reports, month=month, year=year[2:], firstWeek=firstWeek, secondWeek=secondWeek, thirdWeek=thirdWeek, fourthWeek=fourthWeek, fifthWeek=fifthWeek)

def numDaysInMonth(month, year):
    if month==4 or month==6 or month==9 or month==11:
        return 30
    elif month==2:
        if year%4==0:
            return 29
        else:
            return 28
    else:
        return 31

@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method=="POST":
        rep = request.form.get("r")
        m = request.form.get("m")
        if int(m) < 10:
            m = "0" + m
        d = request.form.get("d")
        if int(d) < 10:
            d = "0" + d
        y = request.form.get("y")
        y = y[2:]
        d = time.strftime(m + "/" + d + "/" + y)
        print "d: " + str(d)
        #d = time.strftime("%x")#date
        #print "date: " + d
        db.reports.insert({'date':d,'report':rep})
        q = db.reports.find()
        print "q: " + str(q)
        for x in q:
            print "document: " + str(x)
        return redirect("/")
    year = time.strftime("%Y")
    month = time.strftime("%m")
    day = time.strftime("%d")
    return render_template("report.html", year=year, month=month, day=day)

if __name__=="__main__":
    app.debug=True
    app.run()
