from requests import get, put, post, delete
from pprint import pprint

response = delete(
    "http://127.0.0.1:5000/api/student/4/course/2",
).json()
pprint(response)

# response = get(
#     "http://127.0.0.1:5000/api/student/",
# ).json()
# pprint(response)
