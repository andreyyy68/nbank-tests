from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.deposit_request import DepositRequestModel
from src.main.ui.constants.alert_message import AlertMessage
from src.main.ui.pages.deposit_page import DepositPage
import pytest



@pytest.mark.regression
@pytest.mark.ui
class TestDepositUser:
    def test_valid_deposit_user(self, api_manager, user_page, user_account):
        user_amount = RandomModelGenerator.generate(DepositRequestModel)
        deposit_page = (DepositPage(user_page).open().
         select_account(user_account.account_id).
         enter_amount(user_amount.balance).
         submit_deposit(AlertMessage.DEPOSIT_ACCOUNT))

        deposited_amount = deposit_page.parse_deposit_alert()
        assert deposited_amount == user_amount.balance, f"The deposit {deposited_amount} does not match the deposit {user_amount.balance} on the account"

        deposit = api_manager.user_steps.get_transactions(user_account.account_id)
        for deposit_user in deposit:
            assert deposit_user.amount == user_amount.balance, "The balance was not replenished on BE"

    @pytest.mark.parametrize(
        argnames="amount, message",
        argvalues=[(0, AlertMessage.DEPOSIT_ACCOUNT_FAILED),
                   (-1, AlertMessage.DEPOSIT_ACCOUNT_FAILED),
                   (5001, AlertMessage.DEPOSIT_MORE_MAX),
                   ]
    )
    def test_invalid_deposit_user(self, api_manager, user_page, user_account, amount, message):
        (DepositPage(user_page).open().
         select_account(user_account.account_id).
         enter_amount(amount).
         submit_deposit_expecting_error(message))

        deposit = api_manager.user_steps.get_transactions(user_account.account_id)
        for deposit_user in deposit:
            assert deposit_user.amount < 0, "The balance was replenished on BE"
