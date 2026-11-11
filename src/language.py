
import sys
from enum import Enum, auto


def error():
    print("Error")

class TokenType(Enum):
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    ASTRIX = auto()

    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()

    EOF = auto()






    


class Token:
    def __init__(self, type: TokenType, lexeme: str, literal: object, line:int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"{self.type.name} {self.lexeme} {self.literal}"

class Scanner:
    KEYWORDS = {
        "and": TokenType.AND, "class": TokenType.CLASS, "else": TokenType.ELSE,
        "false": TokenType.FALSE, "for": TokenType.FOR, "fun": TokenType.FUN,
        "print": TokenType.PRINT, "return": TokenType.RETURN, "super": TokenType.SUPER,
        "this": TokenType.THIS, "true": TokenType.TRUE, "var": TokenType.VAR,
        "while": TokenType.WHILE, "if": TokenType.IF, "nil": TokenType.NIL, 
        "or": TokenType.OR
    }

    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.start =0
        self.current = 0
        self.line = 1
        self.had_error = False

    def scan_tokens(self):
        while not self.is_at_end():
            self.start=self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens, self.had_error

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> str:
        char = self.source[self.current]
        self.current += 1
        return char

    def peek(self) -> str:
        if self.is_at_end(): return '\0'
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source): return '\0'
        return self.source[self.current+1]

    def match(self, expected: str) ->bool:
        if self.is_at_end() or self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def report_error(self, message: str):
        self.had_error = True
        print(f"Error: {message} at line [{self.line}] while scanning", file=sys.stderr)

    def scan_token(self):
        c=self.advance()
        match c:
            case '(': self.add_token(TokenType.LEFT_PAREN)
            case ')' : self.add_token(TokenType.RIGHT_PAREN)
            case '+' : self.add_token(TokenType.PLUS)
            case '-' : self.add_token(TokenType.MINUS)
            case ',': self.add_token(TokenType.COMMA)
            case '.': self.add_token(TokenType.DOT)
            case '{': self.add_token(TokenType.LEFT_BRACE)
            case '}': self.add_token(TokenType.RIGHT_BRACE)
            case ';': self.add_token(TokenType.SEMICOLON)
            case '*': self.add_token(TokenType.ASTRIX)
        
            case '!': self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
            case '=': self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
            case '<': self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
            case '>': self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)

            case '/':
                if self.match('/'):
                    while self.peek() != '\n' and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
        
            case ' ' | '\r' | '\t': pass
            case '\n': self.line += 1

            case '"': self.handle_string()
            
            case _:
                if c.isdigit():
                    self.handle_number()
                elif c.isalpha() or c == '_':
                    self.handle_identifier()
                else:
                    self.report_error(f"Unexpected character: '{c}'")

    def add_token(self, token_type:TokenType, literal: object = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def handle_string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n': self.line += 1
            self.advance()

        if self.is_at_end():
            self.report_error("String not closed")
            return

        self.advance()

        value=self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)


    def handle_number(self):
        while self.peek().isdigit():
            self.advance()

        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()

        value = float(self.source[self.start:self.current])
        self.add_token(TokenType.NUMBER, value)

    

    def handle_identifier(self):
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()

        text = self.source[self.start:self.current]
        token_type = self.KEYWORDS.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)


# syntax is expression is a binary, grouping, literal, or unary
# binary is expression, operator, expression
# unary is operator, expression
# literal is value

# grammar: function (parameters) strings contained in " "
# math number operator number

# values are number,string,true/false,nil
# groupings are ()
# operators are +,-,*,/



class Expr:

    def accept(self, visitor):
        pass

class Binary(Expr):
    
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)

class Unary(Expr):

    def __init__(self, operator: Token, expression: Expr):
        self.operator = operator
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)

class Grouping(Expr):
    
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)

class Literal(Expr):
    
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)


