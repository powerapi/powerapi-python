import requests, re
import hmac, hashlib, base64 # PCAS is horrible

from .user import user

class core:
	ua = 'powerapi-python/1.0 (https://github.com/henriwatson/powerapi-python)'
	
	def __init__(self, url):
		if url[-1] != '/':
			self.url = url + '/'
		else:
			self.url = url
		
		self.session = requests.Session()
	
	def setUserAgent(self, ua):
		self.ua = ua
		
	def _getAuthData(self):
		r = self.session.get(self.url)
		
		if r.status_code != requests.codes.ok:
			raise Exception('Unable to retrieve authentication tokens from PS server.')
		
		data = {}
		
		pstoken = re.search(r'<input type="hidden" name="pstoken" value="(.*?)" \/>', r.text, re.S)
		data['pstoken'] = pstoken.groups()[0]
		
		contextData = re.search(r'<input type="hidden" name="contextData" value="(.*?)" \/>', r.text, re.S)
		data['contextData'] = contextData.groups()[0]
		
		if "<input type=hidden name=ldappassword value=''>" in r.text:
			data['ldap'] = True
		else:
			data['ldap'] = False
			
		return data
		
	def auth(self, uid, pw):
		authdata = self._getAuthData()
		
		fields = {
					'pstoken': authdata['pstoken'],
					'contextData': authdata['contextData'],
					'dbpw': hmac.new(authdata['contextData'].encode('ascii'), pw.lower().encode('ascii'), hashlib.md5).hexdigest(),
					'serviceName': 'PS Parent Portal',
					'pcasServerUrl': '/',
					'credentialType': 'User Id and Password Credential',
					'account': uid,
					'pw': hmac.new(authdata['contextData'].encode('ascii'), base64.b64encode(hashlib.md5(pw.encode('ascii')).digest()).replace(b"=", b""), hashlib.md5).hexdigest()
				}
		
		if authdata['ldap'] == True:
			fields['ldappassword'] = pw
		
		r = self.session.post(self.url + "guardian/home.html", data=fields)
		
		if not u'Grades and Attendance' in r.text:
			pserror = re.search(r'<div class="feedback-alert">(.*?)<\/div>', r.text, re.S)
			
			if pserror:
				raise Exception(pserror.groups()[0])
			else:
				raise Exception('Unable to login to PS server.')
		else:
			return user(self, r.text)