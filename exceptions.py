from fastapi import HTTPException, status

NOT_ALLOWED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User not allowed to perform this action",
    headers={"WWW-Authenticate": "Bearer"},
)
