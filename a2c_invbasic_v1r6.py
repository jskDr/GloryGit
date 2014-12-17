# Python Hangul Basic ver. org+0.2 
# Upgraded by Sungjin Kim (2014-11-27)
# Originated by Craig "Ichabod" O'Brien    
#
# Python 3.0 must be used because of on-the-fly dictionay deleting 
# The base source can be founded in the following link as basic.zip
# http://www.python-forum.org/viewtopic.php?f=11&t=603 
# [basic.zip] http://xenomind.com/Python/basic.zip 
#             written by Craig "Ichabod" O'Brien    
# Modified by Sungjin Kim (2014.11.25), https://www.facebook.com/jamessungjin.kim
# - Hangul can be used as well as English for commands.
# - Inverse commands can be possible soon for supporting Korean well. 

from __future__ import print_function

import cmd
import math
import os
import random
import re
import sys

HELP = {}
HELP[''] = """
THE FOLLOWING COMMANDS ARE AVAILABLE IN THE ICHABOD BASIC INTERPRETER. FOR
HELP ON COMMANDS ALLOWED IN ICHABOD BASIC PROGRAMS, TYPE 'HELP BASIC'.
BYE (종료): QUIT ICHABOD BASIC
CATALOG (목록): SHOW PROGRAMS AVAILABLE FOR LOADING
DEBUG: SET DEBUGGING TO SHOW LINE NUMBER AND VARIABLE TRACE
HELP: SHOW HELP FOR A SPECIFIED TOPIC
LIST (리스트): LIST THE CURRENT PROGRAM
NEW (신규): START A NEW PROGRAM
NODEBUG: TURN OFF DEGUGGING
OLD: LOAD AN OLD PROGRAM
RENAME: RENAME THE CURRENT PROGRAM
RUN (실행): RUN THE CURRENT PROGRAM
SAVE (저장): SAVE THE CURRENT PROGRAM
SCRATCH: DELETE THE CURRENT PROGRAM
UNSAVE: PERMANENTLY DELETE THE CURRENT PROGRAM.
FOR MORE INFORMATION ON A COMMAND TYPE HELP FOR THAT COMMAND.
"""
HELP['BASIC'] = """
EACH LINE IN THE PROGRAM MUST START WITH A LINE NUMBER. LINES ARE PROCESSED
IN THE ORDER OF THEIR LINE NUMBERS, EXCEPT AS MODIFIED BY GOTO, GOSUB, NEXT, 
AND RETURN STATEMENTS.
TO DELETE A LINE OF THE PROGRAM, ENTER THE LINE NUMBER WITH NO COMMAND.
VARIABLES NAMES MUST START WITH A LETTER OR UNDERSCORE, AND MAY CONTAIN 
LETTERS, NUMBERS, AND UNDERSCORES. STRING VARIABLES NAMES SHOULD START WITH
AN UNDERSCORE, NUMERIC VARIABLE NAMES SHOULD NOT.
STATEMENTS:
DATA (데이타): DEFINES PROGRAM DATA.
DEF (정의): DEFINES A FUNCTION TO BE USED LATER.
DIM (크기): DEFINES AN ARRAY.
END (끝내라): MARKS THE END OF THE PROGRAM.
FOR (돌려라): SETS UP A LOOP WITH AN INDEX.
GOSUB (갔다와라): REDIRECT PROCESSING AND REMEMBER CURRENT LINE.
GOTO (가라): REDIRECT PROCESSING.
IF (만약), THEN (이라면): DIVERT PROCESSING BASED ON VARIABLES.
INPUT (넣어라): GETS A RESPONSE FROM THE USER.
LET (대입): ASSIGN A VALUE TO A VARIABLE.
NEXT (다음): MARKS THE BOUNDARY OF A FOR LOOP.
ON (온): GOTO BASED ON A VARIABLE VALUE.
PRINT (찍어라): DISPLAY OUTPUT TO THE USER.
READ (읽어라): READ THE NEXT PIECE OF DATA.
REM (주석): REMARK.
RETURN (돌려주라): REDIRECT PROCESSING TO A GOSUB.
STOP (끝내라): END PROCESSING.
FOR MORE INFORMATION ON A STATEMENT, CHECK THE HELP FOR THAT STATEMENT.
FUNCTIONS:
ABS(X): THE ABSOLUTE VALUE OF X
ATN(X): THE ARC TANGENT OF X
CHR(X): CONVERT X TO A STRING USING ASCII
COS(X): THE COSINE OF X
EXP(X): E RAISED TO THE POWER X
INT(X): INTEGER CONVERSION OF X
LOG(X): THE NATURAL LOGARITHM OF X
ORD(_C): CONVERT _C TO AN INTEGER USING ASCII
RND(X): A RANDOM NUMBER BETWEEN 0 AND X
SIN(X): THE SINE OF X
SQR(X): THE SQUARE ROOT OF X
TAB(X): X SPACES
TAN(X): THE TANGENT OF X
TRIGONOMETRIC FUNCTIONS EXPECT AND RETURN VALUES IN RADIANS
"""
HELP['BYE'] = """
BYE (종료): QUIT ICHABOD BASIC. BE SURE TO SAVE YOUR PROGRAMS BEFORE LEAVING
ICHABOD BASIC.
"""
HELP['CATALOG'] = """
CATALOG (목록): SHOW PROGRAMS AVAILABLE FOR LOADING. LISTS ALL FILES IN THE 
CURRENT WORKING DIRECTORY WITH A BSC EXTENSION.
"""
HELP['DATA'] = """
DATA: DEFINES PROGRAM DATA. DATA IS FOLLOWED BY COMMA SEPARATED VALUES TO 
BE PUT INTO VARIABLES WITH A READ STATEMENT. VALUES MAY BE INTEGERS,
FLOATING POINT NUMBERS, OR STRING LITERALS ENCLOSED IN QUOTES. THE DATA
STATEMENT FOR A VALUE MUST COME BEFORE THE READ STATEMENT THAT READS THAT
VALUE. (DATA 2, 3, 5, 7, 11, 13, 17, 19)
"""
HELP['DEBUG'] = """
DEBUG: SET DEBUGGING TO SHOW LINE NUMBER AND VARIABLE TRACE. DEBUG STARTS
DEBUGGING MODE, DURING WHICH THE LINE NUMBER IS PRINTED FOR EVERY LINE OF CODE
PROCESSED. IN ADDITION, A SET OF COMMA SEPARATED VARIABLE NAMES MAY BE GIVEN
AS A PARAMETER TO THE DEBUG COMMAND. THESE VARIABLES AND THEIR VALUES WILL
BE PRINTED ALONG WITH THE LINE NUMBER.
"""
HELP['DEF'] = """
DEF: DEFINES A FUNCTION TO BE USED LATER. FOLLOW WITH THE NEW FUNCTION'S NAME,
A PARAMETER LIST IN PARENTHESES, AN EQUALS SIGN, AND THE FUNCTION AS AN
EXPRESSION OPERATING ON THE PARAMETERS. (DEF SQR(X) = X * X)
"""
HELP['DIM'] = """
DIM: DEFINES AN ARRAY. ARRAYS MAY BE ONE OR TWO DIMENSIONAL. ARRAYS ARE
REFERENCED USING BRACKETS (X[1] OR Y[3][5]) AND ARE ONE-INDEXED. USING
THE SAME NAME FOR ARRAY AND NON-ARRAY VARIABLES MAY CAUSE ERRORS.
MULTIPLE ARRAYS MAY BE DEFINED IN ONE DIM STATEMENT BY SEPARATING THEM
WITH COMMAS (DIM X[5], Y[10][8])
"""
HELP['END'] = """
END: MARKS THE END OF THE PROGRAM. EVERY PROGRAM SHOULD HAVE AN END STATEMENT.
PROGRAMS WITHOUT END STATEMENTS MAY HAVE ERRORS DURING EXECUTION. (END)
"""
HELP['FOR'] = """
FOR: SET A LOOP WITH A VARIABLE. A FOR STATEMENT HAS EIGHT PARTS, TWO OF THEM
OPTIONAL: FOR <VARIABLE> = <NUMBER> TO <NUMBER> STEP <NUMBER>. THE VARIABLE 
KEEPS TRACK OF THE LOOP COUNT, THE FIRST NUMBER IS THE STARTING VALUE OF THE
LOOP VARIABLE, THE SECOND NUMBER IS THE TERMINAL (LAST) VALUE OF THE LOOP 
VARIABLE, AND THE OPTIONAL THIRD (STEP) NUMBER IS ADDED TO THE LOOP VARIABLE 
EACH TIME THE CORRESPONDING NEXT STATEMENT IS REACHED. (FOR I = 1 TO 10)
"""
HELP['GIRLS'] = """
REPEAT AFTER ME: "YES, DEAR."
"""
HELP['GOSUB'] = """
GOSUB: REDIRECT PROCESSING AND REMEMBER CURRENT LINE. GOSUB WILL REDIRECT
PROCESSING TO THE SPECIFIED LINE NUMBER AND REMEMBER THE CURRENT LINE 
NUMBER. PROCESSING CAN BE REDICTED BACK TO THE CURRENT LINE NUMBER WITH A
RETURN STATEMENT. MULTIPLE GOSUB/RETURN REDIRECTIONS ARE POSSIBLE. THEY 
ARE HANDLED IN A LAST IN FIRST OUT (LIFO) ORDER. (GOSUB 180)
"""
HELP['GOTO'] = """
GOTO: REDIRECT PROCESSING. REDIRECTS PROCESSING TO THE SPECIFIED LINE
NUMBER. (GOTO 810)
"""
HELP['HELP'] = """
TO GET HELP ON HELP, TYPE HELP HELP
"""
HELP['IF'] = """
IF: DIVERT PROCESSING BASED ON VARIABLES. IF STATEMENTS HAVE TWO PARTS: A
CONDITION AND A LINE NUMBER TO GOTO IF THE CONDITION IS TRUE. THE CONDITION
AND THE LINE NUMBER ARE SEPARATED BY THE KEYWORD 'THEN'. (IF A[3] > X THEN 20)
"""
HELP['INPUT'] = """
INPUT: GETS INPUT FROM THE USER AND ASSIGNS IT TO THE SPECIFIED VARIABLE.
VALUES FOR NUMERIC VARIABLES (WITH A LEADING UNDERSCORE) ARE AUTOMATICALLY
CONVERTED. (INPUT X)
"""
HELP['LET'] = """
LET: ASSIGN A VALUE TO A VARIABLE. THE LET STATEMENT SHOULD BE FOLLOWED BY 
A VARIABLE NAME, AN EQUALS SIGN, AND AN EXPRESSION. THE RESULT OF THE
EXPRESSION IS ASSIGNED TO THE VARIABLE NAME. THE LET STATEMENT IS OPTIONAL,
ANY LINE WITH AN EQUALS SIGN AND NO OTHER COMMAND WILL BE INTERPRETTED AS
A LET STATEMENT (LET X = 5 * Y) OR (L[7] = SQR(X + Z))
"""
HELP['NEW'] = """
NEW (신규): START A NEW PROGRAM. THIS COMMAND ERASES THE PROGRAM CURRENTLY IN 
MEMORY, SO MAKE SURE THAT PROGRAM IS SAVED FIRST. IT ALSO REQUIRES A NEW
NAME FOR THE NEW PROGRAM. (NEW SIEVE)
"""
HELP['NEXT'] = """
NEXT: MARKS THE BOUNDARY OF A FOR LOOP. WHEN THE NEXT STATEMENT IS REACHED,
THE LOOP VARIABLE SPECIFIED BY THE NEXT STATMENT (NEXT I) HAS THE STEP VALUE
FOR THE LOOP ADDED TO IT. IT IS THEN CHECKED AGAINST THE TERMINAL VALUE FOR
THE LOOP. IF IT IS GREATER THAN THE TERMINAL VALUE (LESS THAN FOR NEGATIVE
STEP VALUES) THE LOOP TERMINATES AND PROCESSING CONTINUES WITH THE NEXT
LINE OF CODE. OTHERWISE PROCESSING RETURNS TO THE LINE JUST AFTER THE 
DEFINING FOR STATEMENT. (NEXT I)
"""
HELP['NODEBUG'] = """
NODEBUG: TURN OFF DEGUGGING. STOPS LINE AND VARIABLE TRACING. (NODEBUG)
"""
HELP['OLD'] = """
OLD: LOAD AN OLD PROGRAM. LOADS A PREVIOUSLY SAVED PROGRAM INTO MEMORY.
THIS DELETES ANY PROGRAM ALREADY IN MEMORY, SO BE SURE TO SAVE BEFORE
USING OLD. OLD MUST BE FOLLOWED BY THE NAME OF ONE OF THE PROGRAMS LISTED 
WITH THE CATALOG COMMAND. (OLD SIEVE)
"""
HELP['ON'] = """
ON: GOTO BASED ON THE VALUE OF A VARIABLE. THE ON STATEMENT IS FOLLOWED
BY A VARIABLE NAME, THE GOTO KEYWORD, AND A SERIES OF COMMA SEPARATED LINE
NUMBERS. IF THE VALUE OF THE VARIABLE IS 1, PROCESSING GOTO'S THE FIRST
LINE NUMBER, IF IT IS 2, PROCESSING GOTO'S THE SECOND LINE NUMBER, AND
SO ON. (ON X GOTO 180, 810, 1999)
"""
HELP['PRINT'] = """
PRINT (찍어라): DISPLAY OUTPUT TO THE USER. THE PRINT STATEMENT IS FOLLOWED BY ONE
OR MORE VARIABLE NAMES OR STRING LITERALS SEPARATED BY SEMI-COLONS. EACH
ONE IS EVALUATED AND DISPLAYED TO THE USER WITH A SPACE IN BETWEEN. IF THE
PRINT COMMAND ENDS WITH A SEMI-COLON, A NEW LINE IS NOT PRINTED, AND THE
NEXT PRINT STATEMENT WILL BE DISPLAYED ON THE SAME LINE. (PRINT "THE VALUE
IS"; X)
"""
HELP['READ'] = """
READ: READ THE NEXT PIECE OF DATA. THE READ STATEMENT SPECIFIES A VARIABLE
AND SETS THAT VARIABLE TO EQUAL THE NEXT PIECE OF DATA FROM A DATA STATEMENT.
VALUES ARE READ FROM DATA STATEMENTS IN THE ORDER THEY ARE PROCESSED, AND
IN THE ORDER THEY ARE LISTED IN THE DATA STATEMENT. DATA STATEMENTS WITH THE
VALUE READ MUST COME BEFORE THE READ STATEMENT. (READ L[X])
"""
HELP['REMARK'] = """
REM: REMARK. REMARKS ARE NOT PROCESSED AND ANY TEXT AFTER REM IS IGNORED.
REMARKS ARE FOR EXPLAINING THE PROGRAM AND HOW IT WORKS TO OTHERS READING IT.
(REM THIS IS A REMARK)
"""
HELP['RENAME'] = """
RENAME: RENAME THE CURRENT PROGRAM. THE CURRENT PROGRAM IS RETAINED, BUT 
GIVEN A NEW NAME FOR FUTURE SAVES. TO COPY A PROGRAM, OPEN IT WITH OLD,
RENAME IT, AND SAVE IT AGAIN.
"""
HELP['RETURN'] = """
RETURN: REDIRECT PROCESSING TO A GOSUB. RETURN REDIRECTS PROCESSING TO THE
LAST GOSUB STATEMENT THAT WAS EXECUTED. (RETURN)
"""
HELP['RUN'] = """
RUN (실행): BASIC PROGRAM IS INVOKED.
"""
HELP['SAVE'] = """
SAVE (저장): SAVE THE CURRENT PROGRAM. THE SAVED PROGRAM CAN BE RETRIEVED WITH THE
OLD COMMAND. SAVE EARLY, SAVE OFTEN.
"""
HELP['SCRATCH'] = """
SCRATCH: DELETE THE CURRENT PROGRAM. THIS ONLY DELETES THE CODE ENTERED.
ANY NEW CODE ENTERED WILL BE CONSIDERED TO HAVE THE CURRENT PROGRAM NAME.
TO DELETE AND RENAME, USE THE NEW COMMAND.
"""
HELP['STOP'] = """
STOP: END PROCESSING. THE STOP STATEMENT ENDS PROCESSING BEFORE THE END OF 
THE PROGRAM IS REACHED. (STOP)
"""
HELP['UNSAVE'] = """
UNSAVE: PERMANENTLY DELETE THE CURRENT PROGRAM. UNSAVE CLEARS THE PROGRAM
NAME, DELETES THE PROGRAM FROM TEMPORARY MEMORY, AND DELETES THE PROGRAM
FROM PERMANENT MEMORY.
"""

