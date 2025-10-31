import pytest
from src.main.ui.constants.alert_message import AlertMessage
from src.main.ui.constants.defaults import DefaultValues
from src.main.ui.pages.transfer_page import TransferPage


@pytest.mark.regression
@pytest.mark.ui
class TestTransfer:
    @pytest.mark.parametrize(
        argnames="amount",
        argvalues=[(0.01),
                  (4999)]
        )
    def test_valid_transfer(self, user_page, api_manager, user_with_two_accounts, amount):
        transfer_page = (TransferPage(user_page).open().
                         select_account(user_with_two_accounts.from_account_id).
                         enter_recipient_name(user_with_two_accounts.user.username).
                         enter_recipient_account_number(f"{DefaultValues.ACC}{user_with_two_accounts.to_account_id}").
                         enter_amount(amount).
                         check().
                         transfer(AlertMessage.TRANSFER_VALID)
                         )

        transfer = transfer_page.parse_transfer_alert()
        assert transfer == amount, "The transfer amounts are not equal"

    @pytest.mark.parametrize(
        argnames="amount, message",
        argvalues=[(0, AlertMessage.TRANSFER_FAILED),
                   (-1, AlertMessage.TRANSFER_FAILED),
                   (10000.01, AlertMessage.TRANSFER_FAILED),
                   (9999.99, AlertMessage.TRANSFER_FAILED),
                   ]
    )
    def test_invalid_transfer(self, user_page, api_manager, user_with_two_accounts, amount, message):
        (TransferPage(user_page).open().
         select_account(user_with_two_accounts.from_account_id).
         enter_recipient_name(user_with_two_accounts.user.username).
         enter_recipient_account_number(f"{DefaultValues.ACC}{user_with_two_accounts.to_account_id}").
         enter_amount(amount).
         check().
         transfer(message)
         )

    def test_not_confirm(self, user_page):
        (TransferPage(user_page).open().
        transfer_expected_error(AlertMessage.NOT_CHECK_CONFIRM))