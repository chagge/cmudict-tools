#!/usr/bin/python
#
# Tool for processing the CMU Pronunciation Dictionary file formats.
#
# Copyright (C) 2015 Reece H. Dunn
#
# This file is part of cmudict-tools.
#
# cmudict-tools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# cmudict-tools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with cmudict-tools.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

import os
import sys
import re

class ArpabetPhonemeSet:
	def __init__(self):
		self.re_phonemes = re.compile(r' (?=[A-Z][A-Z]?[0-9]?)')

	def __call__(self, phonemes):
		return self.re_phonemes.split(phonemes.strip())

VOWEL = 1
CONSONANT = 2

phoneme_table = [
	{'arpabet': 'AA', 'type': VOWEL,     'accent': ['cmudict']},
	{'arpabet': 'AE', 'type': VOWEL,     'accent': ['cmudict']},
	{'arpabet': 'AH', 'type': VOWEL,     'accent': ['cmudict']},
	{'arpabet': 'AO', 'type': VOWEL,     'accent': ['cmudict']},
	{'arpabet': 'AW', 'type': VOWEL,     'accent': ['cmudict']},
	{'arpabet': 'AY', 'type': VOWEL,     'accent': ['cmudict']},
	{'arpabet': 'B',  'type': CONSONANT, 'accent': ['cmudict']},
	{'arpabet': 'CH', 'type': CONSONANT, 'accent': ['cmudict']},
	{'arpabet': 'D',  'type': CONSONANT, 'accent': ['cmudict']},
	{'arpabet': 'DH', 'type': CONSONANT, 'accent': ['cmudict']},
	{'arpabet': 'EH', 'type': VOWEL,     'accent': ['cmudict']},
	{'arpabet': 'ER', 'type': VOWEL,     'accent': ['cmudict']},
	{'arpabet': 'EY', 'type': VOWEL,     'accent': ['cmudict']},
	{'arpabet': 'F',  'type': CONSONANT, 'accent': ['cmudict']},
	{'arpabet': 'G',  'type': CONSONANT, 'accent': ['cmudict']},
	{'arpabet': 'HH', 'type': CONSONANT, 'accent': ['cmudict']},
	{'arpabet': 'IH', 'type': VOWEL,     'accent': ['cmudict']},
	{'arpabet': 'IY', 'type': VOWEL,     'accent': ['cmudict']},
	{'arpabet': 'JH', 'type': CONSONANT, 'accent': ['cmudict']},
	{'arpabet': 'K',  'type': CONSONANT, 'accent': ['cmudict']},
	{'arpabet': 'L',  'type': CONSONANT, 'accent': ['cmudict']},
	{'arpabet': 'M',  'type': CONSONANT, 'accent': ['cmudict']},
	{'arpabet': 'N',  'type': CONSONANT, 'accent': ['cmudict']},
	{'arpabet': 'NG', 'type': CONSONANT, 'accent': ['cmudict']},
	{'arpabet': 'OW', 'type': VOWEL,     'accent': ['cmudict']},
	{'arpabet': 'OY', 'type': VOWEL,     'accent': ['cmudict']},
	{'arpabet': 'P',  'type': CONSONANT, 'accent': ['cmudict']},
	{'arpabet': 'R',  'type': CONSONANT, 'accent': ['cmudict']},
	{'arpabet': 'S',  'type': CONSONANT, 'accent': ['cmudict']},
	{'arpabet': 'SH', 'type': CONSONANT, 'accent': ['cmudict']},
	{'arpabet': 'T',  'type': CONSONANT, 'accent': ['cmudict']},
	{'arpabet': 'TH', 'type': CONSONANT, 'accent': ['cmudict']},
	{'arpabet': 'UH', 'type': VOWEL,     'accent': ['cmudict']},
	{'arpabet': 'UW', 'type': VOWEL,     'accent': ['cmudict']},
	{'arpabet': 'V',  'type': CONSONANT, 'accent': ['cmudict']},
	{'arpabet': 'W',  'type': CONSONANT, 'accent': ['cmudict']},
	{'arpabet': 'Y',  'type': CONSONANT, 'accent': ['cmudict']},
	{'arpabet': 'Z',  'type': CONSONANT, 'accent': ['cmudict']},
	{'arpabet': 'ZH', 'type': CONSONANT, 'accent': ['cmudict']},
]

