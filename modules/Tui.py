from modules.FirewallCmd import FirewallCmd

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


def main():
	fc = FirewallCmd()
	dic_mainMenu = {
			'0': 'Show firewall status',
			'1': 'Show all available zones',
			'2': 'Show details of all zones',
			'3': 'Change the zone of an interface...',
			'4': 'Edit policy of a specific zone...',
			'5': 'Show direct rules',
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
		
		if ch == '5':
			print('Direct rules:')
			fc.getDirectRules()
			print('\n')

if __name__ == '__main__':
	main()
