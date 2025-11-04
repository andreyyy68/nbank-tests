import pytest
from src.main.classes.api_manager import ApiManager
from src.main.api.models.transaction_type import TransactionType




@pytest.mark.api
class TestDepositMoneyUser:
    @pytest.mark.parametrize(
        argnames="balance",
        argvalues=[(1),
                   (5000),
                   (4999),
                   (4000)]
    )
    def test_valid_deposit_user(self, api_manager: ApiManager, user_account, balance):
        api_manager.user_steps.set_user(user_account.user).deposit_user(user_account_id=user_account.account_id, request_balance=balance)
        response = api_manager.user_steps.get_transactions(user_account.account_id)

        for transaction in response:
            assert transaction.relatedAccountId == user_account.account_id
            assert transaction.amount > 0
            assert transaction.type == TransactionType.DEPOSIT.value


        # Тест возвращает 200 при депозите в 10.000 (баг)
    @pytest.mark.parametrize(
        argnames= 'balance, expected_status',
        argvalues= [
            (-1, 400),
            (0, 400)
        ]
    )
    @pytest.mark.debug
    def test_invalid_deposit_user(self, api_manager: ApiManager, user_account, balance, expected_status):
        api_manager.user_steps.set_user(user_account.user).invalid_deposit_user(user_account.account_id, balance, expected_status)
        response = api_manager.user_steps.get_transactions(user_account.account_id)

        for transaction in response:
            assert transaction.amount < 0

        # Проверка депозита на не сущ. аккаунт
    def test_invalid_account_user(self, api_manager: ApiManager, user_request):
        api_manager.user_steps.set_user(user_request).deposit_invalid_id_user(request_balance=1)









