
import sys, getopt

import modules.Tui
import modules.FormWrapper


if __name__ == '__main__':
	print('Enter TUI mode without parameters, or use:')
	print('efc -c <rule.xlsx> -t <ACCESS | NAT> [-p (--permanent)]')
	if len(sys.argv) == 1:
		modules.Tui.main()
	else:
		isPermanent = False
		opts, args = getopt.getopt(sys.argv[1:], 'pc:t:', ['config=', 'table=', ])
		print(opts)
		for opt, arg in opts:
			if opt in ['-c', '--config']:
				config = arg
			if opt in ['-t', '--table']:
				table = arg
			if opt in ['-p', '--permanent']:
				isPermanent = True
			print((opt, arg))
		modules.FormWrapper.main(config, table, isPermanent)
