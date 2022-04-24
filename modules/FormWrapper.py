import os

class Wrapper:
	def __init__(self, permanent=False):
		self.cmd_base = 'firewall-cmd%s --direct' % ({True: ' --permanent', False: ''}[permanent])

	def parse_access(self, row_array):
		cmd_complete = self.cmd_base

		cmd_complete += {'A':' --add-rule', '-D': ' --remove-rule'}[row_array[0]]
		cmd_complete += ' ' + row_array[1]
		cmd_complete += (' filter ' + row_array[2])
		cmd_complete += ' ' + row_array[3]
		if row_array[10] != '*':
			cmd_complete += ' -p ' + row_array[10]
		if row_array[4] != '*':
			cmd_complete += ' -i ' + row_array[4]
		if row_array[5] != '*':
			cmd_complete += ' -s ' + row_array[5]
		if row_array[6] != '*':
			cmd_complete += ' --sport ' + row_array[6]
		if row_array[7] != '*':
			cmd_complete += ' -o ' + row_array[7]
		if row_array[8] != '*':
			cmd_complete += ' -d ' + row_array[8]
		if row_array[9] != '*':
			cmd_complete += ' --dport ' + row_array[9]
		cmd_complete += ' -j ' + row_array[11]

		return cmd_complete

	# def parse_nat(self, row_array):
	# 	# firewall-cmd --permanent --direct --add-rule ipv4 nat POSTROUTING 0 -s 192.168.10.0/24 -o eth0 -j MASQUERADE

def main(config_fname, table, isPermanent):
	from modules.ConfigEater import ExcelReader
	er = ExcelReader(config_fname)
	wp = Wrapper(isPermanent)
	rule_list = er.parse(table, 4, {'ACCESS': 12}[table])
	for rule in rule_list:
		if table == 'ACCESS':
			cmd = wp.parse_access(rule)
			print(cmd)
			os.system(cmd)


if __name__ == '__main__':
	w = Wrapper()
	with open('./access.conf', 'r') as o:
		while True:
			buff = o.readline()
			if buff == '':
				break
			print(w.parse_access(buff.split()))
