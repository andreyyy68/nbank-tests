def ensure_balance(api_manager, account_id, minimum: float = 0.01):
    transactions = api_manager.user_steps.get_transactions(account_id)
    balance = sum(t.amount for t in transactions)
    assert balance >= minimum, f"Баланс {balance} меньше требуемого {minimum}"