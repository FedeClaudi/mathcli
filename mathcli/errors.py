class ArgumentsNumberError(ValueError):
    """
        When solving a symbolic expression, not enough params were passed
    """

    def __init__(self, expression, **values):
        self.message = (
            "Wrong number of arguments for evaluating a symbolic expression.\n"
            "Original expression:\n"
            f"   -->   {expression.expression_string}\n"
            "parsed expression:\n"
            f"   -->   {expression.expression}\n"
            f"Found {len(values)} values for {expression.n_variables} variables: {expression.variables}\n"
        )

    def __str__(self):
        return self.message