class PrintNode(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_print_expr(self)

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0
        #self.line = 1
        self.had_error=False
        self.total = 0



    def report_error(self, token: Token, message: str):
            self.had_error = True
            print(f"Error: {message} on line [{token.line}] while parsing", file=sys.stderr)

    def parse(self)->Expr:
        expr=None
        if self.match(TokenType.PLUS, TokenType.ASTRIX, TokenType.SLASH):
            self.report_error(self.previous(),f"missing left operand before {self.previous().lexeme} at token {self.current}")
            return expr, self.had_error
        if self.match(TokenType.PRINT):
                self.consume(TokenType.LEFT_PAREN, "Syntax error: Expect '(' after 'print'.")
                expr = self.expression()
                self.consume(TokenType.RIGHT_PAREN, "Syntax error: Expect ')' after print expression.")
                self.consume(TokenType.SEMICOLON, "Syntax error: Expect ';' at the end of the statement")
                return PrintNode(expr), self.had_error
        
        expr=self.expression()
        self.consume(TokenType.SEMICOLON, "Syntax error: Expect ';' at the end of the statement")
        if self.had_error:
            return expr, self.had_error
        if not self.is_at_end() and self.peek().type == TokenType.RIGHT_PAREN:
            self.report_error(self.previous(),f"Unmatched right parenthesis at token {self.current}")
            return expr, self.had_error
        
        
        return expr, self.had_error

    def expression(self) -> Expr:
        if self.match(TokenType.PLUS, TokenType.ASTRIX, TokenType.SLASH):
                self.report_error(self.previous(),f"missing left operand before {self.previous().lexeme} at token {self.current}")
                return
        return self.equality()

    def equality(self)-> Expr:
        expr = self.comparison()
        while self.match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            operator = self.previous()
            if self.is_at_end() or self.peek().type in (TokenType.RIGHT_PAREN, TokenType.EOF):
                self.report_error(self.previous(),f"missing right operand after {operator.lexeme} at token {self.current}")
                return
            right = self.comparison()
            

            expr = Binary(expr, operator, right)
        return expr

    def comparison(self) -> Expr:

        expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            if self.is_at_end() or self.peek().type in (TokenType.RIGHT_PAREN, TokenType.EOF):
                self.report_error(self.previous(),f"missing right operand after {operator.lexeme} at token {self.current}")
                return
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self) -> Expr:
        expr = self.factor()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous()
            if self.is_at_end() or self.peek().type in (TokenType.RIGHT_PAREN, TokenType.EOF):
                self.report_error(self.previous(),f"missing right operand after {operator.lexeme} at token {self.current}")
                return
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor(self) -> Expr:
        expr = self.unary()
        while self.match(TokenType.ASTRIX, TokenType.SLASH):
            operator = self.previous()
            if self.is_at_end() or self.peek().type in (TokenType.RIGHT_PAREN, TokenType.EOF):
                self.report_error(self.previous(),f"missing right operand after {operator.lexeme} at token {self.current}")
                return
            right = self.unary()
            expr = Binary(expr, operator, right)
            
        return expr

    def unary(self) -> Expr:
        if self.match(TokenType.MINUS, TokenType.BANG):
            operator = self.previous()
            if self.is_at_end() or self.peek().type in (TokenType.RIGHT_PAREN, TokenType.EOF):
                self.report_error(self.previous(),f"missing operand after unary {operator.lexeme} at token {self.current}")
                return
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self) -> Expr:
        if self.match(TokenType.NUMBER):
            return Literal(self.previous().literal)
        if self.match(TokenType.IDENTIFIER):
            return Literal(self.previous().lexeme)
        if self.match(TokenType.TRUE):
            return Literal(self.previous().lexeme)
        if self.match(TokenType.FALSE):
            return Literal(self.previous().lexeme)
        if self.match(TokenType.STRING):
            return Literal(self.previous().literal)
        if self.match(TokenType.NIL):
            return Literal("Nil")
        
        if self.match(TokenType.LEFT_PAREN):
            if self.peek().type == TokenType.RIGHT_PAREN:
                self.report_error(self.previous(),f"empty parenthesis with missing expression at token {self.current}")
                return
            expr = self.expression()
            if expr == None:
                return
            if self.match(TokenType.RIGHT_PAREN):  # Consume closing parenthesis
                return Grouping(expr)
            
            else:
                self.report_error(self.previous(),"Unclosed parenthesis")
                return
        if self.peek().type == TokenType.RIGHT_PAREN:
            self.report_error(self.previous(),"Unmatched closing parenthesis ) at token 0")
            return
        if self.peek().type in (TokenType.PLUS, TokenType.MINUS, TokenType.ASTRIX, TokenType.SLASH):
            self.report_error(self.previous(),f"Unexpected operator {self.peek().lexeme} at token {self.current} where operand was expected")
            return
        
        else:
            self.report_error(self.previous(),f"Unexpected character {self.peek().lexeme}")
            return
        

    def match(self, *types) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def peek(self) -> Token:
        return self.tokens[self.current]

    def check(self, type) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        return self.current >= len(self.tokens)

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def consume(self, type_, message: str) -> Token:
        if self.check(type_): return self.advance()
        self.report_error(self.previous(),message)

