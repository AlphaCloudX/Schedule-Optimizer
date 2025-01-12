from flask import Flask, render_template, request
import json
import time  # Import the time module
from CourseUtil import ScheduleItem, CourseSection, CoursePlanner
from sortingMethods import filterByEarliestAtSchool, filterByLatestAtSchool, filterByTotalMinTimeBetweenClasses

app = Flask(__name__)

import re

error_codes = ["No_Course_Entered", "Course_Not_Available", "Invalid_Times", "None", "No_Combinations"]


# Function to correct course code formatting
def correct_course_codes(course_codes):
    # Regular expression to match course codes missing the '*'
    corrected_codes = []

    for code in course_codes:
        # If the code doesn't already contain a '*', fix it
        if '*' not in code:
            # Use regex to separate the letters and numbers, and insert '*'
            corrected_code = re.sub(r'([A-Za-z]+)(\d+)', r'\1*\2', code)
            corrected_codes.append(corrected_code)
        else:
            corrected_codes.append(code)

    return corrected_codes


@app.route('/', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        error_code = "None"

        # Record the start time
        start_time = time.time()

        # Get the course codes and correct the format
        course_codes = ''.join(request.form.getlist('courses[]')[0].split()).upper().split(',')
        print("Received Course Codes")
        print(course_codes)

        course_codes = [code for code in course_codes if code]  # Remove empty strings
        course_codes = correct_course_codes(course_codes)  # Correct the course code format

        print("Filtered Course Codes")
        print(course_codes)

        # If no course codes were entered, trigger an error
        if len(course_codes) == 0:
            print("No Courses Entered")
            error_code = "No_Course_Entered"
            return render_template('error.html', error_code=error_code)

        # Get earliest and latest times
        earliest = request.form.get('earliest', None)
        latest = request.form.get('latest', None)

        print("Entered Times:")
        print(earliest, latest)

        if earliest:
            earliestAtSchool = int(earliest.split(":")[0]) * 60 + int(earliest.split(":")[1])
        else:
            earliestAtSchool = 0  # Default: 12:00 AM

        if latest:
            latestAtSchool = int(latest.split(":")[0]) * 60 + int(latest.split(":")[1])
        else:
            latestAtSchool = 0  # Default: 12:00 AM (Midnight)

        # Check if times are valid
        if earliestAtSchool > latestAtSchool:
            error_code = "Invalid_Times"
            print("User entered invalid times")
            return render_template('error.html', error_code=error_code)

        # Load the correct file based on the selected semester
        semester = request.form.get('semester')
        if semester == "Fall 2024":
            json_file = 'outputF24.json'
            print("Reading Fall Courses")

        elif semester == "Winter 2025":
            json_file = 'outputW25NoProfNoRooms.json'
            print("Reading Winter Courses")
        else:
            error_code = "Invalid_Semester"
            return render_template('error.html', error_code=error_code)

        try:
            with open(json_file, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            error_code = "File_Not_Found"
            return render_template('error.html', error_code=error_code)

        # Rest of your code to process the course schedule
        allCourseData = []

        # Initialize a list to store invalid course codes
        invalid_courses = []

        # Check if courses are available in the data
        for course_code in course_codes:
            if course_code in data:
                course_info = data[course_code]
                allCourseData.append([])
                cData = course_info.get("Sections", [])

                for sec in cData:
                    try:
                        lectureTime = ScheduleItem("Lecture", sec["LEC"]["start"], sec["LEC"]["end"],
                                                   sec["LEC"]["date"])
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

                    newSection = CourseSection(sec["id"], lectureTime, semTime, labTime)
                    allCourseData[-1].append(newSection)
            else:
                invalid_courses.append(course_code)

        # If there are invalid courses, trigger an error
        if invalid_courses:
            print("Invalid Course Codes")
            print(invalid_courses)
            error_code = "Course_Not_Available"
            return render_template('error.html', error_code=error_code, invalid_courses=invalid_courses)

        comb = CoursePlanner(allCourseData)
        validCombination = comb.nonOverlapped()



        if len(validCombination) == 0:
            print("Could not find any valid combinations")
            error_code = "No_Combinations"
            return render_template('error.html', error_code=error_code)

        validCombination = filterByEarliestAtSchool(validCombination, earliestAtSchool)
        validCombination = filterByLatestAtSchool(validCombination, latestAtSchool)

        validCombination, sortedTimeIndices1, times1 = filterByTotalMinTimeBetweenClasses(validCombination)

        print("Post Processed Valid Combinations:")
        print(len(validCombination))

        combinations = []
        for i in sortedTimeIndices1:
            combination = {
                "total_time": times1[i],
                "courses": validCombination[i]
            }
            combinations.append(combination)

        # Record the end time
        end_time = time.time()
        elapsed_time = end_time - start_time

        return render_template('result.html', combinations=combinations, earliestAtSchool=earliestAtSchool,
                               latestAtSchool=latestAtSchool, elapsed_time=elapsed_time,
                               total_possible=len(comb.combinations))

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)













#
# from flask import Flask, render_template
#
# import M68k_Tutorial.routes
# from CoursePlaner.routes import course_planer_bp
# from M68k_Tutorial.routes import m68k_bp
#
# app = Flask(__name__)
#
# # Register the blueprint
# app.register_blueprint(course_planer_bp)
#
# # Register the blueprint
# app.register_blueprint(M68k_Tutorial.routes.m68k_bp)
#
# @app.route('/')
# def landing_page():
#     return render_template('landing_page.html')
#
# if __name__ == '__main__':
#     app.run(debug=False)

#
#
#
#
#
#
#
# from flask import Flask, render_template, Blueprint, request
# import json
# import time
# import re
# from CourseUtil import ScheduleItem, CourseSection, CoursePlanner
# from sortingMethods import filterByEarliestAtSchool, filterByLatestAtSchool, filterByTotalMinTimeBetweenClasses
#
#
# # Course Planner Blueprint
# course_planer_bp = Blueprint('course_planer', __name__, template_folder='templates', static_folder='static')
#
# error_codes = ["No_Course_Entered", "Course_Not_Available", "Invalid_Times", "None", "No_Combinations"]
#
# def correct_course_codes(course_codes):
#     corrected_codes = []
#     for code in course_codes:
#         if '*' not in code:
#             corrected_code = re.sub(r'([A-Za-z]+)(\d+)', r'\1*\2', code)
#             corrected_codes.append(corrected_code)
#         else:
#             corrected_codes.append(code)
#     return corrected_codes
#
# @course_planer_bp.route('/course-planner', methods=['GET', 'POST'])
# def schedule():
#     if request.method == 'POST':
#         error_code = "None"
#         start_time = time.time()
#
#         # Get the course codes and correct the format
#         course_codes = ''.join(request.form.getlist('courses[]')[0].split()).upper().split(',')
#         print("Received Course Codes:", course_codes)
#
#         course_codes = [code for code in course_codes if code]
#         course_codes = correct_course_codes(course_codes)
#
#         if not course_codes:
#             error_code = "No_Course_Entered"
#             return render_template('error.html', error_code=error_code)
#
#         earliest = request.form.get('earliest', None)
#         latest = request.form.get('latest', None)
#         if earliest:
#             earliestAtSchool = int(earliest.split(":")[0]) * 60 + int(earliest.split(":")[1])
#         else:
#             earliestAtSchool = 0
#
#         if latest:
#             latestAtSchool = int(latest.split(":")[0]) * 60 + int(latest.split(":")[1])
#         else:
#             latestAtSchool = 0
#
#         if earliestAtSchool > latestAtSchool:
#             error_code = "Invalid_Times"
#             return render_template('error.html', error_code=error_code)
#
#         semester = request.form.get('semester')
#         if semester == "Fall 2024":
#             json_file = 'CoursePlaner/outputF24.json'
#         elif semester == "Winter 2025":
#             json_file = 'CoursePlaner/outputW25NoProfNoRooms.json'
#         else:
#             error_code = "Invalid_Semester"
#             return render_template('error.html', error_code=error_code)
#
#         try:
#             with open(json_file, 'r') as file:
#                 data = json.load(file)
#         except FileNotFoundError:
#             error_code = "File_Not_Found"
#             return render_template('error.html', error_code=error_code)
#
#         allCourseData = []
#         invalid_courses = []
#         for course_code in course_codes:
#             if course_code in data:
#                 course_info = data[course_code]
#                 allCourseData.append([])
#                 cData = course_info.get("Sections", [])
#                 for sec in cData:
#                     try:
#                         lectureTime = ScheduleItem("Lecture", sec["LEC"]["start"], sec["LEC"]["end"],
#                                                    sec["LEC"]["date"])
#                     except KeyError:
#                         lectureTime = None
#                     try:
#                         semTime = ScheduleItem("Seminar", sec["SEM"]["start"], sec["SEM"]["end"], sec["SEM"]["date"])
#                     except KeyError:
#                         semTime = None
#                     try:
#                         labTime = ScheduleItem("Lab", sec["LAB"]["start"], sec["LAB"]["end"], sec["LAB"]["date"])
#                     except KeyError:
#                         labTime = None
#
#                     newSection = CourseSection(sec["id"], lectureTime, semTime, labTime)
#                     allCourseData[-1].append(newSection)
#             else:
#                 invalid_courses.append(course_code)
#
#         if invalid_courses:
#             error_code = "Course_Not_Available"
#             return render_template('error.html', error_code=error_code, invalid_courses=invalid_courses)
#
#         comb = CoursePlanner(allCourseData)
#         validCombination = comb.nonOverlapped()
#
#         if not validCombination:
#             error_code = "No_Combinations"
#             return render_template('error.html', error_code=error_code)
#
#         validCombination = filterByEarliestAtSchool(validCombination, earliestAtSchool)
#         validCombination = filterByLatestAtSchool(validCombination, latestAtSchool)
#         validCombination, sortedTimeIndices1, times1 = filterByTotalMinTimeBetweenClasses(validCombination)
#
#         combinations = []
#         for i in sortedTimeIndices1:
#             combination = {"total_time": times1[i], "courses": validCombination[i]}
#             combinations.append(combination)
#
#         end_time = time.time()
#         elapsed_time = end_time - start_time
#
#         return render_template(
#             'result.html',
#             combinations=combinations,
#             earliestAtSchool=earliestAtSchool,
#             latestAtSchool=latestAtSchool,
#             elapsed_time=elapsed_time,
#             total_possible=len(comb.combinations),
#         )
#
#     return render_template('index.html')
#
#
# # Main Flask App
# app = Flask(__name__)
#
# app.register_blueprint(course_planer_bp)
#
# @app.route('/')
# def landing_page():
#     return render_template('index.html')
#
# if __name__ == '__main__':
#     app.run(debug=True)





