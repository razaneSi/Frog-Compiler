class SemanticError(Exception):
    def __init__(self, message):
        
        super().__init__(f"[Semantic Error] : {message}")
        

class Semantique:
    """Analyseur semantique pour le langage FROG."""
    def __init__(self, syntax_tree)-> None:
        """
        Initialise l'analyseur semantique.
        
        Args:
            syntax_tree (ASTNode): Arbre syntaxique abstrait.
        """
        self.ast = syntax_tree
        self.symboles = {}  # { var_name: {"type": ..., "value": ... ,"initialized:..."} } objet de obj

    def run(self)-> None:
        """Execute l'analyse semantique sur l'arbre syntaxique."""
        self.visit_program(self.ast)

    # ---------- Programme ----------
    def visit_program(self, node)-> None:
        """
        Visite un Noeud PROGRAM.
        
        Args:
            node (ASTNode): Noeud PROGRAM a analyser.
        """
        for child in node.children:
            if child.type == "INSTRUCTION_LIST":
                self.visit_instruction_list(child)

    def visit_instruction_list(self, node)-> None:
        """
        Visite une liste d'instructions.
        
        Args:
            node (ASTNode): Noeud INSTRUCTION_LIST a analyser.
        """
        for child in node.children:
            self.visit_instruction(child)                

    # ---------- Liste d'instructions ----------
    def visit_instruction(self, node)-> None:
        """
        Visite une instruction.
        
        Args:
            node (ASTNode): Noeud d'instruction a analyser.
        """

        if node.type == "DECLARATION":
            self.visit_declaration(node)
        elif node.type == "ASSIGNMENT":
            self.visit_assignment(node)
        elif node.type == "PRINT":
            self.visit_print(node)
        elif node.type == "IF_STATEMENT":
            self.visit_if(node)
        elif node.type == "REPEAT_LOOP":
            self.visit_repeat(node)
       

    # ---------- Declaration ----------
    def visit_declaration(self, node)-> None:
        """
        Visite une declaration de variable.
        
        Args:
            node (ASTNode): Noeud DECLARATION a analyser.
            
        Raises:
            SemanticError: Si une variable est deja declaree.
        """
        node_type=node.children[0].type #type de neoud
        if(node_type=="FRG_STRG"):
            var_type="string"
        else:
            var_type = node_type.replace("FRG_", "").lower()#real int ext

        for child in node.children[1:]: #apres le type 1 valeur
            if child.type == "IDENTIFIER":
                var_name = child.value #recuperer le nom de var
                if var_name in self.symboles:#si existe ds table symb erreur
                    raise SemanticError(f"Variable '{var_name}' deja declaree")
                self.symboles[var_name] = {"type": var_type, "value": None,
                "initialized": False}

    # ---------- Affectation ----------
    def visit_assignment(self, node)-> None:
        """
        Visite une affectation de variable.
        
        Args:
            node (ASTNode): Noeud ASSIGNMENT a analyser.
            
        Raises:
            SemanticError: Si variable non declaree ou types incompatibles.
        """
        var_name = node.children[0].value
        if var_name not in self.symboles:
            raise SemanticError(f"Variable '{var_name}' non declaree")

        expr_node = node.children[2]  # expression
        value, value_type = self.evaluate_expression(expr_node)
        var_type = self.symboles[var_name]["type"]

        if not self.type_compatible(var_type, value_type):
            raise SemanticError(f"Incompatibilite de type: '{var_name}' ({var_type}) := {value_type}")

        self.symboles[var_name]["value"] = value
        self.symboles[var_name]["initialized"] = True

    # ---------- PRINT ----------
    def visit_print(self, node)-> None:
        """
        Visite une instruction d'impression.
        
        Args:
            node (ASTNode): Noeud PRINT a analyser.
            
        Raises:
            SemanticError: Si variable non declaree.
        """
        outputs = []
        for child in node.children[1:]:
            if child.type == "IDENTIFIER":
                if child.value not in self.symboles:
                    raise SemanticError(f"Variable '{child.value}' non declaree")
                val = self.symboles[child.value]["value"]
                outputs.append(str(val) if val is not None else "None")
            elif child.type == "STRING":
                outputs.append(child.value.strip('"'))
            elif child.type == "COMMA":
                continue    
        print(*outputs) #unpacking

    # ---------- IF / ELSE ----------
    def visit_if(self, node) -> None:
        """
        Visite une condition IF/ELSE.
        """
        comparison_node = None
        then_block = None
        else_block = None

        # Look for comparison, then block, and else node
        for child in node.children:
            if child.type == "COMPARAISON":
                comparison_node = child
            elif child.type == "ELSE":
                # The else node contains  block/instruction
                else_block = child
            elif child.type in ["BLOCK", "DECLARATION", "ASSIGNMENT", "PRINT", "IF_STATEMENT", "REPEAT_LOOP"]:
                # This is the then block (comes before ELSE)
                if then_block is None:
                    then_block = child
    
    
        cond = self.evaluate_comparison(comparison_node)
    
        if cond and then_block:
            if then_block.type == "BLOCK":
                self.visit_block(then_block)
            else:
                self.visit_instruction(then_block)
    
    # Execute ELSE block
        elif not cond and else_block:
        # else_block is an "ELSE" node, need to get its content
            for child in else_block.children:
                if child.type != "ELSE":  # Skip the ELSE token itself
                    if child.type == "BLOCK":
                        self.visit_block(child)
                    elif child.type in ["DECLARATION", "ASSIGNMENT", "PRINT", "IF_STATEMENT", "REPEAT_LOOP"]:
                        self.visit_instruction(child)



    # ---------- REPEAT / UNTIL ----------
    def visit_repeat(self, node)-> None:
        """
        Visite une boucle REPEAT/UNTIL.
    
        Args:
            node (ASTNode): Noeud REPEAT_LOOP a analyser.
        """
        instr_node = None
        cmp_node = None
        for child in node.children:
            if child.type == "INSTRUCTION_LIST":
                instr_node = child
            elif child.type == "COMPARAISON":
                cmp_node = child

        while True:
            self.visit_instruction_list(instr_node)
            if self.evaluate_comparison(cmp_node):
                break


    # ---------- BLOCK ----------
    def visit_block(self, node)-> None:
      """
        Visite un bloc d'instructions.
        
        Args:
            node (ASTNode): Noeud BLOCK a analyser.
      """
      
    # Parcourir tous les enfants du bloc
      for child in node.children:
        # Ignorer les tokens BEGIN et END
        if child.type in ["BEGIN", "END"]:
            continue
            
        # Si c'est une liste d'instructions, la traiter
        if child.type == "INSTRUCTION_LIST":
            self.visit_instruction_list(child)
          


    def build_expr_string(self, node)-> str:
        """
        Construit une expression Python a partir d'un AST.
        
        Args:
            node (ASTNode): Noeud d'expression a convertir.
            
        Returns:
            str: Expression Python equivalente.
        """
        # Cas de base
        if node.type in ["NUMBER", "REAL"]:
            return node.value
    
        elif node.type == "IDENTIFIER":
            return node.value
    
        elif node.type == "STRING":
            return repr(node.value.strip('"'))  # Garde les guillemets
    
        elif node.type == "FACTOR":
            return self.build_expr_string(node.children[0])
    
        elif node.type == "TERM": #(2+3)
            if len(node.children) == 1:
                return self.build_expr_string(node.children[0])
            else:
                # Parentheses : ( EXPRESSION )
                return f"({self.build_expr_string(node.children[1])})" #"2+3"
    
        elif node.type == "EXPRESSION":
            # Nous devons gerer la priorite des operateurs
            # * et / ont priorite sur + et -
        
            # Separer les operandes et operateurs
            operands = [] #"2+3"
            operators = [] #+
        
            for i, child in enumerate(node.children):
                if i % 2 == 0:  # Operande (position paire)
                    operands.append(self.build_expr_string(child))#term    term
                else:  # Operateur (position impaire) +
                    operators.append(child.value)
        
            # Si un seul operande
            if len(operands) == 1:
                return operands[0]
        
            # Construire l'expression avec priorites
            # Python gere deja les priorites, donc nous pouvons juste
            # construire une expression comme "a + b * c"
            expr = operands[0] #"2+3"
            for i in range(len(operators)):
                # Ajouter l'operateur et l'operande suivant
                op = operators[i]
                if op == '^':        # puissance frog
                    op = '**'
                expr = f"{expr} {op} {operands[i+1]}"
        
            return f"({expr})"  # Parentheses pour securite
    
        return ""
    

    def evaluate_expression(self, node)-> tuple[any, str]:
        """
        evalue une expression et retourne sa valeur et son type.
        
        Args:
            node (ASTNode): Noeud d'expression a evaluer.
            
        Returns:
            tuple: (valeur, type)
            
        Raises:
            SemanticError: En cas d'erreur d'evaluation.
        """
        # Construire la chaîne d'expression
        expr_str = self.build_expr_string(node)
    
        # Preparer le contexte avec les valeurs des variables
        context = {}
        for var_name, info in self.symboles.items():
            if info.get("initialized", False):
                 context[var_name] = info["value"]
    
        try:
            # evaluer l'expression eval evaluates s string as python exprssion return results
            val = eval(expr_str, {}, context) 
        except ZeroDivisionError:
            raise SemanticError("Division par zero interdite"  )
        except NameError as e:
            var_name = str(e).split("'")[1]
            raise SemanticError(f"Variable '{var_name}' non initialisee ou non declaree"  )
        except Exception as e:
            raise SemanticError(f"Erreur d'evaluation: {str(e)}"  )
    
        # Determiner le type du resultat
        if isinstance(val, int):
            typ = "int"
        elif isinstance(val, float):
            typ = "real"
        elif isinstance(val, str):
            typ = "string"
        else:
            raise SemanticError(f"Type inattendu dans le resultat: {type(val)}"  )
    
        return val, typ #retourner valeur expression calculer et son type
 
    def evaluate_comparison(self, node)-> bool:
      """
        evalue une comparaison.
        
        Args:
            node (ASTNode): Noeud COMPARAISON a evaluer.
            
        Returns:
            bool: Resultat de la comparaison.
            
        Raises:
            SemanticError: Si types incompatibles ou operateur inconnu.
        """
      left, left_type = self.evaluate_expression(node.children[0])
      right, right_type = self.evaluate_expression(node.children[2])
     
      
      op = node.children[1].value
    
      if left_type != right_type:
        if left_type == "int" and right_type == "real":
            left = float(left)
        elif left_type == "real" and right_type == "int":
            right = float(right)
        else:#ajouter string
            raise SemanticError(f"Types incompatibles dans la comparaison: {left_type} {op} {right_type}"  )
    
      if op == "==":
        return left == right
      elif op == "!=":
        return left != right
      elif op == "<":
        return left < right
      elif op == "<=":
        return left <= right
      elif op == ">":
        return left > right
      elif op == ">=":
        return left >= right
      else:
        raise SemanticError(f"Operateur inconnu: {op}"  )
      

    # ---------- Type compatibility ----------
    def type_compatible(self, var_type, expr_type)-> bool:
        """
        Verifie la compatibilite de types.
        
        Args:
            var_type (str): Type de la variable.
            expr_type (str): Type de l'expression.
            
        Returns:
            bool: True si les types sont compatibles.
        """

        if var_type == expr_type:
            return True
        if var_type == "real" and expr_type == "int":
            return True
        if var_type == "string" and expr_type == "string":
            return True 
        return False