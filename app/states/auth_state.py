import reflex as rx
from typing import Optional


class AuthState(rx.State):
    """Handles authentication logic and user state."""

    _user_db: dict[str, str] = {"admin": "password123"}
    username: str = ""
    password: str = ""
    confirm_password: str = ""
    is_authenticated: bool = False
    current_user: str = ""
    auth_error: str = ""

    def _validate_password(self, pwd: str) -> bool:
        return len(pwd) >= 6

    @rx.event
    def set_username(self, value: str):
        self.username = value
        self.auth_error = ""

    @rx.event
    def set_password(self, value: str):
        self.password = value
        self.auth_error = ""

    @rx.event
    def set_confirm_password(self, value: str):
        self.confirm_password = value
        self.auth_error = ""

    @rx.event
    def login(self):
        """Authenticates the user."""
        if not self.username or not self.password:
            self.auth_error = "Please enter both username and password."
            return
        stored_password = self._user_db.get(self.username)
        if stored_password and stored_password == self.password:
            self.is_authenticated = True
            self.current_user = self.username
            self.auth_error = ""
            self.password = ""
            return rx.redirect("/")
        else:
            self.auth_error = "Invalid username or password."

    @rx.event
    def register(self):
        """Registers a new user."""
        if not self.username or not self.password:
            self.auth_error = "All fields are required."
            return
        if self.username in self._user_db:
            self.auth_error = "Username already exists."
            return
        if len(self.password) < 6:
            self.auth_error = "Password must be at least 6 characters."
            return
        if self.password != self.confirm_password:
            self.auth_error = "Passwords do not match."
            return
        self._user_db[self.username] = self.password
        self.is_authenticated = True
        self.current_user = self.username
        self.auth_error = ""
        self.password = ""
        self.confirm_password = ""
        return rx.redirect("/")

    @rx.event
    def logout(self):
        """Logs out the user."""
        self.is_authenticated = False
        self.current_user = ""
        self.username = ""
        self.password = ""
        return rx.redirect("/")

    @rx.event
    def check_login(self):
        """Checks if user is logged in on page load."""
        pass