class Evaluator:
    def evaluate(self, expr: Expr):
        try:
            return self._evaluate(expr)
        except (TypeError, ZeroDivisionError) as e:
            print(f"Runtime Error: {e}")
            return None

    def _evaluate(self, expr: Expr):
        if expr is None:
            return None

        # Hard-coded routing based on node type
        if isinstance(expr, Literal):
            return expr.value

        elif isinstance(expr, Grouping):
            return self._evaluate(expr.expression)

        elif isinstance(expr, Unary):
            right = self._evaluate(expr.right)
            op_type = expr.operator.type

            if op_type == TokenType.MINUS:
                if isinstance(right, str):
                    raise TypeError(f"Unsupported operand type for unary '-': string.")
                return -right
            elif op_type == TokenType.BANG:
                return 0

        elif isinstance(expr, Binary):
            left = self._evaluate(expr.left)
            right = self._evaluate(expr.right)
            op_type = expr.operator.type

            # Arithmetic Operators
            if op_type in (TokenType.PLUS, TokenType.MINUS, TokenType.ASTRIX, TokenType.SLASH):
                if op_type == TokenType.PLUS:
                    if type(left) != type(right):
                        raise TypeError(f"Cannot add mismatched types: {type(left).__name__} and {type(right).__name__}")
                    return left + right
                
                # Math type validation (Strings not allowed for -, *, /)
                if isinstance(left, str) or isinstance(right, str):
                    raise TypeError(f"Unsupported operand type(s) for '{expr.operator.lexeme}': strings not supported.")
                
                if op_type == TokenType.MINUS: return left - right
                if op_type == TokenType.ASTRIX:  return left * right
                if op_type == TokenType.SLASH:
                    if right == 0:
                        raise ZeroDivisionError("Division by zero.")
                    return left / right
        

            # Comparison Operators
            if op_type in (TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
                if type(left) != type(right) and not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                    raise TypeError(f"Cannot compare mismatched types: {type(left).__name__} and {type(right).__name__}")
                
                if op_type == TokenType.GREATER:
                    if left > right:
                        return 1
                    else:
                        return 0
                if op_type == TokenType.GREATER_EQUAL:
                    if left >= right:
                        return 1
                    else:
                        return 0
                if op_type == TokenType.LESS:
                    if left < right:
                        return 1
                    else:
                        return 0
                if op_type == TokenType.LESS_EQUAL:
                    if left <= right:
                        return 1
                    else:
                        return 0

            # Equality Operators
            if op_type == TokenType.EQUAL_EQUAL:
                if left == right:
                    return 1
                else:
                    return 0
            if op_type == TokenType.BANG_EQUAL:
                if left != right:
                    return 1
                else:
                    return 0
        elif isinstance(expr, PrintNode):
                    value = self._evaluate(expr.expression)
                    # Format booleans cleanly matching your print preferences
                    output = str(value).lower() if isinstance(value, bool) else str(value)
                    print(output)
                    return None

        raise NotImplementedError(f"Unknown evaluation sequence path for node type: {type(expr)}")

class AstPrinter:
    
    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def visit_binary_expr(self, expr: Binary) -> str:
        # Hard-coded logic for formatting binary expressions
        return f"({expr.operator.lexeme} {expr.left.accept(self)} {expr.right.accept(self)})"

    def visit_unary_expr(self, expr:Unary) -> str:
        return f"({expr.operator.lexeme} {expr.expression.accept(self)})"

    def visit_grouping_expr(self, expr: Grouping) -> str:
        # Hard-coded logic for formatting grouped expressions
        return f"(group {expr.expression.accept(self)})"

    def visit_literal_expr(self, expr: Literal) -> str:
        # Hard-coded logic for handling base/leaf values
        if expr.value is None:
            return "nil"
        return str(expr.value)
    
    def visit_print_expr(self, expr: PrintNode)-> str:
        value = expr.expression.accept(self)
        # Explicitly check for internal evaluation state
        if value is None:
            print("nil")
        else:
            print(str(value).lower() if isinstance(value, bool) else value)
        return None
        


 
class Interpreter:
    def __init__(self):
        self.had_error = False
        self.printer = AstPrinter()
        # Scope context defining what variables/classes eval() can access
        self.environment = {
            "TokenType": TokenType,
            "Token": Token,
            "Unary": Unary,
            "Binary": Binary,
            "Grouping": Grouping,
            "Literal": Literal
        }




    def run_file(self, path: str):
        try:
            with open(path, "r", encoding="utf-8") as file:
                self.run(file.read())
                
        except FileNotFoundError:
            print(f"Error: file '{path}' not found", file=sys.stderr)
            sys.exit(1)

    def run_prompt(self):
        while True:
            try:
                returning = input(">>> ").strip()
                
                self.run(returning)
                self.had_error = False
            except (KeyboardInterrupt, EOFError):
                break

    def run(self, source: str,):
        scanner = Scanner(source)
        tokens, error_occurred = scanner.scan_tokens()

        if error_occurred:
            self.had_error = True
            return

        statements_tokens = []
        current_statement = []
    
        for token in tokens:
            if token.type == TokenType.EOF:
                if current_statement:
                    current_statement.append(Token(TokenType.EOF, "", None, token.line))
                    statements_tokens.append(current_statement)
                break
            current_statement.append(token)
            if token.type == TokenType.SEMICOLON:
                # Anchor synthetic EOF to the exact final line of this statement
                current_statement.append(Token(TokenType.EOF, "", None, token.line))
                statements_tokens.append(current_statement)
                current_statement = []


        #parser=Parser(tokens)
        #ast_tree, error_parser = parser.parse()
        #if error_parser:
        #    self.had_error = True
        #    return

        evaluator=Evaluator()

        for stmt_tokens in statements_tokens:
            parser = Parser(stmt_tokens)
            ast_tree, parse_error = parser.parse()

            if not parse_error and ast_tree is not None:
                # Uncomment below to inspect real-time AST structures:
                # print(f"AST Layout Structure: {printer.print(ast_structure)}")
                evaluator.evaluate(ast_tree)

        #for token in tokens:
        #    print(token)
        

        #if isinstance(ast_tree, Expr):
        #    result_string = self.printer.print(ast_tree)
        #    print(f"Structure: {result_string}")
        #else:
        #    print("Error: Evaluated object is not a structural subclass of Expr.")

        #value = evaluator.evaluate(ast_tree)
        #if value is not None and not isinstance(ast_tree, PrintNode):
        #    print(f"Result => {str(value).lower() if isinstance(value, bool) else value}")



    

if __name__ == "__main__":
    mon= Interpreter()
    if len(sys.argv) >= 3:
        print("Error: Too many arguments")
        sys.exit(1)
    elif len(sys.argv)==2:
        mon.run_file(sys.argv[1])
    elif len(sys.argv)==1:
        mon.run_prompt()
    #conor
    #3 15 14 15 18
    #buchkows
    #2 20 3 8 11 15 23 19

#    * + / == 5 3 !3 4

#3 * 15 + !14 / (1.5 == 18)