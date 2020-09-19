import requests
import json
from postdata import *
import random

url = "https://itsapp.bjut.edu.cn"
loginurl = url + "/uc/wap/login/check"
reporturl = url + "/ncov/wap/default/index"
posturl = url+"/ncov/wap/default/save"

def temporature():
	a_list = [True, False]
	distribution = [.98, .02]
	random_number = random.choices(a_list, distribution)
	return random_number[0]

class Report():

	def __init__(self, ID, PWD):
		self.ID = ID
		self.PWD = PWD

	def login(self):
		session = requests.session()
		lgnForm = {"username": self.ID, "password": self.PWD}

		#登录
		try:
			resp = session.post(loginurl, lgnForm)
		except:
			print("[ERROR] Network Error")
			return False

		#登录验证
		try:
			resp = json.loads(resp.content.decode("utf8"))
			if resp['m'] == '操作成功':
				print("Logged in as " + self.ID)
			else:
				print("[ERROR] Login failed, " + resp['m'])
				return False
		except:
			print("[ERROR] Json error.\n" + resp.content.decode("utf8"))
			return False		
		self.session = session
		return True

	def chkSign(self):
		#判断Flag
		flag = self.html.split("var vm = new Vue(")[1].split("hasFlag: \'")[1].split("\'")[0]
		if flag == '1':
			print("Already reported!")
			return True
		return False

	def dCon(self):
		#获取网页
		try:
			html = self.session.get(reporturl).content.decode("utf8")
		except:
			print("[ERROR] Network Error")
			return False
		self.html = html
		#用户数据
		jsondata = self.html.split("<script src=\"https://itsapp.bjut.edu.cn/wap/ncov/js/city.js\"></script>")[1].split("<script type=\"text/javascript\">\n")[1].split(";\n")[0].split("var def = ")[1]
		try:
			jsondata = json.loads(jsondata)
		except:
			print("[ERROR] Json error.\n" + jsondata)
			return False
		postdata['date'] = jsondata['date']
		postdata['uid'] = jsondata['uid']
		postdata['created'] = jsondata['created']
		postdata['id'] = jsondata['id']

		#GPS
		gpsdata = json.loads(postdata['geo_api_info'])
		gpsdata['position']['Q'] = round(random.uniform(39.930, 39.931), 14)
		gpsdata['position']['R'] = round(random.uniform(116.669, 116.670), 14)
		gpsdata['position']['lng'] = round(gpsdata['position']['R'], 6)
		gpsdata['position']['lat'] = round(gpsdata['position']['Q'], 6)
		postdata['geo_api_info'] = json.dumps(gpsdata)

		#体温
		if temporature():
			postdata['tw'] = "2"
		else:
			postdata['tw'] = "3"

		self.postdata = postdata
		return True

	def send(self):
		#发送数据
		try:
			resp = self.session.post(posturl, self.postdata).content.decode("utf8")
		except:
			print("[ERROR] Report Failed")
			return False

		#检查打卡
		try:
			strSuccess = json.loads(resp)
		except:
			print("[ERROR] Json error.\n" + resp)
			return False

		if strSuccess['m'] == '操作成功':
			print("Report Successful!")
			return True
		else:
			print("[ERROR] Report failed, server returns: "+strSuccess['m'])
			return False

