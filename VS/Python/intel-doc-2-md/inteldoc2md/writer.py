# -*- coding: utf8 -*-

import os
import re
import pdb
import time

class State(object):
	def __init__(self):
		self.code_mode = False;
		self.type = None
		self.type_next = None
	
class Writer(object):

	def __init__(self):
		#self.source = 'Intel® Architecture Instruction Set Extensions Programming Reference (APRIL 2017)'
		self.source = 'Intel® Architecture Software Developer\'s Manual (JULY 2017)'


	@staticmethod
	def _cleanup_hyphens(str):

		str = str.replace('•\n\n', '\n * ')
		str = str.replace('•\n', '\n * ')
		str = str.replace('•', '\n * ')

		str = str.replace('addi-\ntional', 'additional\n')

		str = str.replace('combina-\ntion ', 'combination\n')
		str = str.replace('compar-\nison)', 'comparison)\n')
		str = str.replace('compar-\nisons', 'comparisons\n')
		str = str.replace('corre-\nsponding', 'corresponding\n')

		 
		str = str.replace('documenta-\ntion', 'documentation\n')
		str = str.replace('destina-\ntion', 'destination\n')
		str = str.replace('desti-\nnation', 'destination\n')
		str = str.replace('infor-\nmation', 'information\n')
		str = str.replace('instruc-\ntions', 'instructions\n')
		str = str.replace('instruc-\ntion', 'instruction\n')
		str = str.replace('regis-\nters', 'registers\n')
		str = str.replace('regis-\nter', 'register\n')
		str = str.replace('oper-\nands', 'operands\n') 
		str = str.replace('oper-\nations', 'operations\n')
		
		str = str.replace('preci-\nsion', 'precision\n')
		str = str.replace('loca-\ntions', 'locations\n')
		str = str.replace('loca-\ntion', 'location\n')
		str = str.replace('speci-\nfied', 'specified\n')


		str = str.replace('single- precision', 'single-precision')
		str = str.replace('no- operand', 'no-operand')
		str = str.replace('no- operands', 'no-operands')
		str = str.replace('REP/REPE/REPZ /REPNE/REPNZ', 'REP/REPE/REPZ/REPNE/REPNZ')
		str = str.replace('general- purpose', 'general-purpose')
		return str


	def close_file(self, instruction, markdown):

		markdown = Writer._cleanup_hyphens(markdown)

		filename = './output/' + str(instruction).replace('/', '_').replace(' ', '_') + '.md'
		print 'writing ' + filename
		fwrite = open(filename, 'w')
		#generatedTime = time.strftime("%c")
		generatedTime = '22-aug-2017: 11:37:19'
		markdown += '\n --- \n<p align="right"><i>Source: '+self.source+'<br>Generated: '+generatedTime+'</i></p>\n'
		fwrite.write(markdown)
		fwrite.close()

	def write(self, piles):
		createNewFile = False

		if (len(piles) > 0):
			instruction_curr, descr = piles[0]._get_instruction()
		else:
			instruction_curr = None
			descr = None

		instruction_prev = instruction_curr

		state = State()
		state.code_mode = False;
		state.type = None
		state.type_next = None

		markdown = ''

		for i in range (0, len(piles)):
			pile = piles[i]
			pileInstruction, descr = pile._get_instruction()
			#print 'pileInstruction ' + str(pileInstruction)

			createNewFile = False
			if (pileInstruction != None):
				if (pileInstruction != instruction_curr):
					createNewFile = True
					instruction_prev = instruction_curr
					instruction_curr = pileInstruction
					#print 'instruction_prev=' + str(instruction_prev) +'; instruction_curr='+instruction_curr
				
			if (createNewFile):
				self.close_file(instruction_prev, markdown)
				markdown = ''

			markdown += pile.gen_markdown(state)

		self.close_file(instruction_curr, markdown)