OPERATORS = {'+': (1, lambda x, y: x + y), '-': (1, lambda x, y: x - y),
             '*': (2, lambda x, y: x * y), '/': (2, lambda x, y: x / y)}


def eval_(formula_string):
    """
    Analog of eval() built-in function

    Parameters
    ----------
    formula_string: str
        mathematical expression

    Returns
    -------
    result of mathematical expression in float type
    """

    def preparse(formula_string):
        """
        Checking signs and inserting '0' in front of unary minus.

        Parameters
        ----------
        formula_string: str
            mathematical expression

        Returns
        -------
        preparsed expression in str type
        """
        formula_list = [s for s in formula_string if s != ' ']
        new = ''
        for counter, s in enumerate(formula_list):
            if s not in '1234567890.+-*/()':
                raise Exception('DO NOT UNDERSTAND YOUR QUERY! PLEASE USE APPROPRIATE SYMBOLS')
            elif s != '-':
                new += s
            elif counter == 0 and s == '-':
                new += '0-'
            elif s == '-' and (formula_list[counter - 1] in OPERATORS or formula_list[counter - 1] in '()'):
                new += '0-'
        return new

    def parse(formula_string):
        """
        Generator parsing of the original expression into numbers, scoops and signs

        Parameters
        ----------
        formula_string: str
            mathematical expression

        Returns
        -------
        yields number, scoop or sign to stack in str or float type
        """
        number = ''
        for s in formula_string:

            if s in '1234567890.':
                number += s
            elif number:
                yield float(number)
                number = ''
            if s in OPERATORS or s in "()":
                yield s
        if number:
            yield float(number)

    def shunting_yard(parsed_formula):
        """
        Shunting yard algorythm.

        Parameters
        ----------
        parsed_formula: Union[str, float]
            return of parse function

        Returns
        -------
        yields number, scoop or sign to stack in str or float type
        """
        stack = []
        for token in parsed_formula:
            if token in OPERATORS:
                while stack and stack[-1] != "(" and OPERATORS[token][0] <= OPERATORS[stack[-1]][0]:
                    yield stack.pop()
                stack.append(token)
            elif token == ")":
                while stack:
                    x = stack.pop()
                    if x == "(":
                        break
                    yield x
            elif token == "(":
                stack.append(token)
            else:
                yield token
        while stack:
            yield stack.pop()

    def calc(polish):
        """
        Evaluation of expression using stack.

        Parameters
        ----------
        polish: list
            stack

        Returns
        -------
        result of operation in float type
        """
        stack = []
        for token in polish:
            if token in OPERATORS:
                y, x = stack.pop(), stack.pop()
                try:
                    stack.append(OPERATORS[token][1](x, y))
                except ZeroDivisionError:
                    return 'DO NOT DIVIDE BY ZERO! IT IS FORBIDDEN, STUPIDO!'
            else:
                stack.append(token)
        return stack[0]

    return calc(shunting_yard(parse(preparse(formula_string))))
