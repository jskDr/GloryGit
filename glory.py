# -*- coding: utf-8 -*-
# Edited by Sungjin Kim (facebook.com/jamessungjin.kim)

""" 
Python Korean Basic ver.4, rev.1 (2014-12-30)
- 스페인 언어가 지원됨
- '으로 가라'에서 '으로'가 인식됨(지워짐).

Upgraded by Sungjin Kim (2014-11-27), 
This upgraded part follows MIT Licences (https://en.wikipedia.org/wiki/MIT_License).
Originated by Craig "Ichabod" O'Brien	 

Python 3.0 must be used because of on-the-fly dictionay deleting 
The base source can be founded in the following link as basic.zip
http://www.python-forum.org/viewtopic.php?f=11&t=603 
[basic.zip] http://xenomind.com/Python/basic.zip 
			written by Craig "Ichabod" O'Brien	  
Modified by Sungjin Kim (2014.11.25), https://www.facebook.com/jamessungjin.kim
- Hangul can be used as well as English for commands.
- Inverse commands can be possible soon for supporting Korean well. 

파이썬 한국어 베이직의 특징
- 영어 명령어 대신 한글 명령어를 사용할 수 있다.
- 영어 베이직 키워드 대신 한글 베이직 키워드를 사용할 수 있다.
- 영어식 문장 순서인 동사-목적어 대신 목적어-동사를 사용할 수 있다.
- 한국어에 맞도록 조사를 사용할 수 있다. (개발 진행 중)

향후 개발 계획
- 다른 언어와 호환이 되는 모드를 지원한다.
- 코드를 기본 부분과 고도화 부분을 구분한다.

"""

from __future__ import print_function

import cmd
import math
import os
import random
import re
import sys

print( '다언어 코딩언어 - 글로리 (Glory)')
try:
	import sjkim_lib
	flag_sjkim_lib = True
	print( "All rights reserved by Sungjin Kim, (c)2015")
	print( "Except the part written by Craig Ichabod O'Brien")
except ImportError:
	flag_sjkim_lib = False
	print( "Opensource - MIT License, written by Sungjin Kim(2015)")
	print( "Based on the part written by Craig Ichabod O'Brien")
	
