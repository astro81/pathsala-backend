```toml
name = 'logout'
method = 'POST'
url = 'http://localhost:8000/api/auth/logout/'
sortWeight = 3000000
id = '065f1ddf-9a61-4abb-87d6-c04f55134250'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwNzM3MzU3LCJpYXQiOjE3NTA3MzcwNTcsImp0aSI6ImQ3ODM4MGNkNzQ3ZDRhZWRiNGIzMGZjYWE3NmZlYTQ2IiwidXNlcl9pZCI6IjI1NWJhZTgzLWM1MDEtNDAzOS05ZTEwLWE2ODVmZDc0ZjY4YSJ9.IfZPdEsvTIPdyPet-BzzZYp5GheLGBJhngzc9r2x3PA'

[body]
type = 'JSON'
raw = '''
{
  "refresh" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MDgyMzQ1NywiaWF0IjoxNzUwNzM3MDU3LCJqdGkiOiJjYWYwMDdmM2I2ODU0ZjYxYjUyOTE0ODBmNGEyN2E2NyIsInVzZXJfaWQiOiIyNTViYWU4My1jNTAxLTQwMzktOWUxMC1hNjg1ZmQ3NGY2OGEifQ.TSPnMxysR1r-j8qZhHJfZDmsh4dNTfwU8ZUZt_LhtZE"
}'''
```
