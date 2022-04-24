import os

class FirewallCmd:

	def __init__(self, exec=True):
		self.exec = exec
	
	def printCmd(self, cmd):
		print('Execute **********\n' + cmd + '\n******************') 
	
	def getFwStatus(self):
		os.system('firewall-cmd --state')
		print('* If firewalld seems unavailable, run \"systemctl start firewalld\" first.')
		return 0
	
	def getZones(self):
		os.system('firewall-cmd --get-zones')
		return 0

	def getZonesDetail(self):
		os.system('firewall-cmd --list-all-zones')
		return 0
	
	def getZoneStatus(self, zone):
		print('[Opened ports]')
		os.system('firewall-cmd --zone=%s --list-ports' % zone)
		print('[Enabled services]')
		os.system('firewall-cmd --zone=%s --list-services' % zone)
		print('[Interfaces]')
		os.system('firewall-cmd --zone=%s --list-interfaces' % zone)
	
	def changeZoneOfInterface(self, inf, zone):
		cmd = '''firewall-cmd --zone=%s --change-interface=%s --permanent
firewall-cmd --reload
systemctl restart firewalld.service''' % (zone, inf)
		self.printCmd(cmd)
		if self.exec == True:
			os.system(cmd)
		return 0
	
	def portOpen(self, zone, s_port):
		cmd = '''firewall-cmd --zone=%s --add-port=%s --permanent
firewall-cmd --reload''' % (zone, s_port)
		self.printCmd(cmd)
		if self.exec == True:
			os.system(cmd)
		return 0
	
	def portClose(self, zone, s_port):
		cmd = '''firewall-cmd --zone=%s --remove-port=%s --permanent
firewall-cmd --reload''' % (zone, s_port)
		self.printCmd(cmd)
		if self.exec == True:
			os.system(cmd)
		return 0
	
	def setDefaultAction(self, zone, action):
		## firewall-cmd --zone=%s --set-target=<default|ACCEPT|REJECT|DROP>
		cmd = '''firewall-cmd --zone=%s --set-target=%s --permanent
firewall-cmd --reload''' % (zone, action)
		self.printCmd(cmd)
		if self.exec == True:
			os.system(cmd)
		return 0
	
	def serviceEnable(self, zone, service):
		cmd = '''firewall-cmd --zone=%s --add-service=%s --permanent
firewall-cmd --reload
''' % (zone, service)
		self.printCmd(cmd)
		if self.exec == True:
			os.system(cmd)
		return 0
	
	def serviceDisable(self, zone, service):
		cmd = '''firewall-cmd --zone=%s --remove-service=%s --permanent
firewall-cmd --reload''' % (zone, service)
		self.printCmd(cmd)
		if self.exec == True:
			os.system(cmd)
		return 0