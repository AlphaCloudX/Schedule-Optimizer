import itertools
import json

from CourseUtil import ScheduleItem, CourseSection, CoursePlanner
from sortingMethods import *

# Input and data loading logic
# Use the list instead of retyping everything
usePredefinedList = True
course_codes = ["MATH*1210", "STAT*2050", "CIS*3110", "CIS*2750", "CIS*3490"]

# How to calculate First Class Of Day?
# HH : MM
# (HH * 60) + MM
# For Example:
# HH = 10 | which is 10am
# MM = 30 | 30min after 10am
# We Do (10 * 60) + 30
# HH = 13 | 1pm
# HH = 0 | just 1pm
# We Do (13 * 60) + 0
# LEAVE TO 0 FOR NOW IF YOU DO NOT WANT TO USE THIS PARAMETER
earliestAtSchool = (10 * 60) + 0

# Calculate Last Class Of Day
latestAtSchool = (21 * 60) + 00

# remove this for now since it's probably easier to hardcode the values
# earliestAtSchool = (10 * 60) + 30  # 10:30
# earliestAtSchool = 1
#
# if not usePredefinedList:
#     while True:
#         course_code = input("Enter course code (or type 'done' to finish): ").upper().strip()
#         if course_code.lower() == 'done':
#             break
#         course_codes.append(course_code)
#
# earliestAtSchool *= int(input("Enter The Earliest Hour You Want To Be At School 24hr format:")) * 60
# earliestAtSchool += int(input("Enter The Earliest Minute You Want To Be At School 24hr format:"))

# Load the JSON file into a Python dictionary
with open('outputW25NoProfNoRooms.json', 'r') as file:
    data = json.load(file)

allCourseData = []

# Loop through each course code the user entered
for course_code in course_codes:

    # Loop through every course code
    if course_code in data:
        # Find the information for the specified course code
        course_info = data[course_code]

        # Initialize the list for this course's sections
        allCourseData.append([])

        cData = course_info.get("Sections", [])

        for sec in cData:
            try:
                lectureTime = ScheduleItem("Lecture", sec["LEC"]["start"], sec["LEC"]["end"], sec["LEC"]["date"])
            except KeyError:
                lectureTime = None

            try:
                semTime = ScheduleItem("Seminar", sec["SEM"]["start"], sec["SEM"]["end"], sec["SEM"]["date"])
            except KeyError:
                semTime = None

            try:
                labTime = ScheduleItem("Lab", sec["LAB"]["start"], sec["LAB"]["end"], sec["LAB"]["date"])
            except KeyError:
                labTime = None

            # Create a new CourseSection with the ScheduleItems
            newSection = CourseSection(sec["id"], lectureTime, semTime, labTime)

            allCourseData[-1].append(newSection)
    else:
        print(f"Course code {course_code} not found.")

# Pass the course data into the CoursePlanner and print schedules
validCombination = CoursePlanner(allCourseData).nonOverlapped()

# print(f"There are {len(validCombination)} valid combinations. Would You Like To View This Combination?")
# CoursePlanner(allCourseData, earliestAtSchool).print_all_schedules()
validCombination = filterByEarliestAtSchool(validCombination, earliestAtSchool)
validCombination = filterByLatestAtSchool(validCombination, latestAtSchool)
validCombination, sortedTimeIndices, times = filterByTotalMinTimeBetweenClasses(validCombination)

print("Combinations After Including Filters:")

# Print Sorted From Low To High:
for i in sortedTimeIndices:
    print(f"Combination: {i} | Total Time Between Classes = {times[i]} | Courses:")
    for c in validCombination[i]:
        print(c.courseCode)

    print("\n\n")



# Uncomment this code to draw the schedules out:




# Regular print
# for i in validCombination:
#     for c in i:
#         print(c.courseCode)
#
#     print("\n\n")
