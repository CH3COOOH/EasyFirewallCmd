import os

class FirewallCmd:

	def __init__(self, exec=True):
		self.exec = exec
	
	def printCmd(self, cmd):
		print('Execute **********\n' + cmd + '\n******************') 
	
	def getDirectRules(self):
		os.system('firewall-cmd --direct --get-all-rules')
		return 0
	
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
		cmd = f'''firewall-cmd --zone={zone} --change-interface={inf} --permanent'''
# firewall-cmd --reload
# systemctl restart firewalld.service''' % (zone, inf)
		self.printCmd(cmd)
		if self.exec == True:
			os.system(cmd)
		return 0

	def removeInterfaceFromZone(self, inf, zone):
		cmd = f'''firewall-cmd --zone={zone} --remove-interface={inf} --permanent'''
# firewall-cmd --reload
# systemctl restart firewalld.service''' % (zone, inf)
		self.printCmd(cmd)
		if self.exec == True:
			os.system(cmd)
		return 0
	
	def portOpen(self, zone, s_port):
		cmd = f'''firewall-cmd --zone={zone} --add-port={s_port} --permanent'''
# firewall-cmd --reload''' % (zone, s_port)
		self.printCmd(cmd)
		if self.exec == True:
			os.system(cmd)
		return 0
	
	def portClose(self, zone, s_port):
		cmd = f'''firewall-cmd --zone={zone} --remove-port={s_port} --permanent'''
# firewall-cmd --reload''' % (zone, s_port)
		self.printCmd(cmd)
		if self.exec == True:
			os.system(cmd)
		return 0
	
	def setDefaultAction(self, zone, action):
		## firewall-cmd --zone=%s --set-target=<default|ACCEPT|REJECT|DROP>
		cmd = f'''firewall-cmd --zone={zone} --set-target={action} --permanent'''
# firewall-cmd --reload''' % (zone, action)
		self.printCmd(cmd)
		if self.exec == True:
			os.system(cmd)
		return 0
	
	def serviceEnable(self, zone, service):
		cmd = f'''firewall-cmd --zone={zone} --add-service={service} --permanent'''
# firewall-cmd --reload
# ''' % (zone, service)
		self.printCmd(cmd)
		if self.exec == True:
			os.system(cmd)
		return 0
	
	def serviceDisable(self, zone, service):
		cmd = f'''firewall-cmd --zone={zone} --remove-service={service} --permanent'''
# firewall-cmd --reload''' % (zone, service)
		self.printCmd(cmd)
		if self.exec == True:
			os.system(cmd)
		return 0

	def direct_redirect(self, pr, si, sp, di, dp, isAdd=True):
		## protocol, src_ip, src_port, des_ip, des_port
		rule_cmd = {True: 'add', False: 'remove'}
		cmd = f'''firewall-cmd --permanent --direct --{rule_cmd[isAdd]}-rule ipv4 nat PREROUTING 0 -p {pr} -d {si} --dport {sp} -j DNAT --to-destination {di}:{dp}
firewall-cmd --permanent --direct --{rule_cmd[isAdd]}-rule ipv4 nat POSTROUTING 0 -p {pr} -d {di} --dport {dp} -j MASQUERADE'''
# firewall-cmd --reload'''
		self.printCmd(cmd)
		if self.exec == True:
			os.system(cmd)
		return 0
