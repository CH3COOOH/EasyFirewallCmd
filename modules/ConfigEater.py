from openpyxl import load_workbook

MAP_COL = 'abcdefghijklmnopqrstuvwxyz'

class ExcelReader:
	def __init__(self, fname):
		self.fname = fname
		self.wb = load_workbook(filename=fname, read_only=True)

	def parse(self, sheetname, start_line, end_col, start_col=1):
		sh = self.wb[sheetname]
		rule_list = []
		ctr = start_line
		while True:
			if sh[MAP_COL[start_col-1]+str(ctr)].value == None:
				print('Scan finished.')
				break
			buff = []
			for i in range(start_col-1, end_col):
				buff.append(str(sh[MAP_COL[i]+str(ctr)].value))
			rule_list.append(buff)
			ctr += 1

		return rule_list

	def close(self):
		self.wb.close()
