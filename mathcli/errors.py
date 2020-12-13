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

    def __init__(self, expression, wrt):
        self.message = (
            "When computing the derivative of expressions with >2 variables, "
            "the variable(s) of differentiation must be supplied.\n"
            "Original expression:\n"
            f"   -->   {expression.string}\n"
            "Derivation variables:\n"
            "".join(wrt)
        )

    def __str__(self):
        return self.message
