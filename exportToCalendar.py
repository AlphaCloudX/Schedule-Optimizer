from icalendar import Calendar, Event
from datetime import datetime
import zoneinfo

def exportToCal(courses, allCourseData):
    newCal = Calendar()
    for c in courses:
        for i in allCourseData:
            for j in i:
                if j.courseCode == c.courseCode:
                    addSectionItems(j, newCal)
    #to_ical() returns bytes, so writing in binary is necessary 
    newIcs = open("coursePlanner.ics", 'wb')
    newIcs.write(newCal.to_ical())
    print("Calendar exported.")
    newIcs.close()

def addSectionItems(item, cal):
    if item.lecture != None:
        newEvent = addScheduleItem(item.courseCode, item.lecture, cal)
    if item.seminar != None:
        newEvent = addScheduleItem(item.courseCode, item.seminar, cal)
    if item.lab != None:
        newEvent = addScheduleItem(item.courseCode, item.lab, cal)
    
def addScheduleItem(courseCode, item, cal):
    for i in item.days:            
        newEvent = Event()
        newEvent.add('summary', courseCode + ' ' + item.item_type)
        #start of the event
        newEvent.add('dtstart', getCourseDateTime(item, item.start, i))
        #end of the event
        newEvent.add('dtend', getCourseDateTime(item, item.finish, i))
        cal.add_component(newEvent)

def getCourseDateTime(item, time, day):
    year = 2025
    month = 1
    hour = int(time / 60)
    minutes = time - hour * 60
    return datetime(year, month, getFirstDay(day), hour, minutes, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York"))

#the day a course starts
def getFirstDay(day):
    week = ['M','T','W','Th','F']
    #dates of weekdays in the first week
    dates = [6,7,8,9,10]
    i = week.index(day)
    if(i != -1):
        return dates[i]
    else:
        print("getFirstDay(): invaild weekday")
        return 0
