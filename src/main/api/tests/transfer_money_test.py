from src.main.classes.api_manager import ApiManager
from src.main.api.models.user_two_accounts import UserTwoAccounts
import pytest



@pytest.mark.api
class TestTransferMoney():
    # Дефолтный позитивный (между своими счетами)
    def test_transfer_money(self, api_manager: ApiManager, user_with_two_accounts: UserTwoAccounts, amount=300):
        api_manager.user_steps.set_user(user_with_two_accounts.user).transfer_between_your_accounts(user_with_two_accounts, amount)
        response = api_manager.user_steps.get_transactions_between_your_accounts(user_with_two_accounts)

        for transaction in response:
            assert transaction.relatedAccountId == user_with_two_accounts.to_account_id


    @pytest.mark.parametrize(
        argnames= 'amount, expected_status',
        argvalues=[
            (0, 400),
            (10000, 400),
            (10001, 400)
        ]
    )
    def test_invalid_transfer_money(self, api_manager: ApiManager, amount, expected_status, user_with_two_accounts: UserTwoAccounts):
        api_manager.user_steps.transfer_between_invalid_your_accounts(user_with_two_accounts, amount, expected_status)
        response = api_manager.user_steps.get_transactions_between_your_accounts(user_with_two_accounts)
        for transaction in response:
            assert transaction.amount < 0


    def test_transfer_money_different_users(self, api_manager: ApiManager, user_with_two_accounts: UserTwoAccounts, amount=911):
        api_manager.user_steps.transfer_between_your_accounts(user_with_two_accounts, amount)








