# Временный файл для аутентификации
# Будет дополнен во втором спринте

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Заглушка для функции получения текущего пользователя
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Временная заглушка
    return {"id": 1, "username": "test_user", "role": "customer"}
