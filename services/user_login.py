import bcrypt
from sqlalchemy.orm import Session
from database.models import UserLogin
from datetime import datetime


class UserLoginService:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, username: str, password: str):
        """Create a new user with hashed password."""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = UserLogin(
            id=username,  # or generate a UUID if you prefer
            username=username,
            password=hashed_password,
            created_at=datetime.now()
        )
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def authenticate_user(self, username: str, password: str) -> bool:
        """Check if username and password match."""
        user = self.get_user_by_username(username)
        if user is None:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))

    def update_last_login(self, username: str):
        """Update the last login time for the user."""
        user = self.get_user_by_username(username)
        if user:
            user.last_login = datetime.now()
            self.session.commit()

    def get_user_by_username(self, username: str):
        """Retrieve user by username."""
        return self.session.query(UserLogin).filter_by(username=username).first()
