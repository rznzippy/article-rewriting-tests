class ActiveSubscriptionException(RuntimeError):
    pass


class InsufficientFundsException(RuntimeError):
    pass


class TokenMissingException(RuntimeError):
    pass


class PaymentException(RuntimeError):
    pass
