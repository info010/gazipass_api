from enum import Enum

class AuthMessages(Enum):
    USER_REGISTERED = "User successfully created."
    USER_LOGINED = "User successfully logined."
    SUCCESSFULLY_GET_CURRENT_USER = "Successfully fetched current user."
    SUCCESSFULLY_LOGOUT = "Successfully logout."
    TOKEN_REFRESHED = "Token successfully refreshed."
    EMAIL_EXISTS = "Email or username already exists."
    USER_CREATION_FAILED = "User creation failed."
    WRONG_INFORMATION = "Wrong email or password"
    USER_NOT_FOUND = "User not found."
    TOKEN_NOT_FOUND = "Refresh token not found."
    REGISTER_ERROR = "Something went wrong while registering."
    LOGIN_ERROR = "Something went wrong while logining."
    ME_ERROR = "Something went wrong while get current user."
    LOGOUT_ERROR = "Something went wrong while logout current user.",
    REFRESH_ERROR = "Something went wrong while refresh access token."