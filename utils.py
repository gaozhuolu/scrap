import os
import re


def wholerstrip(s, stipchar):
	if s is None or s == '':
		return ''

	while True:
		tmp = s.rstrip(stipchar)
		if tmp == s:
			return tmp
		else:
			s = tmp
	return s


def wholelstrip(s, stipchar):
	if s is None or s == '':
		return ''

	while True:
		tmp = s.lstrip(stipchar)
		if tmp == s:
			return tmp
		else:
			s = tmp
	return s

# remove annoying characters
chars = {
    '\xc2\x82' : ',',        # High code comma
    '\xc2\x84' : ',,',       # High code double comma
    '\xc2\x85' : '...',      # Tripple dot
    '\xc2\x88' : '^',        # High carat
    '\xc2\x91' : '\x27',     # Forward single quote
    '\xc2\x92' : '\x27',     # Reverse single quote
    '\xc2\x93' : '\x22',     # Forward double quote
    '\xc2\x94' : '\x22',     # Reverse double quote
    '\xc2\x95' : ' ',
    '\xc2\x96' : '-',        # High hyphen
    '\xc2\x97' : '--',       # Double hyphen
    '\xc2\x99' : ' ',
    '\xc2\xa0' : ' ',
    '\xc2\xa6' : '|',        # Split vertical bar
    '\xc2\xab' : '<<',       # Double less than
    '\xc2\xbb' : '>>',       # Double greater than
    '\xc2\xbc' : '1/4',      # one quarter
    '\xc2\xbd' : '1/2',      # one half
    '\xc2\xbe' : '3/4',      # three quarters
    '\xca\xbf' : '\x27',     # c-single quote
    '\xcc\xa8' : '',         # modifier - under curve
    '\xcc\xb1' : ''          # modifier - under line
}
def replace_chars(match):
	char = match.group(0)
	return chars[char]


def removespecialchars(text):
	return re.sub('(' + '|'.join(chars.keys()) + ')', replace_chars, text)