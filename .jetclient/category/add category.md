```toml
name = 'add category'
method = 'POST'
url = '{{url}}/api/category/add-category/'
sortWeight = 1000000
id = 'a561f2b0-bafd-4994-9ab5-321b7353cb9b'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxNDI3MTY2LCJpYXQiOjE3NTEzNDA3NjYsImp0aSI6IjdhOWE5MWY0ZTcwZDQ2NjViOTU0NmViMjc1ODZkYjJmIiwidXNlcl9pZCI6ImMzZWI5NjE1LTg2ODUtNDI1OC04ZDJmLWQ3MjMzZGI3MTJkNiJ9.XP-VExj7BTw8UQuu8_NjV3f-gm98l-sKwaLQ6HDymkU'

[body]
type = 'JSON'
raw = '''
{
  "name": "Frontend Development"
}'''
```
