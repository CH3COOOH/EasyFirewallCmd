import os

class Menu:
	def __init__(self, dic_menu):
		self.menu = dic_menu
		self.head = ''
		self.prompt = '> '
	
	def setHead(self, s_head):
		self.head = s_head
	
	def setPrompt(self, s_prompt):
		self.prompt = s_prompt

	def print(self):
		print(self.head)
		for k in self.menu.keys():
			print(' %s: %s' % (k, self.menu[k]))
		print('----------')

	def getInput(self):
		ch = None
		while True:
			ch = input(self.prompt)
			if ch in self.menu.keys():
				return ch
			elif ch == '':
				continue
			else:
				print('Invalid input.')
	
	def getMenuDict(self):
		return self.menu


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


if __name__ == '__main__':
	
	fc = FirewallCmd()
	dic_mainMenu = {
			'0': 'Show firewall status',
			'1': 'Show all available zones',
			'2': 'Show details of all zones',
			'3': 'Change the zone of an interface...',
			'4': 'Edit policy of a specific zone...',
			'q': 'Exit'
			}
	mainMenu = Menu(dic_mainMenu)
	mainMenu.setHead('=== Easy Firewall Cmd ===')

	ch = None
	while True:
		mainMenu.print()
		ch = mainMenu.getInput()
		if ch == 'q':
			break

		if ch == '0':
			fc.getFwStatus()
		
		if ch == '1':
			fc.getZones()

		if ch == '2':
			fc.getZonesDetail()
		
		if ch == '3':
			inf = input('Interface: ')
			zo = input('Change to zone: ')
			fc.changeZoneOfInterface(inf, zo)
		
		if ch == '4':
			fc.getZones()
			zo = input('Which zone: ')
			
			while True:
				subMenuZone = Menu({
					'0': 'Show zone status',
					'1': 'Open a port...',
					'2': 'Close a port...',
					'3': 'Set default action...',
					'4': 'Add an interface into the zone...',
					'5': 'Enable a service...',
					'6': 'Disable a service...',
					'b': 'Back to homepage',
					'q': 'Exit'
					})
				subMenuZone.setPrompt('zone:%s > ' % zo)
				subMenuZone.print()
				ch = subMenuZone.getInput()
				
				if ch == 'b':
					break
				if ch == 'q':
					exit()
				
				if ch == '0':
					fc.getZoneStatus(zo)

				if ch == '1':
					fc.portOpen(zo, input('Port to open (ex. 80/tcp, 500/udp, ...):\n'))
				
				if ch == '2':
					fc.portClose(zo, input('Port to close (ex. 80/tcp, 500/udp, ...):\n'))
					
				if ch == '3':
					subMenuAction = Menu({
						'1': 'default',
						'2': 'ACCEPT',
						'3': 'REJECT',
						'4': 'DROP'
						})
					subMenuAction.setHead('Select the action:')
					subMenuAction.setPrompt('zone:%s:action > ' % zo)
					subMenuAction.print()
					ch = subMenuAction.getInput()
					fc.setDefaultAction(zo, subMenuAction.getMenuDict()[ch])
				
				if ch == '4':
					fc.changeZoneOfInterface(input('Which interface: '), zo)
				
				if ch == '5':
					fc.serviceEnable(zo, input('Enable service: '))
				
				if ch == '6':
					fc.serviceDisable(zo, input('Disable service: '))

