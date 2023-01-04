import unittest
from unittest.mock import Mock, patch

from stripe.error import StripeError

from super_project import errors
from super_project.services import SubscriptionService


class SubscriptionServiceTestCase(unittest.TestCase):
    @patch("stripe.Charge.create")
    def test_charge(self, charge_mock):
        user = Mock()
        subscription_service = SubscriptionService()

        # 1)
        user.has_active_subscription = True
        with self.assertRaises(errors.ActiveSubscriptionException):
            subscription_service.charge(user, 100)

        # 2)
        user.has_active_subscription = False
        user.has_balance.return_value = False
        with self.assertRaises(errors.InsufficientFundsException):
            subscription_service.charge(user, 100)

        # 3)
        user.has_balance.return_value = True
        user.has_payment_token = False
        with self.assertRaises(errors.TokenMissingException):
            subscription_service.charge(user, 100)

        # 4)
        user.has_payment_token = True
        charge_mock.side_effect = StripeError
        with self.assertRaises(errors.PaymentException):
            subscription_service.charge(user, 100)

        # 5)
        charge_mock.side_effect = None
        subscription_service.charge(user, 100)