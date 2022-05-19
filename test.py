from database_functions import *

# user = get_company("6989")
# if len(user) > 0:
#     password = user[0][2]

users_raw = get_company_IDs()
users = [u[0] for u in users_raw]
passwords = [get_company(u)[0][2] for u in users]
print(users)
print(passwords)

