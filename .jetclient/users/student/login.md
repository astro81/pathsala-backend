```toml
name = 'login'
description = 'login the student by entering username and password and get auth tokens'
method = 'POST'
url = '{{url}}/api/auth/login/'
sortWeight = 2000000
id = '3169c91c-f3b2-4ce3-a63d-b23b14fbacf9'

[body]
type = 'JSON'
raw = '''
{
  "username": "test1",
  "password": "StrongPass!23"
}'''
```
