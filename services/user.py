import database
from schemas.user import UserCreate, User

class UserService:
  def __init__(self, db):
    self.db = db

  def get_user(self, user_id: int):
    return self.db.query(database.user.User).filter(database.user.User.id == user_id).first()


  def get_user_by_email(self, email: str):
      return self.db.query(database.user.User).filter(database.user.User.email == email).first()


  def get_users(self, skip: int = 0, limit: int = 100):
      return self.db.query(database.user.User).offset(skip).limit(limit).all()


  def create_user(self, user: UserCreate):
      fake_hashed_password = user.password + "notreallyhashed"
      db_user = database.user.User(email=user.email, password=fake_hashed_password)
      self.db.add(db_user)
      self.db.commit()
      self.db.refresh(db_user)

  def update_user(self, user_id: int, user: UserCreate):
      result = self.get_user(user_id=user_id)
      result.email = user.email
      result.password = user.password
      self.db.commit()
      self.db.refresh(result)
      return result

  def delete_user(self, user_id: int):
      result = self.get_user(user_id=user_id)
      self.db.delete(result)
      self.db.commit()
      return result