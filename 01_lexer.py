from contextvars import Token


class LexicalError:
    pass


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def advance(self):
        """Переміщуємо 'вказівник' на наступний символ вхідного рядка"""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Означає кінець введення
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        """Пропускаємо пробільні символи."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Повертаємо ціле число, зібране з послідовності цифр."""
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """Лексичний аналізатор, що розбиває вхідний рядок на токени."""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TokenType.INTEGER, self.integer())

            if self.current_char == "+":
                self.advance()
                return Token(TokenType.PLUS, "+")

            if self.current_char == "-":
                self.advance()
                return Token(TokenType.MINUS, "-")

            if self.current_char == "*":  # Додано для операції множення
                self.advance()
                return Token(TokenType.MUL, "*")

            if self.current_char == "/":  # Додано для операції ділення
                self.advance()
                return Token(TokenType.DIV, "/")

            if self.current_char == "(":  # Додано для відкриваючої дужки
                self.advance()
                return Token(TokenType.LPAREN, "(")

            if self.current_char == ")":  # Додано для закриваючої дужки
                self.advance()
                return Token(TokenType.RPAREN, ")")

            raise LexicalError("Помилка лексичного аналізу")

        return Token(TokenType.EOF, None)

class TokenType:
    INTEGER = "INTEGER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MUL = "MUL"       # Операція множення
    DIV = "DIV"       # Операція ділення
    LPAREN = "LPAREN" # Відкриваюча дужка
    RPAREN = "RPAREN" # Закриваюча дужка
    EOF = "EOF"       # Означає кінець вхідного рядка
