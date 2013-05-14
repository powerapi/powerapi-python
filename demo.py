from pprint import pprint #DEBUG
import sys #DEBUG

import powerapi

ps = powerapi.core('https://psserv')

try:
	user = ps.auth('username', 'password')
except Exception as err:
	print "Whoops! Something went wrong with PowerAPI:", err
	sys.exit()

courses = user.getCourses()
pprint(courses[2].getName())
pprint(courses[2].getScores())