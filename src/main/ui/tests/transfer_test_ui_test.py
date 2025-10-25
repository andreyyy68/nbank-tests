import pytest
from src.main.ui.constants.alert_message import AlertMessage
from src.main.ui.constants.defaults import DefaultValues
from src.main.ui.pages.transfer_page import TransferPage


@pytest.mark.ui
class TestTransfer:
    def test_valid_transfer(self, user_page, api_manager, user_with_two_accounts):
        transfer_page = (TransferPage(user_page).open().
                         select_account(user_with_two_accounts.from_account_id).
                         enter_recipient_name(user_with_two_accounts.user.username).
                         enter_recipient_account_number(f"{DefaultValues.ACC}{user_with_two_accounts.to_account_id}").
                         enter_amount(user_with_two_accounts.balance).
                         check().
                         transfer(AlertMessage.TRANSFER_VALID)
                         )

        transfer = transfer_page.parse_transfer_alert()
        assert transfer == user_with_two_accounts.balance, "The transfer amounts are not equal"

    @pytest.mark.parametrize(
        argnames="amount",
        argvalues=[(0),
                   (-1),
                   (10000)]
    )
    def test_invalid_transfer(self, user_page, api_manager, user_with_two_accounts, amount):
        (TransferPage(user_page).open().
         select_account(user_with_two_accounts.from_account_id).
         enter_recipient_name(user_with_two_accounts.user.username).
         enter_recipient_account_number(f"{DefaultValues.ACC}{user_with_two_accounts.to_account_id}").
         enter_amount(amount).
         check().
         transfer(AlertMessage.TRANSFER_FAILED)
         )

    def test_not_confirm(self, user_page):
        (TransferPage(user_page).open().
        transfer_expected_error(AlertMessage.NOT_CHECK_CONFIRM))



