import ply.lex as lex
from datetime import datetime
import os
from contributions_yadiSuarez import tokens, lexer

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# test
data = '''
$_POST $_SESSION true
$_COOKIE null 3.42 34 "Hello, World!" 'PHP is fun!'
/* This is a multi-line comment
   that should be ignored */
/** Another multi-line comment **/
"meli '123' 23"
/* Nested comment /* still ignored */ end */
// This is a single-line comment
# Another single-line comment
$_GET && false || !true xor
$_SERVER "GET" $GLOBALS
'''
lexer.input(data)

usuarioGit = "yadiSuarez"
fecha_hora = datetime.now().strftime("%d-%m-%Y-%Hh%M")
log_filename = f"lexico-{usuarioGit}-{fecha_hora}.txt"
log_path = os.path.join(LOG_DIR, log_filename)

with open(log_path, "w") as f:
    while True:
        tok = lexer.token()
        if not tok:
            break
            
        f.write(f"{tok}\n")

print(f"Log generado en: {log_path}")