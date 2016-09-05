import sys


def analysis_name():
	''' Just function which gets argv and return analysis_name. Need sys library'''
	_analysis_name = ''
	if len(sys.argv) == 1:
		_analysis_name = 'Wlv'
		print_nice('analysis_info','Missing analysis_name argument, using default: ', _analysis_name)
	else:
		_analysis_name = sys.argv[1]

	return _analysis_name

def print_nice(print_type, *text):
 
	try:

		if print_type == 'python_info': # Bright Yellow
			print '\033[1;33;40m' + ''.join(text) + '\033[0m'

		elif print_type == 'analysis_info': # Bright Cyan
			print '\033[1;36;40m{0:30s}{1}\033[0m'.format(*text)

		elif print_type == 'analysis_info_list': # Bright Cyan
			print '\033[1;36;40m' + text[0] + '\033[0m'
			for _l in text[1]:
				print '\033[1;36;40m{0:30s}{1}\033[0m'.format('' , _l)

		elif print_type == 'error':  # Bright Red
			print '\033[1;31;40m' + ''.join(text) + '\033[0m'

		elif print_type == 'status': # Bright Green
			print '\033[1;32;40m' + ''.join(text) + '\033[0m'	


	except Exception, e:
		print text

	# ----- Example ------
	# print "\033[1;32;40m Bright Green  \033[0m \n"
	# \033[  Escape code, this is always the same
	# 1 = Style, 1 for normal.
	# 32 = Text colour, 32 for bright green.
	# 40m = Background colour, 40 is for black.

	# print("\033[0;37;40m Normal text\n")
	# print("\033[2;37;40m Underlined text\033[0;37;40m \n")
	# print("\033[1;37;40m Bright Colour\033[0;37;40m \n")
	# print("\033[3;37;40m Negative Colour\033[0;37;40m \n")
	# print("\033[5;37;40m Negative Colour\033[0;37;40m\n")
	 
	# print("\033[1;37;40m \033[2;37:40m TextColour BlackBackground          TextColour GreyBackground                WhiteText ColouredBackground\033[0;37;40m\n")
	# print("\033[1;30;40m Dark Gray      \033[0m 1;30;40m            \033[0;30;47m Black      \033[0m 0;30;47m               \033[0;37;41m Black      \033[0m 0;37;41m")
	# print("\033[1;31;40m Bright Red     \033[0m 1;31;40m            \033[0;31;47m Red        \033[0m 0;31;47m               \033[0;37;42m Black      \033[0m 0;37;42m")
	# print("\033[1;32;40m Bright Green   \033[0m 1;32;40m            \033[0;32;47m Green      \033[0m 0;32;47m               \033[0;37;43m Black      \033[0m 0;37;43m")
	# print("\033[1;33;40m Yellow         \033[0m 1;33;40m            \033[0;33;47m Brown      \033[0m 0;33;47m               \033[0;37;44m Black      \033[0m 0;37;44m")
	# print("\033[1;34;40m Bright Blue    \033[0m 1;34;40m            \033[0;34;47m Blue       \033[0m 0;34;47m               \033[0;37;45m Black      \033[0m 0;37;45m")
	# print("\033[1;35;40m Bright Magenta \033[0m 1;35;40m            \033[0;35;47m Magenta    \033[0m 0;35;47m               \033[0;37;46m Black      \033[0m 0;37;46m")
	# print("\033[1;36;40m Bright Cyan    \033[0m 1;36;40m            \033[0;36;47m Cyan       \033[0m 0;36;47m               \033[0;37;47m Black      \033[0m 0;37;47m")
	# print("\033[1;37;40m White          \033[0m 1;37;40m            \033[0;37;40m Light Grey \033[0m 0;37;40m               \033[0;37;48m Black      \033[0m 0;37;48m")