dict_formats = { # {0} = word ; {1} = context ; {2} = phonemes ; {3} = comment
	'cmudict-weide': {
		# formatting:
		'comment': '##{3}',
		'entry': '{0}  {2}',
		'entry-comment': '{0}  {2} #{3}',
		'entry-context': '{0}({1})  {2}',
		'entry-context-comment': '{0}({1})  {2} #{3}',
		'phonemes': lambda phonemes: ' '.join(phonemes),
		'word': lambda word: word.upper(),
		# parsing:
		'accent': 'cmudict',
		'word-validation': r'^[^ a-zA-Z]?[A-Z0-9\'\.\-\_]*$',
		'context-parser': int,
	},
	'cmudict': {
		# formatting:
		'comment': ';;;{3}',
		'entry': '{0}  {2}',
		'entry-comment': '{0}  {2} #{3}',
		'entry-context': '{0}({1})  {2}',
		'entry-context-comment': '{0}({1})  {2} #{3}',
		'phonemes': lambda phonemes: ' '.join(phonemes),
		'word': lambda word: word.upper(),
		# parsing:
		'accent': 'cmudict',
		'word-validation': r'^[^ a-zA-Z]?[A-Z0-9\'\.\-\_]*$',
		'context-parser': int,
	},
	'cmudict-new': {
		# formatting:
		'comment': ';;;{3}',
		'entry': '{0} {2}',
		'entry-context': '{0}({1}) {2}',
		'entry-comment': '{0} {2} #{3}',
		'entry-context-comment': '{0}({1}) {2} #{3}',
		'phonemes': lambda phonemes: ' '.join(phonemes),
		'word': lambda word: word.lower(),
		# parsing:
		'accent': 'cmudict',
		'word-validation': r'^[^ a-zA-Z]?[a-z0-9\'\.\-\_]*$',
		'context-parser': int,
	},
}

parser_warnings = {
	'context-values': 'check context values are numbers',
	'context-ordering': 'check context values are ordered sequentially',
	'duplicate-entries': 'check for matching entries (word, context, pronunciation)',
	'duplicate-pronunciations': 'check for duplicated pronunciations for an entry',
	'entry-spacing': 'check spacing between word and pronunciation',
	'invalid-phonemes': 'check for invalid phonemes',
	'missing-stress': 'check for missing stress markers',
	'phoneme-spacing': 'check for a single space between phonemes',
	'trailing-whitespace': 'check for trailing whitespaces',
	'unsorted': 'check if a word is not sorted correctly',
	'word-casing': 'check for consistent word casing',
}

default_warnings = [
	'context-values',
	'context-ordering',
	'entry-spacing',
	'invalid-phonemes',
	'phoneme-spacing',
	'word-casing'
]

# dict() is too slow for indexing cmudict entries, so use a simple trie
# data structure instead ...
class Trie:
	def __init__(self):
		self.root = {}

	def lookup(self, key):
		current = self.root
		for letter in key:
			if letter in current:
				current = current[letter]
			else:
				return False, None
		if None in current:
			return True, current[None]
		return False, None

	def __contains__(self, key):
		valid, _ = self.lookup(key)
		return valid

	def __getitem__(self, key):
		valid, item = self.lookup(key)
		if not valid:
			raise KeyError('Item not in Trie')
		return item

	def __setitem__(self, key, value):
		current = self.root
		for letter in key:
			current = current.setdefault(letter, {})
		current[None] = value

