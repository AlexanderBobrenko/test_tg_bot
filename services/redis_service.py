import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def set_user_status(chat_id, status):
    print(f"Setting user status: chat_id={chat_id}, status={status}")  # Отладочный вывод
    redis_client.set(f'user:{chat_id}:status', status.encode('utf-8'))

def get_user_status(chat_id: int) -> str:
    status = redis_client.get(f"user:{chat_id}:status")
    print(f"User {chat_id} status: {status}")  # Отладочный вывод
    return status.decode() if status else "Неизвестный"

def set_user_token(chat_id, token):
    print(f"Setting user token: chat_id={chat_id}, token={token}")  # Отладочный вывод
    redis_client.set(f'user:{chat_id}:token', token.encode('utf-8'))

def get_user_token(chat_id):
    token = redis_client.get(f'user:{chat_id}:token')
    token_decoded = token.decode('utf-8') if token else None
    print(f"Getting user token: chat_id={chat_id}, token={token_decoded}")  # Отладочный вывод
    return token_decoded

def delete_user_session(chat_id: int):
    redis_client.delete(f"user:{chat_id}:status", f"user:{chat_id}:token")
    print(f"Session deleted for user {chat_id}. Remaining keys: {redis_client.keys(f'user:{chat_id}:*')}")  # Отладочный вывод
