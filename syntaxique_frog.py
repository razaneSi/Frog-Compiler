from graphviz import Digraph

class SyntaxiqueError(Exception):
    """Raised when a syntax error is found."""
    def __init__(self, line, val):
        message = f"[Erreur syntaxique] de la valeur:<{val}> a la ligne :{line}"
        super().__init__(message)
        self.line = line
        self.val = val



class ASTNode:
    def __init__(self,nodeType,value=None): #node type declaration assign ext value of the token
        self.type=nodeType
        self.value=value
        self.children=[] #liste de sous noeuds



class Syntaxe:
    """Analyseur syntaxique pour le langage FROG."""
    def __init__(self, tokens)-> None:
        """
        Initialise l'analyseur syntaxique.
        
        Args:
            tokens (list): Liste de tokens generee par le lexer.
        """
        self.tokens = tokens
        self.pos = 0


        self.graph = Digraph(comment="Arbre Syntaxique FROG") #objet graph directed
        self.node_count = 0 #nbr de nodes help in id

    def add_node(self, label):
        node_id = f"n{self.node_count}"
        self.node_count += 1
        self.graph.node(node_id, label)
        return node_id
    
    def add_edge(self, parent, child):
        self.graph.edge(parent, child)



    def checkToken(self, kind)-> tuple[str | None, ASTNode]: #kins is type of token
        """
        Verifie si le token actuel correspond au type attendu.
        
        Args:
            kind (str): Type de token attendu.
            
        Returns:
            tuple: (identifiant_node_graphviz, ASTNode)
            
        Raises:
            SyntaxiqueError: Si le token ne correspond pas.
        """
        if self.pos < len(self.tokens) and kind == self.tokens[self.pos][0] : #pos 0: nom token pos1:valeur token pos 2: line pos 3: column depuis tuple lex
            if kind != "NEWLINE":  
                label = f"{self.tokens[self.pos][0]} ({self.tokens[self.pos][1]})"#token name+ value
            
                node = self.add_node(label) #return id
            
                
            else:
                node=None #if newline no node

            value = self.tokens[self.pos][1]
            self.pos += 1    
            return node, ASTNode(kind,value)
        else:
            raise SyntaxiqueError(self.tokens[self.pos][2],self.tokens[self.pos][1])
        

    def skipNewlines(self)-> None:
        """Ignore les sauts de ligne (NEWLINE) consecutifs."""
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] == "NEWLINE":
            self.checkToken("NEWLINE")    

    def program(self)-> tuple[str, ASTNode]:

        """
        Analyse un programme FROG complet.

        Regle: PROGRAMME → FRG_BEGIN NEWLINE LISTE_INSTRUCTIONS FRG_END
                
        Returns:
            tuple: (identifiant_racine_graphviz, ASTNode_racine)
        """

        root = self.add_node("PROGRAM") #axiome add node graph
        ast_root = ASTNode("PROGRAM") #ast arbre syntaxique

        self.skipNewlines()


        n1,a1 = self.checkToken("FRG_BEGIN") #id objet ast node
        self.add_edge(root, n1)
        ast_root.children.append(a1)#add frg_begin to root 

        self.checkToken("NEWLINE")

        instr_node,a_list  = self.instructionsList() #parent ast liste
        
        self.add_edge(root, instr_node)

        ast_root.children.append(a_list)


        n2,a2 = self.checkToken("FRG_END")
        
        self.add_edge(root, n2)
        ast_root.children.append(a2)

        self.skipNewlines()
        print("Programme FROG correct")

        self.skipNewlines()
        
        self.graph.render("arbre_syntaxique", format="png", cleanup=True)
        print("Arbre syntaxique genre : arbre_syntaxique.png")
        
        return root,ast_root
    

    def instructionsList(self)-> tuple[str, ASTNode]:
        """
        Analyse une liste d'instructions.

        Regle:  LISTE_INSTRUCTIONS → INSTRUCTION LISTE_INSTRUCTIONS | ε
                
        Returns:
            tuple: (identifiant_node_graphviz, ASTNode)
        """

        parent = self.add_node("INSTRUCTION_LIST")

        ast_list=ASTNode("INSTRUCTION_LIST")
        while self.pos < len(self.tokens) :
            if self.tokens[self.pos][0] in ["FRG_END","END", "UNTIL", "ELSE"]:
                break
            if self.tokens[self.pos][0] == "NEWLINE":
                self.checkToken("NEWLINE")
                continue  # skip empty lines
            instr_node,ast_inst = self.instruction()
            if instr_node is not None:
                self.add_edge(parent, instr_node)
                ast_list.children.append(ast_inst)
        
        return parent,ast_list   
            

    def instruction(self) -> tuple[str | None, ASTNode | None]:
        """
        Analyse une instruction unique.

        Regle:  INSTRUCTION → DECLARATION | AFFECTATION | AFFICHAGE | CONDITION | BOUCLE | NEWLINE
            
        Returns:
            tuple: (identifiant_node_graphviz, ASTNode) ou (None, None) pour NEWLINE
        """
        if self.pos >= len(self.tokens):
            return None, None
        token = self.tokens[self.pos][0]
        if token in ["FRG_INT", "FRG_REAL", "FRG_STRG"]:
            return self.declaration()
            
        elif token == "IDENTIFIER":
            return self.assignment()
        elif token == "FRG_PRINT":
            return self.printInstruction()
        elif token=="IF":
            return self.condition() 
        elif token=="REPEAT":
            return self.loop() 
        elif token =="NEWLINE":
            self.checkToken("NEWLINE")
            return None,None
        else:
            raise SyntaxiqueError(self.tokens[self.pos][2],self.tokens[self.pos][1])

    
    def declaration(self)-> tuple[str, ASTNode]:
        """
        Analyse une declaration de variable.

        Regle: 
               DECLARATION → TYPE LISTE_IDENTIFIANTS HASH NEWLINE
               TYPE → FRG_INT | FRG_REAL | FRG_STRG
               LISTE_IDENTIFIANTS →IDENTIFIER SUITE_IDENTIFIANTS
               SUITE_IDENTIFIANTS →COMMA IDENTIFIER SUITE_IDENTIFIANTS | ε
           
        Returns:
            tuple: (identifiant_node_graphviz, ASTNode)
        """

        parent = self.add_node("DECLARATION")

        ast_dec=ASTNode("DECLARATION")

        t_type,a_type =self.checkToken(self.tokens[self.pos][0])  
        self.add_edge(parent, t_type)
        ast_dec.children.append(a_type)
        
        var ,avar = self.checkToken("IDENTIFIER")
        self.add_edge(parent, var)
       
        ast_dec.children.append(avar)
        
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] == "COMMA":
            com , acom=self.checkToken("COMMA")
            self.add_edge(parent, com)
            ast_dec.children.append(acom)

            var,avar = self.checkToken("IDENTIFIER")
            self.add_edge(parent, var)
            ast_dec.children.append(avar)


        finins,afini=self.checkToken("HASH")
        self.add_edge(parent, finins)
        ast_dec.children.append(afini)
        
        self.checkToken("NEWLINE")

        print("Declaration correcte")

        return parent,ast_dec


    
    def assignment(self)-> tuple[str, ASTNode]:
        """
        Analyse une affectation de variable.

        Regle:  
                AFFECTATION → IDENTIFIER ASSIGN EXPRESSION HASH NEWLINE
                
        Returns:
            tuple: (identifiant_node_graphviz, ASTNode)
        """
        parent = self.add_node("ASSIGNMENT")

        a_assign=ASTNode("ASSIGNMENT")

        var,avar = self.checkToken("IDENTIFIER")
        self.add_edge(parent, var)
        a_assign.children.append(avar)


        assign, assign_ast = self.checkToken("ASSIGN")
        self.add_edge(parent, assign)
        a_assign.children.append(assign_ast)


        expr,a_exp = self.expression() #verifier exprss
        self.add_edge(parent, expr)
        a_assign.children.append(a_exp)

        finins,afin=self.checkToken("HASH")
        self.add_edge(parent, finins)
        a_assign.children.append(afin)
        
        self.checkToken("NEWLINE")
        print("Affectation correcte")

        return parent,a_assign
    
    
    def expression(self)-> tuple[str, ASTNode]:
        """
        Analyse une expression arithmetique.

        Regle: 
                EXPRESSION → TERME SUITE_EXPRESSIONS
                SUITE_EXPRESSIONS → OPERATOR TERME SUITE_EXPRESSIONS | ε
                
                
        Returns:
            tuple: (identifiant_node_graphviz, ASTNode)
        """
        parent = self.add_node("EXPRESSION")
        a_exp = ASTNode("EXPRESSION")
        
        term_node, a_term = self.term() #call term
        self.add_edge(parent, term_node)
        a_exp.children.append(a_term)
        #suite d'expression
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] == "OPERATOR":
            op, aop = self.checkToken("OPERATOR")
            self.add_edge(parent, op)
            a_exp.children.append(aop)
            
            term_node, a_term = self.term()
            self.add_edge(parent, term_node)
            a_exp.children.append(a_term)
        
        return parent, a_exp
    
    def term(self)-> tuple[str, ASTNode]:
        """
        Analyse un terme d'expression.

        Regle:   TERME → FACTEUR | LBRACKET EXPRESSION RBRACKET
                
        Returns:
            tuple: (identifiant_node_graphviz, ASTNode)
        """
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == "LBRACKET":
            parent = self.add_node("TERM")
            a_term = ASTNode("TERM")
            
            lbr, a_lbr = self.checkToken("LBRACKET")
            self.add_edge(parent, lbr)
            a_term.children.append(a_lbr)
            
            expr_node, a_expr = self.expression() #expression
            self.add_edge(parent, expr_node)
            a_term.children.append(a_expr)
            
            rbr, a_rbr = self.checkToken("RBRACKET")
            self.add_edge(parent, rbr)
            a_term.children.append(a_rbr)
            
            return parent, a_term
        else:
            # Sinon, c'est un facteur simple
            return self.factor()
    
    def factor(self)-> tuple[str, ASTNode]:
        """
        Analyse un facteur d'expression.

        Regle:  FACTEUR → IDENTIFIER | NUMBER | REAL | STRING
                
        Returns:
            tuple: (identifiant_node_graphviz, ASTNode)
        """
        parent = self.add_node("FACTOR")
        a_factor = ASTNode("FACTOR")
        
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] in ["IDENTIFIER", "NUMBER", "REAL", "STRING"]:
            val, aval = self.checkToken(self.tokens[self.pos][0])
            self.add_edge(parent, val)
            a_factor.children.append(aval)
        else:
            raise SyntaxiqueError(self.tokens[self.pos][2],self.tokens[self.pos][1])
        
        return parent, a_factor
    

    def printInstruction(self)-> tuple[str, ASTNode]:
        """
        Analyse une instruction d'impression.

        Regle:
                AFFICHAGE → FRG_PRINT LISTE_AFFICHAGE HASH NEWLINE
                LISTE_AFFICHAGE → ELEMENT SUITE_ELEMENTS
                SUITE_ELEMENTS → COMMA ELEMENT SUITE_ELEMENTS | ε
                ELEMENT →IDENTIFIER | STRING
                
        Returns:
            tuple: (identifiant_node_graphviz, ASTNode)
        """
        parent = self.add_node("PRINT")
        a_parent = ASTNode("PRINT")

        p, a1 = self.checkToken("FRG_PRINT")
        self.add_edge(parent, p)
        a_parent.children.append(a1)


        if self.tokens[self.pos][0] in ["IDENTIFIER", "STRING"]:
            var, a2 = self.checkToken(self.tokens[self.pos][0])
            self.add_edge(parent, var)
            a_parent.children.append(a2)
        else:
            raise SyntaxiqueError(self.tokens[self.pos][2],self.tokens[self.pos][1])

        while self.pos < len(self.tokens) and self.tokens[self.pos][0] == "COMMA":
            com, acom = self.checkToken("COMMA")
            self.add_edge(parent, com)
            a_parent.children.append(acom)
            
            if self.tokens[self.pos][0] in ["IDENTIFIER", "STRING"]:
                var, avar = self.checkToken(self.tokens[self.pos][0])
                self.add_edge(parent, var)
                a_parent.children.append(avar)
            else:
                raise SyntaxiqueError(self.tokens[self.pos][2],self.tokens[self.pos][1])
       
        finins,a3=self.checkToken("HASH")
        self.add_edge(parent, finins)
        a_parent.children.append(a3)
        self.checkToken("NEWLINE")
        print("Instruction Print correcte")
        
        return parent,a_parent
    
   
    def condition(self) -> tuple[str, ASTNode]:
        """
        Analyse une condition IF/ELSE.

        Regle:
                CONDITION → IF LBRACKET COMPARAISON RBRACKET NEWLINE CORPS_CONDITION SINON_OPTIONNEL
                CORPS_CONDITION →INSTRUCTION | BLOC
                SINON_OPTIONNEL → ELSE NEWLINE CORPS_SINON | ε
                CORPS_SINON →INSTRUCTION | BLOC
                
        
        Returns:
            tuple: (identifiant_node_graphviz, ASTNode)
        """

        parent = self.add_node("IF_STATEMENT")
        a_parent = ASTNode("IF_STATEMENT")

        if_statement,a1= self.checkToken("IF") 
        a_parent.children.append(a1)
        
        self.add_edge(parent, if_statement)
        var, aL=self.checkToken("LBRACKET")
        self.add_edge(parent, var)
        a_parent.children.append(aL)

        var_comparaisson, acmp=self.comparaison()#call comparaison
        self.add_edge(parent, var_comparaisson)
        a_parent.children.append(acmp)

        var, aR=self.checkToken("RBRACKET")
        self.add_edge(parent, var)
        a_parent.children.append(aR)

        self.checkToken("NEWLINE")

        self.skipNewlines()

 #si un bloc begin
        if self.tokens[self.pos][0]=="BEGIN":
            blck,ablck=self.block()
            if blck is not None:
                self.add_edge(parent, blck)
                a_parent.children.append(ablck)


        else:
            inst,ainst=self.instruction()
            if inst is not None:
                self.add_edge(parent, inst) 
                a_parent.children.append(ainst)

        
        self.skipNewlines()      
        if self.pos < len(self.tokens) and self.tokens[self.pos][0]=="ELSE":

            els,aesl=self.checkToken("ELSE")
            
            self.add_edge(parent, els)
            a_parent.children.append(aesl)

            self.checkToken("NEWLINE")
            self.skipNewlines()

            
            if  self.pos < len(self.tokens) and self.tokens[self.pos][0]=="BEGIN":
                block,ablck=self.block()
                if block is not None:
                    self.add_edge(els, block)
                    aesl.children.append(ablck)
            else:
                inst,ainst=self.instruction()
                if inst is not None:
                    self.add_edge(els, inst)
                    aesl.children.append(ainst)

            self.skipNewlines()

        return parent,a_parent            
      
     
     
    def comparaison(self)-> tuple[str, ASTNode]:
        """
        Analyse une comparaison.

        Regle:  
                COMPARAISON → EXPRESSION COMPARISON EXPRESSION
        
        Returns:
            tuple: (identifiant_node_graphviz, ASTNode)
        """
        
        
        parent = self.add_node("COMPARAISON")
        a_parent = ASTNode("COMPARAISON")

        expr1_node, expr1_ast = self.expression() #call exprssion
        self.add_edge(parent, expr1_node)
        a_parent.children.append(expr1_ast)

        comp_token, comp_ast = self.checkToken("COMPARISON")
        self.add_edge(parent, comp_token)
        a_parent.children.append(comp_ast)

        expr2_node, expr2_ast = self.expression()  #call exprssion
        self.add_edge(parent, expr2_node)
        a_parent.children.append(expr2_ast)
            
        return parent, a_parent
        
    

    def block(self) -> tuple[str, ASTNode]:
        """
        Analyse un bloc d'instructions.

        Regle:   BLOC → BEGIN NEWLINE LISTE_INSTRUCTIONS NEWLINE END  NEWLINE
                
                
        Returns:
            tuple: (identifiant_node_graphviz, ASTNode)
        """
        parent = self.add_node("BLOCK")
        a_parent = ASTNode("BLOCK")

        var, a1=self.checkToken("BEGIN")
        self.add_edge(parent, var)
        a_parent.children.append(a1)
        
        self.checkToken("NEWLINE")

        var,a2=self.instructionsList()  #call liste instr
        self.add_edge(parent, var)
        a_parent.children.append(a2)

        var,a3=self.checkToken("END")
        self.add_edge(parent, var)
        a_parent.children.append(a3)

        self.checkToken("NEWLINE")

        return parent,a_parent
    

    def loop(self)-> tuple[str, ASTNode]:
        """
        Analyse une boucle REPEAT/UNTIL.

        Regle:   BOUCLE → REPEAT NEWLINE LISTE_INSTRUCTIONS NEWLINE UNTIL LBRACKET COMPARAISON RBRACKET NEWLINE
          
        Returns:
            tuple: (identifiant_node_graphviz, ASTNode)
        """

        parent = self.add_node("REPEAT_LOOP")
        a_parent = ASTNode("REPEAT_LOOP")

        var,a1=self.checkToken("REPEAT")
        self.add_edge(parent, var)
        a_parent.children.append(a1)
      
        self.checkToken("NEWLINE")

        var, alist=self.instructionsList()  #call liste instr

        self.add_edge(parent, var)
        a_parent.children.append(alist)

        
        var, a2 =self.checkToken("UNTIL")
        self.add_edge(parent, var)
        a_parent.children.append(a2)

        var, aL =self.checkToken("LBRACKET")
        self.add_edge(parent, var)
        a_parent.children.append(aL)

        comp, acmp =self.comparaison()
        self.add_edge(parent, comp)
        a_parent.children.append(acmp)

        var, aR=self.checkToken("RBRACKET")
        a_parent.children.append(aR)
        self.add_edge(parent, var)

        self.checkToken("NEWLINE")

        return parent ,a_parent