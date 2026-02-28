import re
#nmpy
token_specs = [

    # keywords (important : they must be FIRST

    # VALID keywords (must be first)
    (r'\bFRG_Begin\b', 'FRG_BEGIN'),
    (r'\bFRG_End\b', 'FRG_END'),
    (r'\bFRG_Int\b', 'FRG_INT'),
    (r'\bFRG_Real\b', 'FRG_REAL'),
    (r'\bFRG_Strg\b', 'FRG_STRG'),
    (r'\bFRG_Print\b', 'FRG_PRINT'),

    (r'\bIf\b', 'IF'),
    (r'\bElse\b', 'ELSE'),
    (r'\bBegin\b', 'BEGIN'),
    (r'\bEnd\b', 'END'),
    (r'\bRepeat\b', 'REPEAT'),
    (r'\buntil\b', 'UNTIL'),

    # BAD keywords (must be BEFORE IDENTIFIER)
    (r'\bFRG_(?!(Begin|End|Int|Real|Strg|Print)\b)[A-Za-z0-9_]+\b', 'BAD_KEYWORD'),
    (r'\b(If|Else|Begin|End|Repeat|until)[A-Za-z0-9_]+\b', 'BAD_KEYWORD'),
    # comments
    (r'##.*', 'COMMENT'),

    # operators
    (r':=', 'ASSIGN'),
    (r'\[', 'LBRACKET'),
    (r'\]', 'RBRACKET'),
    (r',', 'COMMA'),
    (r'#', 'HASH'),

    (r'[+\-*/^%]', 'OPERATOR'),

    (r'<=|>=|==|!=|<|>', 'COMPARISON'),

    # literals
    (r'\d+\.\d+', 'REAL'),
    (r'\d+', 'NUMBER'),
    (r'"[^"]*"', 'STRING'),

    # identifier (must always be last)
    (r'[a-zA-Z]([a-zA-Z0-9]*(_*[a-zA-Z0-9])*)', 'IDENTIFIER'),

    # spaces
    (r'[ \t]+', 'SKIP'),
    (r'\n', 'NEWLINE'),
]

class LexicalError(Exception):
    """Raised when the lexer encounters an unknown or invalid symbol."""
    def __init__(self, line, column, symbol):
        message = f"[Erreur lexicale] ligne {line}, colonne {column} : symbole inconnu '{symbol}'"
        super().__init__(message)
        self.line = line
        self.column = column
        self.symbol = symbol

class Lexer:
    #LISTE DES TOKENS FROG
   

    def __init__(self,code):
         self.code=code
         self.tokens=[]
         self.ligne=1
         self.colonne=1

    def tokenize(self):
        position_code = 0
    
        while position_code < len(self.code):
            match_found = False
    
            for expression, token_name in token_specs:
                regex = re.compile(expression)
                match = regex.match(self.code, position_code)
    
                if match:
                    match_found = True
                    text = match.group(0)
    
                    #  BAD KEYWORD  lexical error
                    if token_name == "BAD_KEYWORD":
                        raise LexicalError(self.ligne, self.colonne, text)
    
                    # add token unless skip/comment
                    if token_name not in ["SKIP", "COMMENT"]:
                        self.tokens.append((token_name, text, self.ligne, self.colonne))
    
                    # update line/column
                    nb_newlines = text.count("\n")
                    if nb_newlines > 0:
                        self.ligne += nb_newlines
                        self.colonne = 1
                    else:
                        self.colonne += len(text)
    
                    position_code = match.end()
                    break
    
            if not match_found:
                raise LexicalError(self.ligne, self.colonne, self.code[position_code])
    
        return self.tokens
