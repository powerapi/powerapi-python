import re

class course:
	def __init__(self, core, html):
		self.core = core
		self.html = html
		
		self._populateCourse()
	
	def _populateCourse(self):
		courseData = re.search('<td align="left">(.*?)(&nbsp;|&bbsp;)<br>(.*?)<a href="mailto:(.*?)">(.*?)<\/a><\/td>', self.html, re.S)
		
		self.name = courseData.groups()[0]
		self.teacher = {
			'name': courseData.groups()[4],
			'email': courseData.groups()[3]
		}
		
		self.scores = {}
		
		for score in re.finditer('<a href="scores.html\?(.*?)">(.*?)<\/a>', self.html, re.S):
			URLbits = re.search(r'frn\=(.*?)\&fg\=(.*)', score.groups()[0], re.S)
			
			scoreT = score.groups()[1].split("<br>")
			
			if score.groups()[1] == "--":
				break
			elif not scoreT[0].isdigit():
				self.scores[URLbits.groups()[1]] = scoreT[1]
			else:
				self.scores[URLbits.groups()[1]] = scoreT[0]
		
	def getName(self):
		return self.name
	
	def getScores(self):
		return self.scores