HELP = {}
HELP_KOR = {} # 한글 버젼의 헬프를 만든다. HELP_KOR이나 도움말을 치면 나오도록 한다.
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
HELP_KOR[''] = """
파이썬 한국어 베이직에서 사용되는 명령어를 보여준다.
베이직에 사용되는 키워드를 알고 싶으면 HELP_KOR( 키워드)를 치면 된다.

도움말 (HELP_KOR): 키워드에 해당하는 도움말을 제공한다.

[내용 보기와 실행]
내용 (LIST): 현재 프로그램의 내용을 보여준다.
실행 (RUN): 현재 작성되어 있는 프로그램을 실행한다.
디버그 (DEBUG): 행번호를 보여주고 변수 상태를 확인할 수 있도록 한다.
디버그중지 (NODEBUG): 디버깅 모드를 종료한다.
종료 (BYE): 파이썬 한국어 베이직 환경을 마친다.

[목록 보기 및 처리]
신규 (NEW): 정해준 이름으로 새로운 프로그램을 시작한다.
이전 (OLD): 이전 프로그램을 불러온다.
이름 (RENAME): 현재 프로그램의 이름을 바꾼다.
목록 (CATALOG): 불러들일 수 있는 베이직 프로그램들을 보여준다.
저장 (SAVE): 신규, OLD, RENAME으로 지정된 이름으로 저장한다.
영어저장 (SAVEENG): 영어로 번역된 코드를 저장한다.
모두저장 (SAVEALL): 현재 언어 코드와 영어 번역 코드 둘다를 저장한다.
제거 (SCRATCH): 현재의 코드를 지운다.
미저장 (UNSAVE): 파일에 있는 현재의 코드를 지운다.
코드저장 (LANGSAVE): 전환된 프로그래밍 언어의 코드를 저장한다. (e.g., 파이썬) <영문식만 지원>

[언어 종류와 방식]
한글식 (INVERSE): 명령어를 뒤에서부터 해석한다 (한글 방식).
영문식 (REVERSE): 명령어를 원래처럼 앞에서부터 해석한다 (영어 방식).
방식 (MODE): 현재의 언어권 모드와 표기 방식을 보여준다. 
방식전환 (MODETO): 현재의 모드를 다른 모드로 바꾼다.
코드전환 (LANGTO): 현재 프로그래밍 언어의 코드 (e.g., 베이직)을 다른 프로그래밍 언어의 코드(e.g., 파이썬)로 전환한다. <영문식만 지원함>

[간단한 사용법]
]신규 처음프로그램
]10 "가나다"를 출력하라
]실행
가나다
]내용
10 "가나다"를 출력하라
]저장
처음프로그램이란 이름으로 저장했다.
]목록
처음프로그램
]종료
안녕~

각 명령어에 대한 세부적인 정보를 원하면 '도움말 커맨드'를 친다.
또한 '도움말 베이직'을 입력하면 베이직 키워드들을 알 수 있다.
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
FOR (~부터 ~까지 돌려라): SETS UP A LOOP WITH AN INDEX.
GOSUB (~에 갔다와라): REDIRECT PROCESSING AND REMEMBER CURRENT LINE.
GOTO (~으로 가라): REDIRECT PROCESSING.
IF ~ THEN (만약 ~이라면, ~이라면 ~으로 가기를 하라): DIVERT PROCESSING BASED ON VARIABLES.
INPUT (~에 입력하라): GETS A RESPONSE FROM THE USER.
LET (대입): ASSIGN A VALUE TO A VARIABLE.
NEXT (~의 다음): MARKS THE BOUNDARY OF A FOR LOOP.
ON (온, 수정중): GOTO BASED ON A VARIABLE VALUE.
PRINT (~을 출력하라): DISPLAY OUTPUT TO THE USER.
READ (입력하라): READ THE NEXT PIECE OF DATA.
REM (~은 주석이다): REMARK.
RETURN (돌아가라): REDIRECT PROCESSING TO A GOSUB.
STOP (중단하라): END PROCESSING.
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
HELP_KOR['베이직'] = HELP['BASIC']
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
PRINT (출력하라): DISPLAY OUTPUT TO THE USER. THE PRINT STATEMENT IS FOLLOWED BY ONE
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
		
		BASIC arrays are 1-indexed, so the Python representations are one longer
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
		elif 'to' in span: # Lower character will be working
			start, x, stop = span.partition('to')
		else:
			start, x, stop = span.partition('TO')
			
		# check for a step argument
		if '단계' in stop:
			stop, x, step = stop.partition('단계')
		elif 'step' in stop:
			stop, x, step = stop.partition('step')
		elif 'STEP' in stop:
			stop, x, step = stop.partition('STEP')
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
		# print( "[BASIC_IF]", condition, x, goto)
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
		print('? ', end="")
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
		#print( tail) #DEBUG
		# print the parts of the statement
		for group in tail.split(';'):
			if group:
				print(eval(group, self.variables), end = ' ')
		# check for retaining the line
		if tail.endswith(';'):
			print(' ', end = '')
		else:
			print()
	
	def _basic_execpy_r0(self, tail):
	       """
	       this code is moved to sjkim_lib for the future extension.
	       basic_execpy(tail)
	       exec a Python code statement
	       
	       Parameters:
	       tail: The Python statement 
	       """
	       exec( tail, self.execpy_globals) 
	
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

	def _default_r1(self, line):
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
			# I would like to use meta programming for this
			# After Korean word is changed to English word, call self.do_X( line)
			# check for program in progress
			# First, general commands are executed. 
			# Then, code is written. 
			if line == '종료':
				return self.do_BYE( None)
			elif line == '목록':
				self.do_CATALOG( None)
			elif line.split()[0].strip() == '신규': # NEW
				self.do_NEW( line.split(None, 1)[1])
			elif line.split()[0].strip() == '이전': # OLD
				self.do_OLD( line.split(None, 1)[1])
			elif line.split()[0].strip() == '디버그': # DEBUG
				self.do_DEBUG( line.split(None, 1)[1])
			elif line.split()[0].strip() == '이름변경': 
				self.do_RENAME( line.split(None, 1)[1])
			elif line.split()[0].strip() == '도움말': 
				if len(line.split()) > 1:
					self.do_HELP_KOR( line.split(None, 1)[1])
				else:
					self.do_HELP_KOR( '')
			elif line == '삭제': 
				self.do_SCRATCH( None)
			elif line == '미저장': 
				self.do_UNSAVE( None)
			elif line == '디버그오프': #NODEBUG
				self.do_NODEBUG( None)
			elif line == '저장':
				self.do_SAVE( None)
			elif line == '내용':
				self.do_LIST( None)
			elif line == '실행':
				words = line.split()
				if len(words) == 1:
					self.do_RUN( None)
				else:
					self.do_RUN( line.split(None, 1)[1])
			elif line == '인버스':
				self.do_INVERSE( None)
			elif line == '리버스':
				self.do_REVERSE( None)
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

		# I would like to use meta programming for this
		# After Korean word is changed to English word, call self.do_X( line)
		# check for program in progress
		self.commands = {'eng':[], 'kor':[]}
		self.commands['eng'].append( 'BYE'), self.commands['kor'].append( '종료')
		self.commands['eng'].append( 'NEW'), self.commands['kor'].append( '신규')
		self.commands['eng'].append( 'OLD'), self.commands['kor'].append( '이전')
		self.commands['eng'].append( 'DEBUG'), self.commands['kor'].append( '디버그')
		self.commands['eng'].append( 'RENAME'), self.commands['kor'].append( '이름변경')
		self.commands['eng'].append( 'HELP_KOR'), self.commands['kor'].append( '도움말')
		self.commands['eng'].append( 'DEBUG'), self.commands['kor'].append( '디버그')
		self.commands['eng'].append( 'NODEBUG'), self.commands['kor'].append( '디버그중지')
		self.commands['eng'].append( 'SCRATCH'), self.commands['kor'].append( '삭제')
		self.commands['eng'].append( 'UNSAVE'), self.commands['kor'].append( '미저정')
		self.commands['eng'].append( 'SAVE'), self.commands['kor'].append( '저장')
		self.commands['eng'].append( 'SAVEALL'), self.commands['kor'].append( '모두저장')
		self.commands['eng'].append( 'SAVEENG'), self.commands['kor'].append( '영어저장')
		self.commands['eng'].append( 'LIST'), self.commands['kor'].append( '내용')
		self.commands['eng'].append( 'CATALOG'), self.commands['kor'].append( '목록')
		self.commands['eng'].append( 'RUN'), self.commands['kor'].append( '실행')
		self.commands['eng'].append( 'INVERSE'), self.commands['kor'].append( '한글식')
		self.commands['eng'].append( 'REVERSE'), self.commands['kor'].append( '영문식')
		self.commands['eng'].append( 'MODE'), self.commands['kor'].append( '방식')
		self.commands['eng'].append( 'MODETO'), self.commands['kor'].append( '방식전환')
		self.commands['eng'].append( 'LANGTO'), self.commands['kor'].append( '코드전환')
		self.commands['eng'].append( 'LANGSAVE'), self.commands['kor'].append( '코드저장')
        
		cmd_tail = line.split(None, 1)
		if len( cmd_tail) > 1:
			line_tail = cmd_tail[ 1]
		else:
			line_tail = ""

		# check for valid line of BASIC code
		try:
			if cmd_tail[0] in self.commands['kor']:
				idx = self.commands['kor'].index( cmd_tail[0])
				return eval( "self.do_{}( line_tail)".format( self.commands['eng'][ idx]))
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
		if self.mode == 'kor':
			print( "안녕~")
		else:
			print( "Bye~")
		return True
	
	def _do_CATALOG_r0(self, line):
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
			#print()
			for program in programs:
				# print(program[:-4].upper())
				print(program[:-4])
			#print()
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
			print('THERE IS NO HELP FOR THAT TOPIC.')

	def do_HELP_KOR(self, line):
		"""
		do_HELP_KOR(line)
		한글로 도움말을 보여준다.
		
		Parameters:
		line: The command line entered by the user. (str)
		"""
		if line.strip() in HELP_KOR:
			print(HELP_KOR[line.strip()])
		elif line.strip() in HELP:
		        print(HELP_KOR[line.strip()])
		else:
			print('주어진 주제에 대해서는 한글 도움말이 없다.')

	
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
		to the correspoding english keyword such as print to 출력하라.
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
		to the correspoding english keyword such as print to 출력하라.
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

		# Redundant and nonintended results are prohibited as much as possible.
		#print() 
		
		for line_num in line_nums:
			print(line_num, self.code[line_num])
		
		#print()

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
		to the correspoding english keyword such as print to 출력하라.
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
		to the correspoding english keyword such as print to 출력하라.
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
		to the correspoding english keyword such as from 출력하라 to print.

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
		to the correspoding english keyword such as from 출력하라 to print.

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
		All status parameters are displayed.
		
		Parameters:
		line: The command line entered by the user. (str)
		"""
		if self.mode == 'kor':
			print( '방식: {0}, 코드: {1}, 문법: {2}'.format( self.mode, \
				self.status['lang'], '한글식' if self.inverse else '영문식'))

			print( '명령어를 알고 싶으면 도움말을 치세요.')
		else: 
			print( 'Global Programming Language (Glory)')
			print( '[Status - MODE]')
			print( 'All supported modes: {}'.format( ', '.join(self.all_modes)))
			print( 'Current mode: ', self.mode)

			print( '[Status - STYLE]')
			print( 'All supported styles: {}'.format( 'English (Reverse), Korean (Inverse)'))
			print( 'Current style: ',  'inverse' if self.inverse else 'reverse')
		
			print( '[Status - LANG]')
			print( 'All supported languages: {}'.format( ','.join(self.status['all_langs'])))
			print( 'Current language: {}'.format( self.status['lang']))

			print( 'Type HELP for manual.')
		
	def do_MODETO( self, line):
		"""
		do_MOTETO( line)
		The mode is changed to new mode.

		Parameters:
		line: The new mode is entered by an user.
		"""

		if line in self.all_modes:
			print( 'The mode is changed from {0} to {1}.'.format(self.mode, line))

			# A translated codes will be shown. 
			# Real translation processing will be applied
			# Mode mapping tool is used by dictionary.	  
			print( 'The translated code is as follows:')

			self.Mode_Change_LEFT( self.mode_map[self.mode], self.mode_map[line])
			self.mode = line	
		else:
			print( 'Type valild modes in [{}]'.format( ', '.join( self.all_modes)))

	def Mode_Change_LEFT(self, lang1, lang2):
		"""
		_do_LIST_ENG_LEFT(line)
		Handle requests to print the program.
		If hangul keyword is finding, it is changed 
		to the correspoding english keyword such as print to 출력하라.
		* do_LIST_ENG calls do_LIST_ENG_LEFT or LIST_ENG_RIGHT
		  depeding on self.inverse flag.
		  Then, do_LIST_ENG_LEFT will be moved to _do_LIST_ENG_LEFT for hiddening.

		Parameters:
		line: The command line entered by the user. (str)
		"""
		# print the lines in order
		line_nums = sorted(self.code.keys())
		print()
		print('Translation is processing from {0} to {1}'.format( lang1, lang2))
		for line_num in line_nums:
			# In the mode change, no language translation is processed.
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
			
			#list.index can be used
			mult_cmds = [ ['IF', 'THEN'], ['FOR', 'TO', 'STEP']]
			for mc in mult_cmds:
				if basic_cmd == self.mc_lang(mc[0], lang2):
					for mcc in mc[1:]:
						m1 = self.mc_lang(mcc, lang1)
						m2 = self.mc_lang(mcc, lang2)
						basic_tail = basic_tail.replace( m1, m2)

			print(line_num, basic_cmd, basic_tail)
			# The code is also changed to the new mode language
			self.code[line_num] = " ".join( [basic_cmd, basic_tail])
		print()

	def do_LANGTO( self, line):
		"""
		do_LANGTO( line)
		The current language (e.g., basic) codes are changed to the target language (python) codes.

		Parameters:
		line: The new mode is entered by an user.
		"""

		if line in self.status['all_langs']:
			print( 'The Lang is changed from {0} to {1}.'.format(self.status['lang'], line))

			# A translated codes will be shown. 
			# Real translation processing will be applied
			# Mode mapping tool is used by dictionary.	  
			print( 'The translated code is as follows:')

			self.Lang_Change_LEFT( self.status['lang'], line)
			self.lang = line	
		else:
			print( 'Type valild Lang in [{}]'.format( ', '.join( self.status['all_langs'])))

	def _Lang_Change_LEFT_r0(self, plang1, plang2):
		"""
		_do_LIST_ENG_LEFT(line)
		Handle requests to print the program.
		If hangul keyword is finding, it is changed 
		to the correspoding english keyword such as print to 출력하라.
		* do_LIST_ENG calls do_LIST_ENG_LEFT or LIST_ENG_RIGHT
		  depeding on self.inverse flag.
		  Then, do_LIST_ENG_LEFT will be moved to _do_LIST_ENG_LEFT for hiddening.

		Parameters:
		line: The command line entered by the user. (str)
		"""
		# print the lines in order
		# print( plang1, plang2, 'etc.')
		# print( '==={}==='.format( plang2))
		
		# if plang1 is not 'basic':
			# print( 'plang1 is not basic')
		# if plang2 != 'python':
			# print( 'plang2 is not python')
		
		if (plang1 != 'basic') or (plang2 != 'python'):
			print( "Translation from {plang1} to {plang2} is not supported".format(**vars()))
			print( "Only basic to python translation is supported now!")
			print( "The other cases will be supported later as plug-in types.")
		
		line_nums = sorted(self.code.keys())
		#print()
		#print('Translation is processing from {0} to {1}'.format( plang1, plang2))
		self.lang_code = {}
		for line_num in line_nums:
			# In the mode change, no language translation is processed.
			basic_cmd, basic_tail = self.line_split(self.code[line_num])
			#The original statement is shown for reference.
			# print('[ORG]', line_num, basic_cmd, basic_tail)
			
			if basic_cmd == 'PRINT':
				# self.lang_code[ line_num] = 'print( {})'.format( basic_tail)
				self.lang_code[ line_num] = self.trans_print( basic_tail)
			elif '=' in basic_tail or '=' in basic_cmd:
				self.lang_code[ line_num] = self.code[line_num]
		
		#print( "Translation results:");
		for line_num in line_nums:
			print( self.lang_code[ line_num])
		
		print()

	def Lang_Change_LEFT(self, plang1, plang2):
		"""
		_do_LIST_ENG_LEFT(line)
		Handle requests to print the program.
		If hangul keyword is finding, it is changed 
		to the correspoding english keyword such as print to 출력하라.
		* do_LIST_ENG calls do_LIST_ENG_LEFT or LIST_ENG_RIGHT
		  depeding on self.inverse flag.
		  Then, do_LIST_ENG_LEFT will be moved to _do_LIST_ENG_LEFT for hiddening.

		Parameters:
		line: The command line entered by the user. (str)
		"""
		# print the lines in order
		# print( plang1, plang2, 'etc.')
		# print( '==={}==='.format( plang2))
		
		# if plang1 is not 'basic':
			# print( 'plang1 is not basic')
		# if plang2 != 'python':
			# print( 'plang2 is not python')
		
		if (plang1 != 'basic') or (plang2 != 'python'):
			print( "Translation from {plang1} to {plang2} is not supported".format(**vars()))
			print( "Only basic to python translation is supported now!")
			print( "The other cases will be supported later as plug-in types.")

		if flag_sjkim_lib: 
			self.lang_code = sjkim_lib.transpile( self)
		else:
			print( 'Code transpile is not supported.')
		
	def trans_print(self, tail):
		"""
		basic_print(tail)
		Handle output to the user.
		
		Parameters:
		tail: The tail of the BASIC command.
		"""
		#print( tail) #DEBUG
		# print the parts of the statement
		out_str_each = []
		for group in tail.split(';'):
			if group:
				out_str_each.append( group)
		out_str = ','.join( out_str_each)
		# check for retaining the line
		if tail.endswith(';'):
			out_str = "print( {}, end = ' ')".format( out_str)
		else:
			out_str = "print( {})".format( out_str)

		return out_str
		
	def mc_lang_inv( self, cmd, lang):
		"""
		The corresponding english keyword is returned.
		"""
		try:
			idx = self.keywords[ lang].index(cmd)
			return self.keywords[ 'eng'][ idx]
		except ValueError:
			return cmd

	def mct_processing( self, cmd, tail, lang1, lang2):
		"""
		It is half-functinoal code, which uses self.func but no self.var.
		"""
		#list.index can be used
		mult_cmds = [ ['IF', 'THEN'], ['FOR', 'TO', 'STEP']]
		for mc in mult_cmds:
			mc_cmd = mc[0]
			mc_app = mc[1:]
			# Already, cmd is translated.
			if cmd == self.mc_lang(mc_cmd, lang2):				  
				for mcc in mc_app:
					m1 = self.mc_lang(mcc, lang1)
					m2 = self.mc_lang(mcc, lang2)
					tail = tail.replace( m1, m2)
		return tail

	def mct_lang_inv( self, cmd, tail, lang):
		""" line_tail = self.mct_lang_inv( line_cmd, line_tail, lang) """
		return self.mct_processing( cmd, tail, lang, 'eng')

	def mc_lang( self, cmd, lang):
		"""
		The required language keyword is returned.
		"""
		idx = self.keywords[ 'eng'].index(cmd)
		return self.keywords[ lang][ idx]

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
		# execpy의 글로벌 변수를 {}로 셋팅한다.
		#    그렇지 않으면 이전에 실행했던 변수들이 저장된다. 
		self.execpy_globals = {}
		try:
			# loop through the basic code lines
			while pointer < len(line_nums):
				# update line tracking
				line_num = line_nums[pointer]
				basic_cmd, basic_tail = self.line_split_langtrans(self.code[line_num])
				# print( line_num, basic_cmd, basic_tail) #DEBUG

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
				elif basic_cmd == 'EXECPY' or basic_cmd == '실행하라':					
					# self._basic_execpy_r0( basic_tail)
					if flag_sjkim_lib: 
						sjkim_lib.execpy(self, basic_tail)
					else:
						print( 'EXECPY is not supported.')

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
				elif basic_cmd == 'INPUT' or basic_cmd == '입력하라':
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
				elif basic_cmd == 'PRINT' or basic_cmd == '출력하라':
					self.basic_print(basic_tail)
				elif basic_cmd == 'READ' or basic_cmd == '입력하라':
					exec('{} = {}'.format(basic_tail, data.pop(0)), self.variables)
				elif basic_cmd == 'REM' or basic_cmd == '주석':
					pass
				elif basic_cmd == 'RETURN' or basic_cmd == '돌려주라':
					pointer = gosubs.pop()
				elif basic_cmd == 'STOP' or basic_cmd == '끝내라':
					break
				elif '=' in basic_tail or '=' in basic_cmd:
					basic_cmd_tail = basic_cmd + ' ' + basic_tail
					# exec( basic_cmd_tail, self.variables) # 소문자 -> 대문자, 인버스 오류  
					exec(self.code[line_num], self.variables) # 소문자 처리 불가 
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
		#print()
	
	def _do_SAVE_r1(self, line):
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
			if self.mode == 'kor':
				print('{}이란 이름으로 내용을 저장했다.'.format(self.code_name))
			else:
				print('SAVED PROGRAM {}'.format(self.code_name))
		else:
			if self.mode == 'kor':
				print('내용을 저장하지 못했다.')
			else:
				print('NO PROGRAM TO SAVE')			
			
	def do_LANGSAVE(self, line):
		"""
		do_SAVE(line)
		Handle requests to save the current program
		
		Parameters:
		line: The command line entered by the user. (str)
		"""
		# check for program to save
		if self.code_name:
			# write out code lines in order
			line_nums = sorted(self.lang_code.keys())
			program_file = open(self.code_name + '.py', 'w')
			for line_num in line_nums:
				line_text = '{}\n'.format(self.lang_code[line_num])
				program_file.write(line_text)
			print('\nSAVED LANG PROGRAM {}\n'.format(self.code_name))
		else:
			print('\nNO LANG PROGRAM TO SAVE\n')			
	

	def do_SAVEENG(self, line):
		if self.code_name:
			self.do_MODETO( 'eng')
			org_code_name = self.code_name
			self.code_name = self.code_name + '_eng'
			self.do_SAVE( line)
			self.code_name = org_code_name

	def do_SAVEALL(self, line):
		"""
		do_SAVEALL(line)
		Handle requests to save the current program and
		the compiled program in English
		
		Parameters:
		line: The command line entered by the user. (str)
		"""
		# check for program to save
		if self.code_name:
			self.do_SAVE( line)
			self.do_SAVEENG( line)

			
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
			
	def line_split_langtrans(self, line):
		"""
		line_rsplit(line)
		Language translation is considered.
		
		Parameters:
		line: A line of BASIC code. (str)
		"""

		line_cmd, line_tail = self.line_split(line)
		# print( line_cmd, line_tail) #DEBUG
		lang = self.mode_map[ self.mode]
		line_cmd = self.mc_lang_inv( line_cmd, lang)
		line_tail = self.mct_lang_inv( line_cmd, line_tail, lang)
		
		if self.debug is True:
			if '=' in line_cmd or '=' in line_tail:
				print( "[Trans-pile]", line) 
			else:
				print( "[Trans-pile]", line_cmd, line_tail) 

		# print('[Temporary - Runtime translation result]')
		# print( line_cmd, line_tail)

		return line_cmd, line_tail
	
	def line_split(self, line):
		"""
		line_rsplit_nolangtrans(line)
		Split left or right depending on self.inverse
		Language translation is not considered.
		
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
					# line_tail += part.upper()
					line_tail += part # 변수의 소대문자 구분하도록 함.
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
					# line_tail += part.upper()
					line_tail += part # 변수의 소대문자 구분하도록 함.
		except IndexError:
			# blank tail for parameterless commands
			line_cmd = line.rsplit(None, 1)[0].upper()
			line_tail = ''

		line_tail = self.rsplit_tail_add( line_cmd, line_tail)
		# Special processing for if(만약) in the inverse mode
		if line_cmd == '하라':
			line_cmd = '만약'
		
		return line_cmd, line_tail

	def rsplit_tail_add( self, cmd, tail):
		"""
		In korean inverse mode, if the last tail is special
		it is removed for interpreting. 
		Note that this processing is invoked for korean inverse mode only.

		Parameters:
		cmd: line_cmd
		tail: line_tail
		"""
		add_dict = {}
		add_dict['출력하라'] = ['을', '를']
		add_dict['입력하라'] = ['에']
		add_dict['가라'] = ['으로']
		add_dict['갔다와라'] = ['에']
		add_dict['돌려라'] = ['까지']
		add_dict['다음'] = ['의']
		add_dict['하라'] = ['으로 가기를']
		add_dict['주석이다'] = ['은', '는']
		add_dict['실행하라'] = ['을', '를']

		for each_cmd in add_dict.keys():
			if cmd == each_cmd:
				# 어미를 처리한다. 사실 지우는 형태이다.
				for each_tail in add_dict[ each_cmd]:
					if tail.endswith( each_tail):
						ln = len( each_tail)
						tail = tail[:-ln]
						# if both included, only the first is removed
						#print( 'Tail is changed to {0} by {1}'.format( tail, each_tail))
						break
		return tail

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
		self.execpy_globals = {}	   
		"Code will be read from the stat point."
		
		"Set up modes"
		self.all_modes = ['eng_kor_mixed', 'eng', 'kor', 'kor_inv', 'chn', 'spn']
		self.mode = 'kor' # or self.all_modes[0]
		#self.mode2ls = {'eng_kor_mixed':'eng', 'eng':'eng', 'kor':'kor', 'kor_inv':'kor', 'chn':'chn'}
		self.inverse = True

		"One command for exiting is added."
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
		self.keywords = {'eng':[], 'kor':[], 'chn': [], 'spn': []}
		self.keywords['eng'] = ['PRINT', 'INPUT', 'DATA', 'DEF', 'DIM', 'END', 'STOP', 'RETURN',\
								'IF', 'FOR', 'NEXT', 'GOTO', 'GOSUB', 'THEN', 'TO', 'STEP',\
                                        'REM', 'EXECPY']
		self.keywords['kor'] = ['출력하라', '입력하라', '데이타', '정의', '크기', '끝내라', '중단하라', '돌아가라',\
								'만약', '돌려라', '다음', '가라', '갔다와라', '이라면', '부터', '단계',\
                                        '주석이다', '실행하라']
		self.keywords['chn'] = ['打印', '輸入', '材料', '定義', '個兒', '片尾', '中斷', '回到原地',\
								'万一', '期間', '下次', '走', '來往', '那时', '到', '階段',\
                                        '주석', '실행하라']
		self.keywords['spn'] = ['IMPRIMIR' , 'ENTRADA' , 'DATOS' , 'DEFINIR ', 'DIM ', 'ACABADO', 'DETÉNGASE', 'RETORNO',\
								'SI', 'PARA', 'SIGUIENTE', 'IRA', 'IRSUB', 'ENTONCES', 'A', 'PASO',\
                                        '주석', '실행하라']
								
		"We will show the current mode and some initial conditions if any."
		self.mode_map = {'eng_kor_mixed': 'eng', 'kor': 'kor', \
					'eng': 'eng' , 'kor_inv': 'kor', \
					'chn': 'chn', 'spn': 'spn'}
		
		"Setting Langs"
		# self.lang_code = {}
		self.status = {'all_langs': [], 'lang': None, \
							'all_modes': [], 'mode': None, \
							'all_flags': [], 'flag': None}
		self.status['all_langs'] = ['basic', 'python']
		self.status['lang'] = 'basic'
		
		self.do_MODE( None)
		print('')

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
