from flask import session
from functools import wraps

def check_logged_in(func):
  @wraps(func)
  def wrapper(*args, **kwargs) -> bool:
    if "logged_in" in session:
      return func(*args, **kwargs)
    return str(False)
  
  return wrapper