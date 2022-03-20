
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftDOTleftPLUSMINUSleftTIMESDIVIDEleftEEQUALrightUMINUSAGENTATTRSET AGENTSET ALL BEGIN BEHAVIOUR BUT COLON COMMA DIVIDE DOT EEQUAL ELSE END ENVIRONMENT EQUAL FALSE FILTER FOR FUNCTION GT IF IMPORT INSTANCE LIST LPAREN LT MINIMUM MINUS MODEL NAME NEQUAL NONE NULL NUMBER ONE PIPE PLUS PYTHONLINK RETURN ROLES ROLESET RPAREN SEMICOLON SET STRING SUBL SUBR TIMES TRUE VAR WHILE WITH nONE nULL program : headers b_bodies  program : headers  headers : header  headers : header headers  header : agent_model  header : role_set  header : agent_set  header : agent_attr_set  header : environment_def  header : assign SEMICOLON  header : IMPORT STRING SEMICOLON  agent_model : MODEL STRING SEMICOLON  role_set : ROLESET LPAREN role_set_statement RPAREN SEMICOLON  role_set_statement : role_set_statement COMMA  role_def  role_set_statement : role_def  role_def : BEGIN nameval_pairs END  agent_set : AGENTSET LPAREN role_set_statement RPAREN SEMICOLON  agent_attr_set : AGENTATTRSET literal_list_set_statement SEMICOLON  environment_def : ENVIRONMENT LPAREN role_def RPAREN SEMICOLON literal_list_set_statement : LPAREN literal_list RPARENliteral_list : NAME COMMA literal_listliteral_list : NAME b_bodies : b_bodies b_body  b_bodies : b_body  b_body : behaviour_def\n               | function_def  behaviour_def : BEHAVIOUR NAME BEGIN with_list END function_def : FUNCTION NAME LPAREN names_list RPAREN BEGIN statements END function_def : FUNCTION LPAREN names_list RPAREN BEGIN statements END names_list : NAME COMMA names_list  names_list : NAME  assign : VAR NAME EQUAL expr  assign : NAME EQUAL expr  assign : VAR NAME  assign : NAME DOT NAME EQUAL expr  assign : increment  with_list : with_list with_block  with_list : with_block  with_block : WITH with_set BEGIN statements END  with_block : WITH with_set BEGIN statements END PIPE  with_set : with_set DOT with_set  with_set : ALL  with_set : ONE  with_set : ROLES LPAREN string_list RPAREN  with_set : BUT LPAREN expr RPAREN  with_set : MINIMUM LPAREN function_def RPAREN  with_set : FILTER LPAREN function_def RPAREN  string_list : STRING  string_list : string_list COMMA STRING  statements : statements statement  statements : statement  statement : assign SEMICOLON\n                  | proccall\n                  | methcall\n                  | returnstmt\n                  | if_block\n                  | for_block\n                  | while_block proccall : NAME list_set_statement SEMICOLON  methcall : NAME DOT NAME list_set_statement SEMICOLON  returnstmt : RETURN expr SEMICOLON  if_block : IF LPAREN expr RPAREN then_else_statement  if_block : IF LPAREN expr RPAREN then_else_statement ELSE then_else_statement then_else_statement : statement  then_else_statement : BEGIN statements END  while_block : WHILE LPAREN expr RPAREN then_else_statement  for_block : FOR LPAREN assign SEMICOLON expr SEMICOLON assign RPAREN then_else_statement increment : PLUS PLUS NAMEincrement : NAME PLUS PLUSexpr : INSTANCE NAME expr : MINUS expr %prec UMINUSexpr : expr PLUS exprexpr : expr MINUS exprexpr : expr TIMES exprexpr : expr DIVIDE exprexpr : expr EEQUAL exprexpr : expr NEQUAL exprexpr : expr LT exprexpr : expr GT exprexpr : LPAREN expr RPARENexpr : SET list_set_statementexpr : LIST list_set_statementlist_set_statement : LPAREN RPARENlist_set_statement : LPAREN set_expr_list RPARENset_expr_list : expr COMMA set_expr_listset_expr_list : exprexpr : BEGIN nameval_pairs END nameval_pairs : nameval_pairs COMMA nameval_pair  nameval_pairs : nameval_pair  nameval_pair : NAME COLON expr  expr : PYTHONLINK STRING  expr : NAME DOT with_set  expr : NAME DOT NAME  expr : NAME list_set_statement  expr : NAME DOT NAME list_set_statement expr : with_setexpr : NAME SUBL expr SUBRexpr : NAMEexpr : NUMBERexpr : STRINGexpr : function_defexpr : nONEexpr : NONEexpr : nULLexpr : NULLexpr : TRUEexpr : FALSE'
    
