class ArgumentsNumberError(ValueError):
    """
        When solving a symbolic expression, the wrong number of arguments was passed
    """

    def __init__(self, expression, **values):
        self.message = (
            "Wrong number of arguments for symbolic expression.\n"
            "Original expression:\n"
            f"   -->   {expression.string}\n"
            "parsed expression:\n"
            f"   -->   {expression.expression}\n"
            f"Found {len(values)} values for {expression.n_variables} variables: {expression.variables}\n"
        )

    def __str__(self):
        return self.message


class DerivativeArgumentsNumberError(ValueError):
    """
        When computing a derivative, the wrong number of arguments was passed
    """

    def __init__(self, expression):
        self.message = (
            "When computing the derivative of expressions with >2 variables, "
            "the variable(s) of differentiation must be supplied.\n"
            "Original expression:\n"
            f"   -->   {expression.string}\n"
        )

    def __str__(self):
        return self.message


class CouldNotSolveError(ValueError):
    """
        When computing a derivative, the wrong number of arguments was passed
    """

    def __init__(self, expression, solution, error):
        self.message = f"Failed to solve |{expression}| with error: {error}.\nThis is what we've got: |{solution}|"

    def __str__(self):
        return self.message
