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
  "id": "6119be9f-9u11-45fa-92c8-3022f6833176",
  "username": "h123",
  "email": "hack@gmail.com",
  "password": "securePass123",
  "password2": "securePass123",
  "first_name": "aship",
  "last_name": "aalam",
  "address": "123 Street, City",
  "phone_no": "+997-981234567"
}
'''
```
