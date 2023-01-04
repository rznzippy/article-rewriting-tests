import unittest
from unittest.mock import Mock

import stripe
from stripe.error import StripeError

from super_project import errors
from super_project.services import SubscriptionService


class SubscriptionServiceTestCase(unittest.TestCase):
    def setUp(self):
        stripe_mock = Mock(spec=stripe)
        self.charge_mock = stripe_mock.Charge.create
        self.user = Mock(
            has_active_subscription=False,
            has_balance=Mock(return_value=True),
            has_payment_token=True,
        )

        self.instance = SubscriptionService(stripe=stripe_mock)

    def test_charge_calls_stripe_charge_correctly(self):
        self.instance.charge(self.user, 100)

        self.charge_mock.assert_called_once_with(
            amount=100,
            currency="usd",
            source=self.user.payment_token,
            description="XYZ Subscription: Premium plan",
        )

    def test_charge_raises_active_subscription_exception(self):
        self.user.has_active_subscription = True

        with self.assertRaises(errors.ActiveSubscriptionException):
            self.instance.charge(self.user, 100)

    def test_charge_raises_insufficient_funds_exception(self):
        self.user.has_balance.return_value = False

        with self.assertRaises(errors.InsufficientFundsException):
            self.instance.charge(self.user, 100)

    def test_charge_raises_token_missing_exception(self):
        self.user.has_payment_token = False

        with self.assertRaises(errors.TokenMissingException):
            self.instance.charge(self.user, 100)

    def test_charge_raises_payment_exception(self):
        self.charge_mock.side_effect = StripeError

        with self.assertRaises(errors.PaymentException):
            self.instance.charge(self.user, 100)

    def test_charge_does_not_raise_exception(self):
        self.instance.charge(self.user, 100)
