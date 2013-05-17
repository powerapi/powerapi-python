import re
from .course import course

class user:
	def __init__(self, core, homeContents):
		self.core = core
		self.homeContents = homeContents
		
		self.courses = self._createCourses()
	
	def _createCourses(self):
		courses = []
		
		for item in re.finditer('<tr class="center" bgcolor="(.*?)">(.*?)<\/tr>', self.homeContents, re.S):
			if re.search(r'<td align="left">(.*?)(&nbsp;|&bbsp;)<br>(.*?)<a href="mailto:(.*?)">(.*?)<\/a><\/td>', item.groups()[1], re.S):
				courses.append(course(self.core, item.groups()[1]))
		
		return courses
	
	def getSchoolName(self):
		name = re.search(r'<div id="print-school">(.*?)<br>', self.homeContents, re.S)
		
		return name.groups()[0].strip().encode('ascii')
	
	def getUserName(self):
		name = re.search(r'<li id="userName" .*?<span>(.*?)<\/span>', self.homeContents, re.S)
		
		return name.groups()[0].strip().encode('ascii')
	
	def getCourses(self):
		return self.courses