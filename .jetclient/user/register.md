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
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securePass123",
  "password2": "securePass123",
  "first_name": "John",
  "last_name": "Doe",
  "address": "123 Street, City",
  "phone_no": "+997-981234567"
}
'''
```