class BASIC(cmd.Cmd):
	"""
	A BASIC interpreter in Python.
	
	BASIC is Beginner's All-purpose Symbolic Instruction Code, a programming
	language for non-technical users developed at Dartmouth in the 1960s. This
	is basically an implementation of the original Dartmouth BASIC, with a more
	limited IF/THEN statement.
	
	Class Attributes:
	qq_re: A regular expression for text in double quotes. (re.RE)
	
	Methods:
	basic_def: Handle function definitions. (None)
	basic_dim: Handle array definitions. (None)
	"""
	
	qq_re = re.compile('("*?")"')
	
	def basic_def(self, tail):
		"""
		basic_def(tail)
		Handle function definitions. (None)
		
		Parameters:
		tail: The tail of the BASIC command.
		"""
		# extract the parts
		func_name, eq, func_def = tail.partition('=')
		func_param = func_name[(func_name.find('(')) + 1:func_name.find(')')]
		func_name = func_name[:func_name.find('(')].strip()
		# create and store a lambda function
		lambda_text = 'lambda {}: {}'.format(func_param, func_def)
		self.variables[func_name] = eval(lambda_text, self.variables)
	
	def basic_dim(self, tail):
		"""
		basic_dim(tail)
		Handle array definitions. (None)
		
		BASIC arrays are 1-indexed, so the Python represenations are one longer
		so that the indexes match up.
		
		Parameters:
		tail: The tail of the BASIC command.
		"""
		# check each definition
		for var in tail.split(','):
			# extract the parts
			name = var[:var.find('[')].strip()
			dim1 = eval(var[(var.find('[') + 1):var.find(']')], self.variables) + 1
			# check for second dimension and create array
			if var.count('[') > 1:
				dim2 = eval(var[(var.rfind('[') + 1):var.rfind(']')], self.variables) + 1
				self.variables[name] = [[0] * dim2 for x in range(dim1)]
			else:
				self.variables[name] = [0] * dim1
	
	def basic_for(self, tail):
		"""
		basic_for(tail)
		Handle for loops. (str, int, int)
		
		The return value is the name of the looping variable, the termination
		value, and the increment value.
		
		Parameters:
		tail: The tail of the BASIC command.
		"""
		# split the parts
		name, x, span = tail.partition('=')
		if '부터' in span:
			start, x, stop = span.partition('부터')
		else:
			start, x, stop = span.partition('TO')
            
		# check for a step argument
		if 'STEP' in stop:
			stop, x, step = stop.partition('STEP')
		elif '단계' in stop:
			stop, x, step = stop.partition('단계')
		else:
			step = '1'

		# set up loop variable and return tracking
		self.variables[name.strip()] = eval(start, self.variables)
		return name.strip(), eval(stop, self.variables), eval(step, self.variables)
		
	def basic_if(self, tail):
		"""
		basic_if(tail)
		Handle conditional statements. (int)
		
		Returns 0 if the conditional is false, the goto line number otherwise.
		
		Parameters:
		tail: The tail of the BASIC command.
		"""
		# massage conditional for Python evalulation
		tail = tail.replace('AND', 'and')
		tail = tail.replace('OR', 'or')
		tail = tail.replace('=', '==')
		# correct incorrect corrections correctly
		tail = tail.replace('!==', '!=')
		tail = tail.replace('>==', '>=')
		tail = tail.replace('<==', '<=')
		# separate out condtion and goto
		if '이라면' in tail:
			condition, x, goto = tail.partition('이라면')
		else:
			condition, x, goto = tail.partition('THEN')
		# evaluate condition
		if eval(condition, self.variables):
			return int(goto)
		else:
			return 0
		
	def basic_input(self, tail):
		"""
		basic_input(tail)
		Handle input from the user (None)
		
		The values are put into the variable tracking directly.
		
		Parameters:
		tail: The tail of the BASIC command.
		"""
		# get the input
		tail = tail.strip()
		self.variables[tail] = input()
		# redo the input for non-string variables
		if not tail.startswith('_'):
			self.variables[tail] = int(self.variables[tail])
	
	def basic_on(self, tail):
		"""
		basic_on(tail)
		Handle variable dependent branching. (None)
		
		Parameters:
		tail: The tail of the BASIC command.
		"""
		# split out the command parts
		var, on, gotos = tail.partition('GOTO')
		# use list indexing (-1 for different indexes) to determine the correct goto
		on_text = '[{}][{} - 1]'.format(gotos.strip(), var.strip())
		return eval(on_text, self.variables)
	
	def basic_print(self, tail):
		"""
		basic_print(tail)
		Handle output to the user.
		
		Parameters:
		tail: The tail of the BASIC command.
		"""
		# print the parts of the statement
		for group in tail.split(';'):
			if group:
				print(eval(group, self.variables), end = ' ')
		# check for retaining the line
		if tail.endswith(';'):
			print(' ', end = '')
		else:
			print()
	
	def _default_r0(self, line):
		"""
		default(line)
		Handle unhandled commands.
		
		If there's a line number, assume it is part of the BASIC code. Otherwise 
		give an error to the user.
		
		Parameter:
		line: The command line entered by the user. (str)
		"""
		# check for valid line of BASIC code
		try:
			# check for program in progress
			if self.code_name:
				line_num = int(line.split()[0])
				# check for adding or deleting a line
				try:
					basic = line.split(None, 1)[1]
					self.code[line_num] = line.split(None, 1)[1]
				except IndexError:
					del self.code[line_num]
			else:
				print('\nNO PROGRAM STARTED. PLEASE USE NEW TO START A PROGRAM.\n')
		except ValueError:
			print('\nERROR: INVALID COMMAND.\n')

	def default(self, line):
		"""
		default(line)
		Handle unhandled commands.
		
		[Original] If there's a line number, assume it is part of the BASIC code. Otherwise 
		give an error to the user.

		[2014-12-14] Korea commands can be used. Commands of ['종료', '목록'] are used.
		
		Parameter:
		line: The command line entered by the user. (str)
		"""
		# check for valid line of BASIC code
		try:
			# check for program in progress
			# First, general commands are executed. 
			# Then, code is written. 
			if line == '종료':
				return self.do_BYE( None)
			elif line == '목록':
				self.do_CATALOG( None)
			elif line.split()[0].strip() == '신규':
				self.do_NEW( line.split(None, 1)[1])
			elif line == '저장':
				self.do_SAVE( None)
			elif line == '리스트':
				self.do_LIST( None)
			elif line == '실행':
				words = line.split()
				if len(words) == 1:
					self.do_RUN( None)
				else:
					self.do_RUN( line.split(None, 1)[1])
			elif self.code_name:
				line_num = int(line.split()[0])
				# check for adding or deleting a line
				try:
					basic = line.split(None, 1)[1]
					self.code[line_num] = line.split(None, 1)[1]
				except IndexError:
					del self.code[line_num]
			else:
				print('\nNO PROGRAM STARTED. PLEASE USE NEW TO START A PROGRAM.\n')
		except ValueError:
			print('\nERROR: INVALID COMMAND.\n')

	
	def do_BYE(self, line):
		"""
		do_BYE(line)
		Handle requests to leave Ichabod BASIC.
		
		Parameter:
		line: The command line entered by the user. (str)
		"""
		return True
	
	def do_CATALOG(self, line):
		"""
		do_CATALOG(line)
		Handle requests to list available programs.
		
		Parameter:
		line: The command line entered by the user. (str)
		"""
		# get the programs
		programs = [file_name for file_name in os.listdir() if file_name.lower().endswith('.bsc')]
		# print em if there are any
		if programs:
			print()
			for program in programs:
				print(program[:-4].upper())
			print()
		else:
			print('\nNO PROGRAMS FOUND.\n')
			
	def do_DEBUG(self, line):
		"""
		do_DEBUG(line)
		Handle request to turn on debugging.
		
		Parameters:
		line: The command line entered by the user. (str)
		"""
		self.debug = True
		self.debug_variables = [word.strip() for word in line.split(',')]
		
	def do_HELP(self, line):
		"""
		do_HELP(line)
		Handle help requests.
		
		Parameters:
		line: The command line entered by the user. (str)
		"""
		if line.strip() in HELP:
			print(HELP[line.strip()])
		else:
			print('\nTHERE IS NO HELP FOR THAT TOPIC.\n')
	
	def do_LS(self, line):
		"""
		do_LS(line)
		Hanle requests to translate and print the program.
		Translate from lang1 to lang2

		Parameters:
		line -> lang1, lang2
		"""
		if line == '-h':
			print( 'ls kor, eng')
			print( 'ls eng, kor')
		elif line == '':
			self.do_LIST( line)
		else:
			try:
				lang1, lang2 = line.split(',')
				self.LS( lang1.strip(), lang2.strip())
			except ValueError:
				print( 'Command error: Type LS -h')

	def LS(self, lang1, lang2):
		if self.inverse == False:
			self.LS_LEFT( lang1, lang2)
		else:
			self.LS_RIGHT( lang1, lang2)

	def LS_LEFT(self, lang1, lang2):
		"""
		_do_LIST_ENG_LEFT(line)
		Handle requests to print the program.
		If hangul keyword is finding, it is changed 
		to the correspoding english keyword such as print to 찍어라.
		* do_LIST_ENG calls do_LIST_ENG_LEFT or LIST_ENG_RIGHT
		  depeding on self.inverse flag.
		  Then, do_LIST_ENG_LEFT will be moved to _do_LIST_ENG_LEFT for hiddening.

		Parameters:
		line: The command line entered by the user. (str)
		"""
		# print the lines in order
		line_nums = sorted(self.code.keys())
		print()
		for line_num in line_nums:
			basic_cmd, basic_tail = self.line_split(self.code[line_num])
			#The original statement is shown for reference.
			# print('[ORG]', line_num, basic_cmd, basic_tail)
			try:
				idx = self.keywords[ lang1].index(basic_cmd)
				basic_cmd = self.keywords[ lang2][ idx]
				#DEBUG: how to changed idx is recorded.
				#print( idx, basic_cmd)
			except ValueError:
				"The correspoding keywords are not supported yet"
				basic_cmd = basic_cmd
			print(line_num, basic_cmd, basic_tail)
		print()

	def LS_RIGHT(self, lang1, lang2):
		"""
		_do_LIST_ENG_RIGHT(line)
		Handle requests to print the program.
		If hangul keyword is finding, it is changed 
		to the correspoding english keyword such as print to 찍어라.
		* do_LIST_ENG calls do_LIST_ENG_LEFT or LIST_ENG_RIGHT
		  depeding on self.inverse flag.
		  Then, do_LIST_ENG_LEFT will be moved to _do_LIST_ENG_LEFT for hiddening.

		Parameters:
		line: The command line entered by the user. (str)
		"""
		# print the lines in order
		line_nums = sorted(self.code.keys())
		print()
		for line_num in line_nums:
			basic_cmd, basic_tail = self.line_split(self.code[line_num])
			#The original statement is shown for reference.
			# print('[ORG]', line_num, basic_cmd, basic_tail)
			try:
				idx = self.keywords[lang1].index(basic_cmd)
				basic_cmd = self.keywords[lang2][ idx]
				#DEBUG: how to changed idx is recorded.
				#print( idx, basic_cmd)
			except ValueError:
				"The correspoding keywords are not supported yet"
				basic_cmd = basic_cmd
			# The prining order is different.
			print(line_num, basic_tail, basic_cmd)
		print()

	def do_LIST(self, line):
		"""
		do_LIST(line)
		Handle requests to print the program.
		
		Parameters:
		line: The command line entered by the user. (str)
		"""
		# print the lines in order
		line_nums = sorted(self.code.keys())
		print()
		for line_num in line_nums:
			print(line_num, self.code[line_num])
		print()

	def do_LIST_ENG(self, line):
		"""
		do_LIST_ENG(line)
		It calls do_LIST_ENG_LEFT or LIST_ENG_RIGHT
		depeding on self.inverse flag.
		Then, do_LIST_ENG_LEFT will be moved to _do_LIST_ENG_LEFT for hiddening.

		Parameters:
		line: The command line entered by the user. (str)
		"""
		if self.inverse == False:
			self._do_LIST_ENG_LEFT(line)
		else:
			self._do_LIST_ENG_RIGHT(line)

	def _do_LIST_ENG_LEFT(self, line):
		"""
		_do_LIST_ENG_LEFT(line)
		Handle requests to print the program.
		If hangul keyword is finding, it is changed 
		to the correspoding english keyword such as print to 찍어라.
		* do_LIST_ENG calls do_LIST_ENG_LEFT or LIST_ENG_RIGHT
		  depeding on self.inverse flag.
		  Then, do_LIST_ENG_LEFT will be moved to _do_LIST_ENG_LEFT for hiddening.

		Parameters:
		line: The command line entered by the user. (str)
		"""
		# print the lines in order
		line_nums = sorted(self.code.keys())
		print()
		for line_num in line_nums:
			basic_cmd, basic_tail = self.line_split(self.code[line_num])
			#The original statement is shown for reference.
			# print('[ORG]', line_num, basic_cmd, basic_tail)
			try:
				idx = self.keywords['kor'].index(basic_cmd)
				basic_cmd = self.keywords['eng'][ idx]
				#DEBUG: how to changed idx is recorded.
				#print( idx, basic_cmd)
			except ValueError:
				"The correspoding keywords are not supported yet"
				basic_cmd = basic_cmd
			print(line_num, basic_cmd, basic_tail)
		print()

	def _do_LIST_ENG_RIGHT(self, line):
		"""
		_do_LIST_ENG_RIGHT(line)
		Handle requests to print the program.
		If hangul keyword is finding, it is changed 
		to the correspoding english keyword such as print to 찍어라.
		* do_LIST_ENG calls do_LIST_ENG_LEFT or LIST_ENG_RIGHT
		  depeding on self.inverse flag.
		  Then, do_LIST_ENG_LEFT will be moved to _do_LIST_ENG_LEFT for hiddening.

		Parameters:
		line: The command line entered by the user. (str)
		"""
		# print the lines in order
		line_nums = sorted(self.code.keys())
		print()
		for line_num in line_nums:
			basic_cmd, basic_tail = self.line_split(self.code[line_num])
			#The original statement is shown for reference.
			# print('[ORG]', line_num, basic_cmd, basic_tail)
			try:
				idx = self.keywords['kor'].index(basic_cmd)
				basic_cmd = self.keywords['eng'][ idx]
				#DEBUG: how to changed idx is recorded.
				#print( idx, basic_cmd)
			except ValueError:
				"The correspoding keywords are not supported yet"
				basic_cmd = basic_cmd
			# The prining order is different.
			print(line_num, basic_tail, basic_cmd)
		print()

	def do_LIST_KOR(self, line):
		"""
		do_LIST_KOR(line)
		It calls do_LIST_KOR_LEFT or LIST_KOR_RIGHT
		depeding on self.inverse flag.

		Parameters:
		line: The command line entered by the user. (str)
		"""
		if self.inverse == False:
			self._do_LIST_KOR_LEFT(line)
		else:
			self._do_LIST_KOR_RIGHT(line)

	def _do_LIST_KOR_LEFT(self, line):
		"""
		_do_LIST_KOR_LEFT(line)
		Handle requests to print the program.
		If hangul keyword is finding, it is changed 
		to the correspoding english keyword such as from 찍어라 to print.

		Parameters:
		line: The command line entered by the user. (str)
		"""
		# print the lines in order
		line_nums = sorted(self.code.keys())
		print()
		for line_num in line_nums:
			basic_cmd, basic_tail = self.line_split(self.code[line_num])
			#The original statement is shown for reference.
			# print('[ORG]', line_num, basic_cmd, basic_tail)
			try:
				idx = self.keywords['eng'].index(basic_cmd)
				basic_cmd = self.keywords['kor'][ idx]
				#DEBUG: how to changed idx is recorded.
				#print( idx, basic_cmd)
			except ValueError:
				"The correspoding keywords are not supported yet"
				basic_cmd = basic_cmd
			print(line_num, basic_cmd, basic_tail)
		print()

	def _do_LIST_KOR_RIGHT(self, line):
		"""
		_do_LIST_KOR_RIGHT(line)
		Handle requests to print the program.
		If hangul keyword is finding, it is changed 
		to the correspoding english keyword such as from 찍어라 to print.

		Parameters:
		line: The command line entered by the user. (str)
		"""
		# print the lines in order
		line_nums = sorted(self.code.keys())
		print()
		for line_num in line_nums:
			basic_cmd, basic_tail = self.line_split(self.code[line_num])
			#The original statement is shown for reference.
			# print('[ORG]', line_num, basic_cmd, basic_tail)
			try:
				idx = self.keywords['eng'].index(basic_cmd)
				basic_cmd = self.keywords['kor'][ idx]
				#DEBUG: how to changed idx is recorded.
				#print( idx, basic_cmd)
			except ValueError:
				"The correspoding keywords are not supported yet"
				basic_cmd = basic_cmd
			# The prining order is different.
			print(line_num, basic_tail, basic_cmd)
		print()
			
	def do_NEW(self, line):
		"""
		do_NEW(line)
		Handle requests start a new program.
		
		Parameters:
		line: The command line entered by the user. (str)
		"""
		# check for program name
		if line.strip():
			self.code = {}
			self.code_name = line.strip()
		else:
			print('\nERROR: PLEASE PROVIDE A PROGRAM NAME.\n')
		
	def do_NODEBUG(self, line):
		"""
		do_NODEBUG(line)
		Handle requests stop debugging traces.
		
		Parameters:
		line: The command line entered by the user. (str)
		"""
		self.debug = False

	def do_INVERSE(self, line):
		"""
		do_INVERSE(line)
		Keyword takes at the end of a sentence.
		
		Parameters:
		line: The command line entered by the user. (str)
		"""
		self.inverse = True

	def do_REVERSE(self, line):
		"""
		do_REVERSE(line)
		Keyword takes at the start point of a sentence.
		
		Parameters:
		line: The command line entered by the user. (str)
		"""
		self.inverse = False

	def do_MODE( self, line):
		"""
		do_MODE(line)
		All status paramters are displayed.
		
		Parameters:
		line: The command line entered by the user. (str)
		"""
		print( '[MODE]')
		print( 'Current Mode :', self.mode)
		print( 'All Modes = [{}]'.format( ', '.join(self.all_modes)))
		
		print( 'Flag of inverse:', self.inverse)

	def do_MODETO( self, line):
		"""
		do_MOTETO( line)
		The mode is changed to new mode.

		Parameters:
		line: The new mode is entered by an user.
		"""

		if line in self.all_modes:
			print( 'The mode is changed from {0} to {1}.'.format(self.mode, line))
			self.mode = line	
		else:
			print( 'Type valed modes such as [{}]'.format( ', '.join( self.all_modes)))

	def do_OLD(self, line):
		"""
		do_OLD(line)
		Handle requests load old programs.
		
		Parameters:
		line: The command line entered by the user. (str)
		"""
		try:
			new_code = {}
			for code_line in open(line.strip() + '.bsc'):
				line_num, space, code = code_line.partition(' ')
				new_code[int(line_num)] = code.strip()
			self.code = new_code
			self.code_name = line.strip()
		except IOError:
			print('\nERROR: CANNOT FIND PROGRAM {}.\n'.format(line.strip()))
				
	def do_RENAME(self, line):
		"""
		do_RENAME(line)
		Handle requests to rename the current program.
		
		Parameters:
		line: The command line entered by the user. (str)
		"""
		if line.strip() and self.code_name:
			self.code_name = line.strip()
		elif self.code_name:
			print('\nPLEASE PROVIDE A NEW NAME FOR THE PROGRAM.\n')
		else:
			print('\nERROR: NO PROGRAM TO RENAME.\n')
			
	def do_RUN(self, line):
		"""
		do_RUN(line)
		Interpret and run the current BASIC program.
		
		This steps through the code lines in order, interpreting and evaluating
		each one in turn, branching and looping as required.
		
		Parameters:
		line: The command line entered by the user. (str)
		"""
		# store variables for later clean up
		master_variables = self.variables.keys()
		# prep the command loop
		line_nums = sorted(self.code.keys())
		pointer = 0
		gosubs = []
		for_loops = {}
		data = []
		try:
			# loop through the basic code lines
			while pointer < len(line_nums):
				# update line tracking
				line_num = line_nums[pointer]
				basic_cmd, basic_tail = self.line_split(self.code[line_num])
				# check for debugging
				if self.debug:
					print(line_num, end = ' ')
					for variable in self.debug_variables:
						if variable in self.variables:
							print(variable, '=', self.variables[variable], end = ' ')
					print()
				# interpret based on first word of line
				if basic_cmd == 'DATA' or basic_cmd == '데이타':
					data.extend(eval('[{}]'.format(basic_tail)))
				elif basic_cmd == 'DEF' or basic_cmd == '정의':
					self.basic_def(basic_tail)
				elif basic_cmd == 'DIM' or basic_cmd == '크기':
					self.basic_dim(basic_tail)
				elif basic_cmd == 'END' or basic_cmd == '끝내라':
					break
				elif basic_cmd == 'FOR' or basic_cmd == '돌려라':
					name, limit, step = self.basic_for(basic_tail)
					for_loops[name] = [limit, step, pointer]
				elif basic_cmd == 'GOSUB' or basic_cmd == '갔다와라':
					gosubs.append(pointer)
					pointer = line_nums.index(int(basic_tail)) - 1
				elif basic_cmd == 'GOTO' or basic_cmd == '가라':
					pointer = line_nums.index(int(basic_tail)) - 1
				elif basic_cmd == 'IF' or basic_cmd == '만약' or basic_cmd == '으로_가라':
					goto = self.basic_if(basic_tail)
					if goto:
						pointer = line_nums.index(goto) - 1
				elif basic_cmd == 'INPUT' or basic_cmd == '넣어라':
					self.basic_input(basic_tail)
				elif basic_cmd == 'LET' or basic_cmd == '대입':
					exec(basic_tail, self.variables)
				elif basic_cmd == 'NEXT' or basic_cmd == '다음':
					name = basic_tail.strip()
					self.variables[name] += for_loops[name][1]
					if for_loops[name][1] > 0:
						loop = self.variables[name] <= for_loops[name][0]
					else:
						loop = self.variables[name] >= for_loops[name][0]
					if loop:
						pointer = for_loops[name][2]
					else:
						del for_loops[name]
				elif basic_cmd == 'ON' or basic_cmd == '온':
					pointer = line_nums.index(self.basic_on(basic_tail)) - 1
				elif basic_cmd == 'PRINT' or basic_cmd == '찍어라':
					self.basic_print(basic_tail)
				elif basic_cmd == 'READ' or basic_cmd == '읽어라':
					exec('{} = {}'.format(basic_tail, data.pop(0)), self.variables)
				elif basic_cmd == 'REM' or basic_cmd == '주석':
					pass
				elif basic_cmd == 'RETURN' or basic_cmd == '돌려주라':
					pointer = gosubs.pop()
				elif basic_cmd == 'STOP' or basic_cmd == '끝내라':
					break
				elif '=' in basic_tail or '=' in basic_cmd:
					exec(self.code[line_num], self.variables)
				else:
					print('\nError on line {}: invalid command {}\n'.format(line_num, basic_cmd))
					break
				pointer += 1
		except Exception as err:
			if self.debug:
				# give full error information when debugging
				message = '\nINTERPRETER ERROR ON LINE {}/{}\n{}\n'
				print(message.format(line_num, sys.exc_info()[2].tb_lineno, err.args[0].upper()))
			else:
				# just give line number of any error when not debugging
				print('\nINTERPRETER ERROR ON LINE {}\n'.format(line_num))
		# clean up program variables
		for variable in self.variables:
			if variable not in master_variables:
				del self.variables[variable]
		print()
	
	def do_SAVE(self, line):
		"""
		do_SAVE(line)
		Handle requests to save the current program
		
		Parameters:
		line: The command line entered by the user. (str)
		"""
		# check for program to save
		if self.code_name:
			# write out code lines in order
			line_nums = sorted(self.code.keys())
			program_file = open(self.code_name + '.bsc', 'w')
			for line_num in line_nums:
				line_text = '{} {}\n'.format(line_num, self.code[line_num])
				program_file.write(line_text)
			print('\nSAVED PROGRAM {}\n'.format(self.code_name.upper()))
		else:
			print('\nNO PROGRAM TO SAVE\n')
			
	def do_SCRATCH(self, line):
		"""
		do_SCRATCH(line)
		Handle requests to delete the current program.
		
		Parameters:
		line: The command line entered by the user. (str)
		"""
		if self.code_name:
			self.code = {}
		else:
			print('\nERROR: NO PROGRAM TO SCRATCH.\n')
			
	def do_UNSAVE(self, line):
		"""
		do_UNSAVE(line)
		Handle requests to delete the current program permanently.
		
		Parameters:
		line: The command line entered by the user. (str)
		"""
		# check for program to unsave
		if self.code_name:
			try:
				temp = self.code_name
				self.code_name = ''
				self.code = {}
				os.remove('{}.bsc'.format(temp))
			except OSError:
				print('\nERROR DELETING PERMANENT FILE.\n')
		else:
			print('\nNO PROGRAM TO UNSAVE\n')
			
	def line_split(self, line):
		"""
		line_rsplit(line)
		Split left or right depending on self.inverse
		
		Parameters:
		line: A line of BASIC code. (str)
		"""
		if self.inverse == False:
			return self.line_lsplit( line)
		else:
			return self.line_rsplit( line)

	def line_lsplit(self, line):
		"""
		line_lsplit(line)
		Split a line of basic code into it's command and parameters.
		
		Parameters:
		line: A line of BASIC code. (str)
		"""
		# get the command
		line_cmd = line.split()[0].upper()
		try:
			# split out the quoted parts
			base = line.split(None, 1)[1]
			base = self.qq_re.split(base)
			# capitalize everything not in quotes
			line_tail = ''
			for part in base:
				if part.startswith('"'):
					line_tail += part
				else:
					line_tail += part.upper()
		except IndexError:
			# blank tail for parameterless commands
			line_tail = ''
		return line_cmd, line_tail

	def line_rsplit(self, line):
		"""
		line_rsplit(line)
		Split a line of basic code into parameters and its command.
		
		Parameters:
		line: A line of BASIC code. (str)
		"""
		# get the command
		try:
			# If it is error, except part will be performed. 
			line_cmd = line.rsplit(None, 1)[1].upper()

			# split out the quoted parts
			base = line.rsplit(None, 1)[0]
			base = self.qq_re.split(base)
			# capitalize everything not in quotes
			line_tail = ''
			for part in base:
				if part.startswith('"'):
					line_tail += part
				else:
					line_tail += part.upper()
		except IndexError:
			# blank tail for parameterless commands
			line_cmd = line.rsplit(None, 1)[0].upper()
			line_tail = ''
		
		return line_cmd, line_tail

	def preloop(self):
		"""
		preloop()
		1. Set up the Cmd instance
		2. lowercase keyword will be avaiblae by mapping from uppercase to lowercase cmd
		"""
		
		"Set up the Cmd instance"
		self.code = {}
		self.code_name = ''
		self.debug = []
		self.prompt = ']'
		self.variables = {'__builtins__': {}, 'ABS': abs, 'ATN': math.atan, 'CHR': chr, 'COS': math.cos, 
			'EXP': math.exp, 'INT': int, 'LOG': math.log, 'ORD': ord, 'RND': RND, 'SIN': math.sin, 
			'SQR': math.sqrt, 'TAB': TAB, 'TAN': math.tan}
		"Code will be read from the stat point."
		
		"Set up modes"
		self.all_modes = ['eng_and_kor_mixed', 'eng_only', 'kor_only', 'kor_inv_only']
		self.mode = 'eng_and_kor_mixed' # or self.all_modes[0]
		self.inverse = False

		# Define lowcase commands using mapping from capital commands	
		# self.do_save = self.do_SAVE
		# self.do_catalog = self.do_CATALOG
		# self.do_unsave = self.do_UNSAVE
		# self.do_run = self.do_RUN
		# self.do_rename = self.do_RENAME
		# self.do_old = self.do_OLD
		# self.do_scratch = self.do_SCRATCH
		# self.do_nodebug = self.do_NODEBUG
		# self.do_debug = self.do_DEBUG

		# for docmd in dir( self):
		# 	if docmd.startswith("do_"):
		# 		print( docmd)
		self.do_EXIT = self.do_BYE

		"lowercase keyword will be avaiblae by mapping from uppercase to lowercase cmd"
		docmds = [docmd for docmd in dir(self) if docmd.startswith('do_')]
		# print( "Original uppercase commnds")
		# print( docmds)
		
		for docmd in docmds:
			if docmd[3:].isupper():
				exec ("self.do_%s = self.do_%s" %(docmd[3:].lower(), docmd[3:]))


		#docmds = [docmd for docmd in dir(self) if docmd.startswith('do_')]
		#print( "Remapping to lowercase commands")
		#print( docmds)

		#keyword matching is used.
		self.keywords = {'eng':[], 'kor':[], 'chn': []}
		self.keywords['eng'] = ['PRINT', 'INPUT', 'DATA', 'DEF', 'DIM', 'END', 'IF', 'FOR', 'NEXT']
		self.keywords['kor'] = ['찍어라', '넣어라', '데이타', '정의', '크기', '끝내라', '만약', '돌려라', '다음']
		self.keywords['chn'] = ['打印', '輸入', '材料', '定義', '個兒', '片尾', '万一', '期間', '下次']

def RND(n):
	"""
	RND(n):
	Generate a random float from 0 to n
	"""
	return random.random() * n

def TAB(n):
	"""
	TAB(n):
	Create a blank string n characters long
	"""
	return ' ' * n
		
if __name__ == '__main__':
	basic = BASIC()
	basic.cmdloop('APPLE ][ Compatible')
