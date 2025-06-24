```toml
name = 'logout'
method = 'POST'
url = 'http://localhost:8000/api/auth/logout/'
sortWeight = 3000000
id = '065f1ddf-9a61-4abb-87d6-c04f55134250'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwNzYyOTgzLCJpYXQiOjE3NTA3NjI2ODMsImp0aSI6Ijc5NGM0NzRmZThiYjQ3ZWE4YjE0YTgwMGJhMDg2NmVlIiwidXNlcl9pZCI6ImM0ZjNlOGNmLWE0ZjgtNDNiYS05OGE4LWZkNTRlMzBhNmE5OSJ9.6OfyfRmbg3ufYVwXSQwgA-0DdS0we6YSCx1gr7DJpKk'

[body]
type = 'JSON'
raw = '''
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MDg0OTA4MywiaWF0IjoxNzUwNzYyNjgzLCJqdGkiOiJkNGYyYTU2OTkxYTc0NjkxODU0NzQ0YjIwMGYyYjg1YiIsInVzZXJfaWQiOiJjNGYzZThjZi1hNGY4LTQzYmEtOThhOC1mZDU0ZTMwYTZhOTkifQ.XgSyuJEkcSNmUQvqWw7gZAD8iaCSSXipN3Jtcr4huGA"
}'''
```
