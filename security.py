from werkzeug.security import safe_str_cmp
from models.user import UserModel #from user.py file, import UserModel class

# users = [
#     UserModel(1,"bob","asdf")
# ]

# username_mapping = {#using set comprehension
#     user.username: user for user in users
# }
# #results in:
# # username_mapping = {
# #     "bob": {
# #         "id": 1,
# #         "username": "bob",
# #         "password": "asdf"
# #     }
# # }

# userid_mapping = {
#     user.id: user for user in users
# }


def authenticate(username, password):
    #user = username_mapping.get(username, None)# none is a defualt value
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):# safer way of comparing strings than user.password == password
        return user

def identity(payload):
    user_id = payload["identity"]
    #return userid_mapping.get(user_id,None)
    return UserModel.find_by_id(user_id)