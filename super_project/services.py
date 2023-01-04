import stripe
from stripe.error import StripeError

from super_project import errors


class SubscriptionService:
    def charge(self, user, amount):
        if user.has_active_subscription:
            raise errors.ActiveSubscriptionException()

        if not user.has_balance(amount):
            raise errors.InsufficientFundsException()

        if not user.has_payment_token:
            raise errors.TokenMissingException()

        try:
            stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=user.payment_token,
                description="XYZ Subscription: Premium plan",
            )
        except StripeError as exc:
            raise errors.PaymentException() from exc
