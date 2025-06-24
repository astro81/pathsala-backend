```toml
name = 'register'
method = 'POST'
url = 'http://localhost:8000/api/auth/register/'
sortWeight = 1000000
id = '51e7bd75-2481-46b6-b714-9bc172a4b51e'

[body]
type = 'JSON'
raw = '''
{
  "username": "pathsala",
  "email": "pathsala@gmail.com",
  "password": "securePass@321",
  "password2": "securePass@321",
  "first_name": "path",
  "last_name": "sala",
  "address": "123 Street, City",
  "phone_no": "+997-981234567"
}
'''
```
