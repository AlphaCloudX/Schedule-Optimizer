
# University Of Guelph Course Selection Optimizer

A python script to optimize your course layout to have minimal times between classes.

Made by Michael, Contributions by Robert


## Features

- Ability To Enter How Many Courses
- Sort from minimum to maximum time between classes
- Ability to add earliest and latest class
- Supports DE Classes
- Ability to export to calendar
- Completely Free!

## Dependencies

- icalendar-6.1.0

## How to run

Install dependencies:

```bash
pip install icalendar
```

To run this project modify the
```python
course_codes = ["MATH*1210", "STAT*2050", "CIS*3110", "CIS*2750", "CIS*3490"]
```
variable to contain the courses you want to pick.

Then modify the:
```python
earliestAtSchool = (10 * 60) + 0
```
variable for the appropriate start time if you would like. Otherwise leave it to 0.

The time must be in 24 hours, we do `(Hour * 60) + minutes` so that the time is measured in amount of minutes.

The end time:
```python
latestAtSchool = (10 * 60) + 0
```
Follows the same pattern. Keep in mind the classes often end at HH:20, HH:50 etc.

Lastly make sure the `outputW25NoProfNoRooms.json` is in the root directory with all the python scripts. This contains all the section data but the professor and room info is removed for privacy.

Once these variables are all set either through your IDE or text editor of choice you can run the python script in your terminal window.

This is designed for python 3 so any version works.

To run the python script simply do:
```bash
cd <directory/of/the/folder>
py coursePlanner.py
```
sometimes py might not work so you can experiment with trying:
python, python3, etc.

It will then output a list of course codes in terminal.

You will then be able to export a combination of course codes of your choice into an `.ics` file,
which can be imported into a calendar program of your choice.

## Roadmap

- Ability to generate the schedule into images for easy comparison

- Add custom time blocks for clubs, or lunch breaks

- Ability to find empty study spots based on available rooms

## Feedback

If you have any feedback, please feel free to reachout through github issues.

I can also be reached through discord @alphacloudx
Dm's are open if we share a mutual server.

Enjoy!

