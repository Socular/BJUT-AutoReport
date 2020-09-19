from reportClass import *

users = [ 
	[
		"username", #用户名
		"passwd" #密码
	]
]

for usr in users:
	usr = Report(usr[0], usr[1])
	if not usr.login():
		continue
	if not usr.dCon():
		continue
	if usr.chkSign():
		continue
	usr.send()