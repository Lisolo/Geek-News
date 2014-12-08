import re

def analysis(title=''):
	word_string = re.sub('^\d+\s|\s\d+\s|\s\d+$', ' ', title)
	word = re.findall(r'(\w+)', word_string)
	return word

if __name__ == '__main__':
	analysis()