def sort(entries, mode):
	if mode is None:
		for entry in entries:
			yield entry
	elif mode in ['weide', 'air']:
		ordered = []
		for word, context, phonemes, comment, error in entries:
			if not word:
				yield (word, context, phonemes, comment, error)
				continue
			if mode == 'weide':
				if context:
					key = '{0}({1})'.format(word, context)
				else:
					key = word
			elif mode == 'air':
				if context:
					key = '{0}!{1}'.format(word, context)
				else:
					key = word
			ordered.append((key, (word, context, phonemes, comment, error)))
		for key, entry in sorted(ordered):
			yield entry
	else:
		raise ValueError('unsupported sort mode: {0}'.format(mode))

def format(dict_format, entries):
	fmt = dict_formats[dict_format]
	for word, context, phonemes, comment, error in entries:
		if error:
			print(error, file=sys.stderr)
			continue
		components = []
		if word:
			components.append('entry')
			word = fmt['word'](word)
		if context:
			components.append('context')
		if comment != None:
			components.append('comment')
		if phonemes:
			phonemes = fmt['phonemes'](phonemes)
		if len(components) == 0:
			print()
		else:
			print(fmt['-'.join(components)].format(word, context, phonemes, comment))

def read_file(filename):
	with open(filename) as f:
		for line in f:
			yield line.replace('\n', '')

def warnings_to_checks(warnings):
	checks = default_warnings
	for warning in warnings:
		if warning == 'all':
			checks = parser_warnings.keys()
		elif warning == 'none':
			checks = []
		elif warning.startswith('no-'):
			if warning[3:] in parser_warnings.keys():
				if warning[3:] in checks:
					checks.remove(warning[3:])
			else:
				raise ValueError('Invalid warning: {0}'.format(warning))
		elif warning in parser_warnings.keys():
			if warning not in checks:
				checks.append(warning)
		else:
			raise ValueError('Invalid warning: {0}'.format(warning))
	return checks

def load_phonemes(accent):
	if accent == 'cmudict':
		phonemeset = 'arpabet'
		phoneme_parser = ArpabetPhonemeSet()
	else:
		raise ValueError('Unsupported accent: {0}'.format(accent))

	valid_phonemes = set()
	missing_stress_marks = set()

	for p in phoneme_table:
		if p['type'] == VOWEL:
			missing_stress_marks.add(p[phonemeset])
			valid_phonemes.add('{0}0'.format(p[phonemeset]))
			valid_phonemes.add('{0}1'.format(p[phonemeset]))
			valid_phonemes.add('{0}2'.format(p[phonemeset]))
		else:
			valid_phonemes.add(p[phonemeset])

	return valid_phonemes, missing_stress_marks, phoneme_parser

def parse_cmudict(filename, checks, order_from):
	"""
		Parse the entries in the cmudict file.

		The return value is of the form:
			(line, format, word, context, phonemes, comment, error)
	"""
	re_linecomment = re.compile(r'^(##|;;;)(.*)$')
	re_entry = re.compile(r'^([^ a-zA-Z]?[a-zA-Z0-9\'\.\-\_]*)(\(([^\)]*)\))?([ \t]+)([^#]+)( #(.*))?[ \t]*$')
	format = None
	for line in read_file(filename):
		if line == '':
			yield line, format, None, None, None, None, None
			continue

		m = re_linecomment.match(line)
		if m:
			yield line, format, None, None, None, m.group(2), None
			continue

		m = re_entry.match(line)
		if not m:
			yield line, format, None, None, None, None, 'Unsupported entry: "{0}"'.format(line)
			continue

		word = m.group(1)
		context = m.group(3) # 2 = with context markers: `(...)`
		word_phoneme_space = m.group(4)
		phonemes = m.group(5)
		comment = m.group(7) or None # 6 = with comment marker: `#...`

		if not format: # detect the dictionary format ...
			cmudict_fmt = re.compile(dict_formats['cmudict']['word-validation'])
			if cmudict_fmt.match(word):
				format = 'cmudict'
				spacing = '  '
			else:
				format = 'cmudict-new'
				spacing = ' '

		if word_phoneme_space != spacing and 'entry-spacing' in checks:
			yield line, format, None, None, None, None, 'Entry needs {0} spaces between word and phoneme: "{1}"'.format(len(spacing), line)

		if phonemes.endswith(' ') and 'trailing-whitespace' in checks:
			yield line, format, None, None, None, None, 'Trailing whitespace in entry: "{0}"'.format(line)

		yield line, format, word, context, phonemes, comment, None