_lr_action_items = {'IMPORT':([0,3,4,5,6,7,8,27,44,45,50,128,133,135,],[10,10,-5,-6,-7,-8,-9,-10,-11,-12,-18,-13,-17,-19,]),'MODEL':([0,3,4,5,6,7,8,27,44,45,50,128,133,135,],[11,11,-5,-6,-7,-8,-9,-10,-11,-12,-18,-13,-17,-19,]),'ROLESET':([0,3,4,5,6,7,8,27,44,45,50,128,133,135,],[12,12,-5,-6,-7,-8,-9,-10,-11,-12,-18,-13,-17,-19,]),'AGENTSET':([0,3,4,5,6,7,8,27,44,45,50,128,133,135,],[13,13,-5,-6,-7,-8,-9,-10,-11,-12,-18,-13,-17,-19,]),'AGENTATTRSET':([0,3,4,5,6,7,8,27,44,45,50,128,133,135,],[14,14,-5,-6,-7,-8,-9,-10,-11,-12,-18,-13,-17,-19,]),'ENVIRONMENT':([0,3,4,5,6,7,8,27,44,45,50,128,133,135,],[15,15,-5,-6,-7,-8,-9,-10,-11,-12,-18,-13,-17,-19,]),'VAR':([0,3,4,5,6,7,8,27,44,45,50,128,133,135,163,176,177,178,179,181,182,183,184,185,186,194,195,197,198,203,208,209,215,217,218,219,220,221,223,224,225,226,227,228,230,231,],[16,16,-5,-6,-7,-8,-9,-10,-11,-12,-18,-13,-17,-19,16,16,16,16,-51,-53,-54,-55,-56,-57,-58,16,16,-50,-52,16,-59,-61,16,16,-60,-62,-64,16,-66,16,16,16,-63,-65,16,-67,]),'NAME':([0,3,4,5,6,7,8,16,24,25,27,33,36,37,39,43,44,45,48,50,54,57,58,59,62,84,94,97,99,100,101,102,103,104,105,106,107,108,118,121,127,128,131,132,133,135,163,170,176,177,178,179,181,182,183,184,185,186,188,194,195,197,198,199,202,203,204,208,209,215,216,217,218,219,220,221,223,224,225,226,227,228,230,231,],[17,17,-5,-6,-7,-8,-9,35,41,42,-10,52,55,80,82,86,-11,-12,91,-18,55,109,55,55,91,86,52,136,55,55,55,55,55,55,55,55,55,55,55,55,86,-13,91,55,-17,-19,187,55,187,187,187,-51,-53,-54,-55,-56,-57,-58,55,187,187,-50,-52,207,55,17,55,-59,-61,187,55,187,-60,-62,-64,187,-66,187,187,17,-63,-65,187,-67,]),'PLUS':([0,3,4,5,6,7,8,17,19,27,38,44,45,50,55,56,64,65,66,67,68,69,70,71,72,73,74,75,96,98,109,110,111,112,113,115,128,133,135,136,137,138,139,141,142,143,144,145,146,147,148,149,150,151,152,155,158,163,166,167,168,169,171,173,174,175,176,177,178,179,181,182,183,184,185,186,187,194,195,196,197,198,201,203,206,208,209,210,212,215,217,218,219,220,221,222,223,224,225,226,227,228,230,231,],[19,19,-5,-6,-7,-8,-9,38,39,-10,81,-11,-12,-18,-98,101,-100,-96,-99,-101,-102,-103,-104,-105,-106,-107,-42,-43,101,-94,-70,-71,101,-81,-82,-91,-13,-17,-19,-93,-92,101,-83,101,-72,-73,-74,-75,-76,101,101,101,-80,-87,-41,101,101,19,101,-95,-97,-84,-44,-45,-46,-47,19,19,19,-51,-53,-54,-55,-56,-57,-58,38,19,19,-29,-50,-52,101,19,-28,-59,-61,101,101,19,19,-60,-62,-64,19,101,-66,19,19,19,-63,-65,19,-67,]),'$end':([1,2,3,4,5,6,7,8,20,21,22,23,26,27,40,44,45,50,128,133,135,159,196,206,],[0,-2,-3,-5,-6,-7,-8,-9,-1,-24,-25,-26,-4,-10,-23,-11,-12,-18,-13,-17,-19,-27,-29,-28,]),'BEHAVIOUR':([2,3,4,5,6,7,8,20,21,22,23,26,27,40,44,45,50,128,133,135,159,196,206,],[24,-3,-5,-6,-7,-8,-9,24,-24,-25,-26,-4,-10,-23,-11,-12,-18,-13,-17,-19,-27,-29,-28,]),'FUNCTION':([2,3,4,5,6,7,8,20,21,22,23,26,27,36,40,44,45,50,54,58,59,99,100,101,102,103,104,105,106,107,108,118,119,120,121,128,132,133,135,159,170,188,196,202,204,206,216,],[25,-3,-5,-6,-7,-8,-9,25,-24,-25,-26,-4,-10,25,-23,-11,-12,-18,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,-13,25,-17,-19,-27,25,25,-29,25,25,-28,25,]),'SEMICOLON':([9,18,28,29,32,35,55,56,64,65,66,67,68,69,70,71,72,73,74,75,81,82,87,92,93,95,96,98,109,110,112,113,115,136,137,139,142,143,144,145,146,147,148,149,150,151,152,158,167,168,169,171,173,174,175,180,196,200,201,206,211,214,222,],[27,-36,44,45,50,-34,-98,-33,-100,-96,-99,-101,-102,-103,-104,-105,-106,-107,-42,-43,-69,-68,128,133,-20,135,-32,-94,-70,-71,-81,-82,-91,-93,-92,-83,-72,-73,-74,-75,-76,-77,-78,-79,-80,-87,-41,-35,-95,-97,-84,-44,-45,-46,-47,198,-29,208,209,-28,216,218,226,]),'STRING':([10,11,36,54,58,59,63,99,100,101,102,103,104,105,106,107,108,117,118,121,132,170,172,188,202,204,216,],[28,29,64,64,64,64,115,64,64,64,64,64,64,64,64,64,64,154,64,64,64,64,193,64,64,64,64,]),'LPAREN':([12,13,14,15,25,36,42,54,55,58,59,60,61,76,77,78,79,99,100,101,102,103,104,105,106,107,108,118,121,132,136,170,187,188,189,190,191,202,204,207,216,],[30,31,33,34,43,59,84,59,100,59,59,100,100,117,118,119,120,59,59,59,59,59,59,59,59,59,59,59,59,59,100,59,100,59,202,203,204,59,59,100,59,]),'EQUAL':([17,35,80,187,207,],[36,54,121,36,121,]),'DOT':([17,55,65,74,75,137,152,161,171,173,174,175,187,],[37,97,116,-42,-43,116,-41,116,-44,-45,-46,-47,199,]),'RPAREN':([18,35,46,47,49,51,52,53,55,56,64,65,66,67,68,69,70,71,72,73,74,75,81,82,85,86,96,98,100,109,110,111,112,113,115,125,129,130,134,136,137,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,164,167,168,169,171,173,174,175,192,193,196,206,210,212,229,],[-36,-34,87,-15,92,93,-22,95,-98,-33,-100,-96,-99,-101,-102,-103,-104,-105,-106,-107,-42,-43,-69,-68,126,-31,-32,-94,139,-70,-71,150,-81,-82,-91,162,-14,-16,-21,-93,-92,-83,169,-86,-72,-73,-74,-75,-76,-77,-78,-79,-80,-87,-41,171,-48,173,174,175,-35,-30,-95,-97,-84,-44,-45,-46,-47,-85,-49,-29,-28,215,217,230,]),'BEGIN':([30,31,34,36,41,54,58,59,74,75,88,99,100,101,102,103,104,105,106,107,108,118,121,126,132,152,161,162,170,171,173,174,175,188,202,204,215,216,217,224,230,],[48,48,48,62,83,62,62,62,-42,-43,48,62,62,62,62,62,62,62,62,62,62,62,62,163,62,-41,176,177,62,-44,-45,-46,-47,62,62,62,221,62,221,221,221,]),'INSTANCE':([36,54,58,59,99,100,101,102,103,104,105,106,107,108,118,121,132,170,188,202,204,216,],[57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,]),'MINUS':([36,54,55,56,58,59,64,65,66,67,68,69,70,71,72,73,74,75,96,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,115,118,121,132,136,137,138,139,141,142,143,144,145,146,147,148,149,150,151,152,155,158,166,167,168,169,170,171,173,174,175,188,196,201,202,204,206,210,212,216,222,],[58,58,-98,102,58,58,-100,-96,-99,-101,-102,-103,-104,-105,-106,-107,-42,-43,102,-94,58,58,58,58,58,58,58,58,58,58,-70,-71,102,-81,-82,-91,58,58,58,-93,-92,102,-83,102,-72,-73,-74,-75,-76,102,102,102,-80,-87,-41,102,102,102,-95,-97,-84,58,-44,-45,-46,-47,58,-29,102,58,58,-28,102,102,58,102,]),'SET':([36,54,58,59,99,100,101,102,103,104,105,106,107,108,118,121,132,170,188,202,204,216,],[60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,]),'LIST':([36,54,58,59,99,100,101,102,103,104,105,106,107,108,118,121,132,170,188,202,204,216,],[61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,]),'PYTHONLINK':([36,54,58,59,99,100,101,102,103,104,105,106,107,108,118,121,132,170,188,202,204,216,],[63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,]),'NUMBER':([36,54,58,59,99,100,101,102,103,104,105,106,107,108,118,121,132,170,188,202,204,216,],[66,66,66,66,66,66,66,66,66,66,66,66,66,66,66,66,66,66,66,66,66,66,]),'nONE':([36,54,58,59,99,100,101,102,103,104,105,106,107,108,118,121,132,170,188,202,204,216,],[68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,]),'NONE':([36,54,58,59,99,100,101,102,103,104,105,106,107,108,118,121,132,170,188,202,204,216,],[69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,]),'nULL':([36,54,58,59,99,100,101,102,103,104,105,106,107,108,118,121,132,170,188,202,204,216,],[70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,]),'NULL':([36,54,58,59,99,100,101,102,103,104,105,106,107,108,118,121,132,170,188,202,204,216,],[71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,]),'TRUE':([36,54,58,59,99,100,101,102,103,104,105,106,107,108,118,121,132,170,188,202,204,216,],[72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,]),'FALSE':([36,54,58,59,99,100,101,102,103,104,105,106,107,108,118,121,132,170,188,202,204,216,],[73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,]),'ALL':([36,54,58,59,97,99,100,101,102,103,104,105,106,107,108,116,118,121,124,132,170,188,202,204,216,],[74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,]),'ONE':([36,54,58,59,97,99,100,101,102,103,104,105,106,107,108,116,118,121,124,132,170,188,202,204,216,],[75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,]),'ROLES':([36,54,58,59,97,99,100,101,102,103,104,105,106,107,108,116,118,121,124,132,170,188,202,204,216,],[76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,]),'BUT':([36,54,58,59,97,99,100,101,102,103,104,105,106,107,108,116,118,121,124,132,170,188,202,204,216,],[77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,]),'MINIMUM':([36,54,58,59,97,99,100,101,102,103,104,105,106,107,108,116,118,121,124,132,170,188,202,204,216,],[78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,]),'FILTER':([36,54,58,59,97,99,100,101,102,103,104,105,106,107,108,116,118,121,124,132,170,188,202,204,216,],[79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,79,]),'COMMA':([46,47,49,52,55,64,65,66,67,68,69,70,71,72,73,74,75,86,89,90,98,109,110,112,113,114,115,129,130,136,137,139,141,142,143,144,145,146,147,148,149,150,151,152,153,154,165,166,167,168,169,171,173,174,175,193,196,206,],[88,-15,88,94,-98,-100,-96,-99,-101,-102,-103,-104,-105,-106,-107,-42,-43,127,131,-89,-94,-70,-71,-81,-82,131,-91,-14,-16,-93,-92,-83,170,-72,-73,-74,-75,-76,-77,-78,-79,-80,-87,-41,172,-48,-88,-90,-95,-97,-84,-44,-45,-46,-47,-49,-29,-28,]),'SUBL':([55,],[99,]),'TIMES':([55,56,64,65,66,67,68,69,70,71,72,73,74,75,96,98,109,110,111,112,113,115,136,137,138,139,141,142,143,144,145,146,147,148,149,150,151,152,155,158,166,167,168,169,171,173,174,175,196,201,206,210,212,222,],[-98,103,-100,-96,-99,-101,-102,-103,-104,-105,-106,-107,-42,-43,103,-94,-70,-71,103,-81,-82,-91,-93,-92,103,-83,103,103,103,-74,-75,-76,103,103,103,-80,-87,-41,103,103,103,-95,-97,-84,-44,-45,-46,-47,-29,103,-28,103,103,103,]),'DIVIDE':([55,56,64,65,66,67,68,69,70,71,72,73,74,75,96,98,109,110,111,112,113,115,136,137,138,139,141,142,143,144,145,146,147,148,149,150,151,152,155,158,166,167,168,169,171,173,174,175,196,201,206,210,212,222,],[-98,104,-100,-96,-99,-101,-102,-103,-104,-105,-106,-107,-42,-43,104,-94,-70,-71,104,-81,-82,-91,-93,-92,104,-83,104,104,104,-74,-75,-76,104,104,104,-80,-87,-41,104,104,104,-95,-97,-84,-44,-45,-46,-47,-29,104,-28,104,104,104,]),'EEQUAL':([55,56,64,65,66,67,68,69,70,71,72,73,74,75,96,98,109,110,111,112,113,115,136,137,138,139,141,142,143,144,145,146,147,148,149,150,151,152,155,158,166,167,168,169,171,173,174,175,196,201,206,210,212,222,],[-98,105,-100,-96,-99,-101,-102,-103,-104,-105,-106,-107,-42,-43,105,-94,-70,-71,105,-81,-82,-91,-93,-92,105,-83,105,105,105,105,105,-76,105,105,105,-80,-87,-41,105,105,105,-95,-97,-84,-44,-45,-46,-47,-29,105,-28,105,105,105,]),'NEQUAL':([55,56,64,65,66,67,68,69,70,71,72,73,74,75,96,98,109,110,111,112,113,115,136,137,138,139,141,142,143,144,145,146,147,148,149,150,151,152,155,158,166,167,168,169,171,173,174,175,196,201,206,210,212,222,],[-98,106,-100,-96,-99,-101,-102,-103,-104,-105,-106,-107,-42,-43,106,-94,-70,-71,106,-81,-82,-91,-93,-92,106,-83,106,-72,-73,-74,-75,-76,106,106,106,-80,-87,-41,106,106,106,-95,-97,-84,-44,-45,-46,-47,-29,106,-28,106,106,106,]),'LT':([55,56,64,65,66,67,68,69,70,71,72,73,74,75,96,98,109,110,111,112,113,115,136,137,138,139,141,142,143,144,145,146,147,148,149,150,151,152,155,158,166,167,168,169,171,173,174,175,196,201,206,210,212,222,],[-98,107,-100,-96,-99,-101,-102,-103,-104,-105,-106,-107,-42,-43,107,-94,-70,-71,107,-81,-82,-91,-93,-92,107,-83,107,-72,-73,-74,-75,-76,107,107,107,-80,-87,-41,107,107,107,-95,-97,-84,-44,-45,-46,-47,-29,107,-28,107,107,107,]),'GT':([55,56,64,65,66,67,68,69,70,71,72,73,74,75,96,98,109,110,111,112,113,115,136,137,138,139,141,142,143,144,145,146,147,148,149,150,151,152,155,158,166,167,168,169,171,173,174,175,196,201,206,210,212,222,],[-98,108,-100,-96,-99,-101,-102,-103,-104,-105,-106,-107,-42,-43,108,-94,-70,-71,108,-81,-82,-91,-93,-92,108,-83,108,-72,-73,-74,-75,-76,108,108,108,-80,-87,-41,108,108,108,-95,-97,-84,-44,-45,-46,-47,-29,108,-28,108,108,108,]),'SUBR':([55,64,65,66,67,68,69,70,71,72,73,74,75,98,109,110,112,113,115,136,137,138,139,142,143,144,145,146,147,148,149,150,151,152,167,168,169,171,173,174,175,196,206,],[-98,-100,-96,-99,-101,-102,-103,-104,-105,-106,-107,-42,-43,-94,-70,-71,-81,-82,-91,-93,-92,168,-83,-72,-73,-74,-75,-76,-77,-78,-79,-80,-87,-41,-95,-97,-84,-44,-45,-46,-47,-29,-28,]),'END':([55,64,65,66,67,68,69,70,71,72,73,74,75,89,90,98,109,110,112,113,114,115,122,123,136,137,139,142,143,144,145,146,147,148,149,150,151,152,160,165,166,167,168,169,171,173,174,175,178,179,181,182,183,184,185,186,194,195,196,197,198,205,206,208,209,213,218,219,220,223,225,227,228,231,],[-98,-100,-96,-99,-101,-102,-103,-104,-105,-106,-107,-42,-43,130,-89,-94,-70,-71,-81,-82,151,-91,159,-38,-93,-92,-83,-72,-73,-74,-75,-76,-77,-78,-79,-80,-87,-41,-37,-88,-90,-95,-97,-84,-44,-45,-46,-47,196,-51,-53,-54,-55,-56,-57,-58,205,206,-29,-50,-52,-39,-28,-59,-61,-40,-60,-62,-64,-66,228,-63,-65,-67,]),'WITH':([83,122,123,160,205,213,],[124,124,-38,-37,-39,-40,]),'COLON':([91,],[132,]),'RETURN':([163,176,177,178,179,181,182,183,184,185,186,194,195,197,198,208,209,215,217,218,219,220,221,223,224,225,227,228,230,231,],[188,188,188,188,-51,-53,-54,-55,-56,-57,-58,188,188,-50,-52,-59,-61,188,188,-60,-62,-64,188,-66,188,188,-63,-65,188,-67,]),'IF':([163,176,177,178,179,181,182,183,184,185,186,194,195,197,198,208,209,215,217,218,219,220,221,223,224,225,227,228,230,231,],[189,189,189,189,-51,-53,-54,-55,-56,-57,-58,189,189,-50,-52,-59,-61,189,189,-60,-62,-64,189,-66,189,189,-63,-65,189,-67,]),'FOR':([163,176,177,178,179,181,182,183,184,185,186,194,195,197,198,208,209,215,217,218,219,220,221,223,224,225,227,228,230,231,],[190,190,190,190,-51,-53,-54,-55,-56,-57,-58,190,190,-50,-52,-59,-61,190,190,-60,-62,-64,190,-66,190,190,-63,-65,190,-67,]),'WHILE':([163,176,177,178,179,181,182,183,184,185,186,194,195,197,198,208,209,215,217,218,219,220,221,223,224,225,227,228,230,231,],[191,191,191,191,-51,-53,-54,-55,-56,-57,-58,191,191,-50,-52,-59,-61,191,191,-60,-62,-64,191,-66,191,191,-63,-65,191,-67,]),'ELSE':([181,182,183,184,185,186,198,208,209,218,219,220,223,227,228,231,],[-53,-54,-55,-56,-57,-58,-52,-59,-61,-60,224,-64,-66,-63,-65,-67,]),'PIPE':([205,],[213,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'headers':([0,3,],[2,26,]),'header':([0,3,],[3,3,]),'agent_model':([0,3,],[4,4,]),'role_set':([0,3,],[5,5,]),'agent_set':([0,3,],[6,6,]),'agent_attr_set':([0,3,],[7,7,]),'environment_def':([0,3,],[8,8,]),'assign':([0,3,163,176,177,178,194,195,203,215,217,221,224,225,226,230,],[9,9,180,180,180,180,180,180,211,180,180,180,180,180,229,180,]),'increment':([0,3,163,176,177,178,194,195,203,215,217,221,224,225,226,230,],[18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,]),'b_bodies':([2,],[20,]),'b_body':([2,20,],[21,40,]),'behaviour_def':([2,20,],[22,22,]),'function_def':([2,20,36,54,58,59,99,100,101,102,103,104,105,106,107,108,118,119,120,121,132,170,188,202,204,216,],[23,23,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,156,157,67,67,67,67,67,67,67,]),'literal_list_set_statement':([14,],[32,]),'role_set_statement':([30,31,],[46,49,]),'role_def':([30,31,34,88,],[47,47,53,129,]),'literal_list':([33,94,],[51,134,]),'expr':([36,54,58,59,99,100,101,102,103,104,105,106,107,108,118,121,132,170,188,202,204,216,],[56,96,110,111,138,141,142,143,144,145,146,147,148,149,155,158,166,141,201,210,212,222,]),'with_set':([36,54,58,59,97,99,100,101,102,103,104,105,106,107,108,116,118,121,124,132,170,188,202,204,216,],[65,65,65,65,137,65,65,65,65,65,65,65,65,65,65,152,65,65,161,65,65,65,65,65,65,]),'names_list':([43,84,127,],[85,125,164,]),'nameval_pairs':([48,62,],[89,114,]),'nameval_pair':([48,62,131,],[90,90,165,]),'list_set_statement':([55,60,61,136,187,207,],[98,112,113,167,200,214,]),'with_list':([83,],[122,]),'with_block':([83,122,],[123,160,]),'set_expr_list':([100,170,],[140,192,]),'string_list':([117,],[153,]),'statements':([163,176,177,221,],[178,194,195,225,]),'statement':([163,176,177,178,194,195,215,217,221,224,225,230,],[179,179,179,197,197,197,220,220,179,220,197,220,]),'proccall':([163,176,177,178,194,195,215,217,221,224,225,230,],[181,181,181,181,181,181,181,181,181,181,181,181,]),'methcall':([163,176,177,178,194,195,215,217,221,224,225,230,],[182,182,182,182,182,182,182,182,182,182,182,182,]),'returnstmt':([163,176,177,178,194,195,215,217,221,224,225,230,],[183,183,183,183,183,183,183,183,183,183,183,183,]),'if_block':([163,176,177,178,194,195,215,217,221,224,225,230,],[184,184,184,184,184,184,184,184,184,184,184,184,]),'for_block':([163,176,177,178,194,195,215,217,221,224,225,230,],[185,185,185,185,185,185,185,185,185,185,185,185,]),'while_block':([163,176,177,178,194,195,215,217,221,224,225,230,],[186,186,186,186,186,186,186,186,186,186,186,186,]),'then_else_statement':([215,217,224,230,],[219,223,227,231,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> headers b_bodies','program',2,'p_program_0','swapl.py',39),
  ('program -> headers','program',1,'p_program_1','swapl.py',44),
  ('headers -> header','headers',1,'p_headers_1','swapl.py',51),
  ('headers -> header headers','headers',2,'p_headers_2','swapl.py',55),
  ('header -> agent_model','header',1,'p_header_agent_model','swapl.py',61),
  ('header -> role_set','header',1,'p_header_role_set','swapl.py',66),
  ('header -> agent_set','header',1,'p_header_agent_set','swapl.py',69),
  ('header -> agent_attr_set','header',1,'p_header_agent_attributes','swapl.py',72),
  ('header -> environment_def','header',1,'p_header_environment','swapl.py',75),
  ('header -> assign SEMICOLON','header',2,'p_header_assign','swapl.py',78),
  ('header -> IMPORT STRING SEMICOLON','header',3,'p_header_import','swapl.py',81),
  ('agent_model -> MODEL STRING SEMICOLON','agent_model',3,'p_agent_model','swapl.py',87),
  ('role_set -> ROLESET LPAREN role_set_statement RPAREN SEMICOLON','role_set',5,'p_role_set','swapl.py',94),
  ('role_set_statement -> role_set_statement COMMA role_def','role_set_statement',3,'p_role_set_statement_1','swapl.py',99),
  ('role_set_statement -> role_def','role_set_statement',1,'p_role_set_statement_2','swapl.py',104),
  ('role_def -> BEGIN nameval_pairs END','role_def',3,'p_role_def','swapl.py',108),
  ('agent_set -> AGENTSET LPAREN role_set_statement RPAREN SEMICOLON','agent_set',5,'p_agent_set','swapl.py',117),
  ('agent_attr_set -> AGENTATTRSET literal_list_set_statement SEMICOLON','agent_attr_set',3,'p_agent_attr_set','swapl.py',125),
  ('environment_def -> ENVIRONMENT LPAREN role_def RPAREN SEMICOLON','environment_def',5,'p_environment_def','swapl.py',133),
  ('literal_list_set_statement -> LPAREN literal_list RPAREN','literal_list_set_statement',3,'p_literal_listset','swapl.py',139),
  ('literal_list -> NAME COMMA literal_list','literal_list',3,'p_literal_list_1','swapl.py',143),
  ('literal_list -> NAME','literal_list',1,'p_literal_list_2','swapl.py',148),
  ('b_bodies -> b_bodies b_body','b_bodies',2,'p_b_bodies_1','swapl.py',153),
  ('b_bodies -> b_body','b_bodies',1,'p_b_bodies_2','swapl.py',157),
  ('b_body -> behaviour_def','b_body',1,'p_b_body','swapl.py',162),
  ('b_body -> function_def','b_body',1,'p_b_body','swapl.py',163),
  ('behaviour_def -> BEHAVIOUR NAME BEGIN with_list END','behaviour_def',5,'p_behaviour_def','swapl.py',167),
  ('function_def -> FUNCTION NAME LPAREN names_list RPAREN BEGIN statements END','function_def',8,'p_function_1_def','swapl.py',172),
  ('function_def -> FUNCTION LPAREN names_list RPAREN BEGIN statements END','function_def',7,'p_function_2_def','swapl.py',177),
  ('names_list -> NAME COMMA names_list','names_list',3,'p_names_list_1','swapl.py',186),
  ('names_list -> NAME','names_list',1,'p_name_list_2','swapl.py',190),
  ('assign -> VAR NAME EQUAL expr','assign',4,'p_assing_1','swapl.py',197),
  ('assign -> NAME EQUAL expr','assign',3,'p_assing_2','swapl.py',201),
  ('assign -> VAR NAME','assign',2,'p_assing_3','swapl.py',205),
  ('assign -> NAME DOT NAME EQUAL expr','assign',5,'p_assing_4','swapl.py',209),
  ('assign -> increment','assign',1,'p_assing_5','swapl.py',213),
  ('with_list -> with_list with_block','with_list',2,'p_with_list_1','swapl.py',221),
  ('with_list -> with_block','with_list',1,'p_with_list_2','swapl.py',225),
  ('with_block -> WITH with_set BEGIN statements END','with_block',5,'p_with_block_1','swapl.py',232),
  ('with_block -> WITH with_set BEGIN statements END PIPE','with_block',6,'p_with_block_2','swapl.py',236),
  ('with_set -> with_set DOT with_set','with_set',3,'p_with_set_0','swapl.py',243),
  ('with_set -> ALL','with_set',1,'p_with_set_1','swapl.py',247),
  ('with_set -> ONE','with_set',1,'p_with_set_2','swapl.py',251),
  ('with_set -> ROLES LPAREN string_list RPAREN','with_set',4,'p_with_set_3','swapl.py',255),
  ('with_set -> BUT LPAREN expr RPAREN','with_set',4,'p_with_set_4','swapl.py',259),
  ('with_set -> MINIMUM LPAREN function_def RPAREN','with_set',4,'p_with_set_5','swapl.py',263),
  ('with_set -> FILTER LPAREN function_def RPAREN','with_set',4,'p_with_set_6','swapl.py',267),
  ('string_list -> STRING','string_list',1,'p_string_list_1','swapl.py',272),
  ('string_list -> string_list COMMA STRING','string_list',3,'p_string_list_2','swapl.py',276),
  ('statements -> statements statement','statements',2,'p_statements_1','swapl.py',283),
  ('statements -> statement','statements',1,'p_statements_2','swapl.py',287),
  ('statement -> assign SEMICOLON','statement',2,'p_statement','swapl.py',291),
  ('statement -> proccall','statement',1,'p_statement','swapl.py',292),
  ('statement -> methcall','statement',1,'p_statement','swapl.py',293),
  ('statement -> returnstmt','statement',1,'p_statement','swapl.py',294),
  ('statement -> if_block','statement',1,'p_statement','swapl.py',295),
  ('statement -> for_block','statement',1,'p_statement','swapl.py',296),
  ('statement -> while_block','statement',1,'p_statement','swapl.py',297),
  ('proccall -> NAME list_set_statement SEMICOLON','proccall',3,'p_proc_call','swapl.py',304),
  ('methcall -> NAME DOT NAME list_set_statement SEMICOLON','methcall',5,'p_meth_call','swapl.py',312),
  ('returnstmt -> RETURN expr SEMICOLON','returnstmt',3,'p_returnstmt','swapl.py',338),
  ('if_block -> IF LPAREN expr RPAREN then_else_statement','if_block',5,'p_if_1','swapl.py',345),
  ('if_block -> IF LPAREN expr RPAREN then_else_statement ELSE then_else_statement','if_block',7,'p_if_2','swapl.py',350),
  ('then_else_statement -> statement','then_else_statement',1,'p_then_else_1','swapl.py',356),
  ('then_else_statement -> BEGIN statements END','then_else_statement',3,'p_then_else_2','swapl.py',360),
  ('while_block -> WHILE LPAREN expr RPAREN then_else_statement','while_block',5,'p_while','swapl.py',367),
  ('for_block -> FOR LPAREN assign SEMICOLON expr SEMICOLON assign RPAREN then_else_statement','for_block',9,'p_for','swapl.py',377),
  ('increment -> PLUS PLUS NAME','increment',3,'p_pp1_expr','swapl.py',387),
  ('increment -> NAME PLUS PLUS','increment',3,'p_pp2_expr','swapl.py',391),
  ('expr -> INSTANCE NAME','expr',2,'p_instance_expr','swapl.py',399),
  ('expr -> MINUS expr','expr',2,'p_uminus_expr','swapl.py',403),
  ('expr -> expr PLUS expr','expr',3,'p_p_expr','swapl.py',407),
  ('expr -> expr MINUS expr','expr',3,'p_m_expr','swapl.py',411),
  ('expr -> expr TIMES expr','expr',3,'p_t_expr','swapl.py',415),
  ('expr -> expr DIVIDE expr','expr',3,'p_d_expr','swapl.py',419),
  ('expr -> expr EEQUAL expr','expr',3,'p_eequal','swapl.py',423),
  ('expr -> expr NEQUAL expr','expr',3,'p_nequal','swapl.py',427),
  ('expr -> expr LT expr','expr',3,'p_lt','swapl.py',431),
  ('expr -> expr GT expr','expr',3,'p_gt','swapl.py',435),
  ('expr -> LPAREN expr RPAREN','expr',3,'p_expression_group','swapl.py',439),
  ('expr -> SET list_set_statement','expr',2,'p_set_expr','swapl.py',443),
  ('expr -> LIST list_set_statement','expr',2,'p_list_expr','swapl.py',448),
  ('list_set_statement -> LPAREN RPAREN','list_set_statement',2,'p_listset_0','swapl.py',454),
  ('list_set_statement -> LPAREN set_expr_list RPAREN','list_set_statement',3,'p_listset','swapl.py',458),
  ('set_expr_list -> expr COMMA set_expr_list','set_expr_list',3,'p_set_expr_list_1','swapl.py',462),
  ('set_expr_list -> expr','set_expr_list',1,'p_set_expr_list_2','swapl.py',467),
  ('expr -> BEGIN nameval_pairs END','expr',3,'p_struct','swapl.py',472),
  ('nameval_pairs -> nameval_pairs COMMA nameval_pair','nameval_pairs',3,'p_namevals_1','swapl.py',478),
  ('nameval_pairs -> nameval_pair','nameval_pairs',1,'p_namevals_2','swapl.py',484),
  ('nameval_pair -> NAME COLON expr','nameval_pair',3,'p_nameval','swapl.py',488),
  ('expr -> PYTHONLINK STRING','expr',2,'p_pythonlink','swapl.py',497),
  ('expr -> NAME DOT with_set','expr',3,'p_field_set','swapl.py',501),
  ('expr -> NAME DOT NAME','expr',3,'p_field_expr','swapl.py',505),
  ('expr -> NAME list_set_statement','expr',2,'p_fun_call','swapl.py',509),
  ('expr -> NAME DOT NAME list_set_statement','expr',4,'p_fun_call_2','swapl.py',514),
  ('expr -> with_set','expr',1,'p_with_set_expr','swapl.py',523),
  ('expr -> NAME SUBL expr SUBR','expr',4,'p_val_subscript_expr','swapl.py',527),
  ('expr -> NAME','expr',1,'p_val_expr','swapl.py',531),
  ('expr -> NUMBER','expr',1,'p_num_expr','swapl.py',535),
  ('expr -> STRING','expr',1,'p_string_expr','swapl.py',539),
  ('expr -> function_def','expr',1,'p_fundef_expr','swapl.py',543),
  ('expr -> nONE','expr',1,'p_none1_expr','swapl.py',547),
  ('expr -> NONE','expr',1,'p_none2_expr','swapl.py',551),
  ('expr -> nULL','expr',1,'p_none3_expr','swapl.py',555),
  ('expr -> NULL','expr',1,'p_none4_expr','swapl.py',559),
  ('expr -> TRUE','expr',1,'p_true_expr','swapl.py',563),
  ('expr -> FALSE','expr',1,'p_false_expr','swapl.py',567),
]
