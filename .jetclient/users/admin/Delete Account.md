```toml
name = 'Delete Account'
description = '- Soft Delete others account'
method = 'DELETE'
url = '{{url}}/api/auth/admin/delete/temporary/51b1f968-e264-42af-821b-d8a7502e13d4/'
sortWeight = 6000000
id = '5d45bba4-deb4-4cd2-b7f2-34d4b16ed715'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxNDI3MTY2LCJpYXQiOjE3NTEzNDA3NjYsImp0aSI6IjdhOWE5MWY0ZTcwZDQ2NjViOTU0NmViMjc1ODZkYjJmIiwidXNlcl9pZCI6ImMzZWI5NjE1LTg2ODUtNDI1OC04ZDJmLWQ3MjMzZGI3MTJkNiJ9.XP-VExj7BTw8UQuu8_NjV3f-gm98l-sKwaLQ6HDymkU'

[body]
type = 'JSON'
raw = '''
{
  "username" : "test3"
}'''
```