def parse(filename, warnings=[], order_from=0):
	checks = warnings_to_checks(warnings)
	previous_word = None
	valid_phonemes = None
	missing_stress_marks = None
	re_word = None
	context_parser = None
	phoneme_parser = None
	entries = Trie()
	lines = Trie()
	fmt = None
	for line, format, word, context, phonemes, comment, error in parse_cmudict(filename, checks, order_from):
		if error:
			yield None, None, None, None, error
			continue

		if not word and comment is not None: # line comment
			yield None, None, None, comment, None
			continue

		if not fmt:
			fmt = dict_formats[format]
			valid_phonemes, missing_stress_marks, phoneme_parser = load_phonemes(fmt['accent'])
			re_word = re.compile(fmt['word-validation'])
			context_parser = fmt['context-parser']

		if not re_word.match(word) and 'word-casing' in checks:
			yield None, None, None, None, 'Incorrect word casing in entry: "{0}"'.format(line)

		if previous_word and word < previous_word and 'unsorted' in checks:
			yield None, None, None, None, 'Incorrect word ordering ("{0}" < "{1}") for entry: "{2}"'.format(word, previous_word, line)

		try:
			if context is not None:
				context = context_parser(context)
		except ValueError:
			if 'context-values' in checks:
				yield None, None, None, None, 'Invalid context format "{0}" in entry: "{1}"'.format(m.group(GROUP_CONTEXT), line)

		for phoneme in phoneme_parser(phonemes):
			if ' ' in phoneme or '\t' in phoneme:
				phoneme = phoneme.strip()
				if 'phoneme-spacing' in checks:
					yield None, None, None, None, 'Incorrect whitespace after phoneme in entry: "{1}"'.format(phoneme, line)
			if phoneme in missing_stress_marks:
				if 'missing-stress' in checks:
					yield None, None, None, None, 'Vowel phoneme "{0}" missing stress marker in entry: "{1}"'.format(phoneme, line)
			elif not phoneme in valid_phonemes:
				if 'invalid-phonemes' in checks:
					yield None, None, None, None, 'Invalid phoneme "{0}" in entry: "{1}"'.format(phoneme, line)

		key = word.upper()
		position = order_from if context is None else context

		entry_line = '{0}({1}) {2}'.format(word, context, phonemes)
		if entry_line in lines and 'duplicate-entries' in checks:
			yield None, None, None, None, 'Duplicate entry: "{2}"'.format(position, expect_position, line)
		elif isinstance(position, int):
			pronunciation = ' '.join(phonemes)
			if key in entries:
				expect_position, pronunciations = entries[key]
			else:
				expect_position = order_from
				pronunciations = []
			if position != expect_position and 'context-ordering' in checks:
				yield None, None, None, None, 'Incorrect context ordering "{0}" (expected: "{1}") in entry: "{2}"'.format(position, expect_position, line)
			expect_position = expect_position + 1
			if pronunciation in pronunciations:
				if 'duplicate-pronunciations' in checks:
					yield None, None, None, None, 'Existing pronunciation in entry: "{2}"'.format(position, expect_position, line)
			else:
				pronunciations.append(pronunciation)
			entries[key] = (expect_position, pronunciations)

		lines[entry_line] = True
		previous_word = word

		yield word, context, phonemes, comment, None
