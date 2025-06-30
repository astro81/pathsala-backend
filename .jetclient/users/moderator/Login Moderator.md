```toml
name = 'Login Moderator'
method = 'POST'
url = '{{url}}/api/auth/login/'
sortWeight = 1000000
id = '32e30ee3-09f7-42c1-aa33-75ac4128c001'

[body]
type = 'JSON'
raw = '''
{
  "username": "mod1",
  "password": "Mod@1234"
}'''
```
