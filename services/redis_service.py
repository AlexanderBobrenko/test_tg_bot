import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def set_user_status(chat_id, status):
    redis_client.set(f'user:{chat_id}:status', status.encode('utf-8'))

def get_user_status(chat_id):
    status = redis_client.get(f'user:{chat_id}:status')
    return status.decode('utf-8') if status else None

def set_user_token(chat_id, token):
    redis_client.set(f'user:{chat_id}:token', token.encode('utf-8'))

def get_user_token(chat_id):
    token = redis_client.get(f'user:{chat_id}:token')
    return token.decode('utf-8') if token else None

def delete_user_session(chat_id):
    redis_client.delete(f'user:{chat_id}:status')
    redis_client.delete(f'user:{chat_id}:token')