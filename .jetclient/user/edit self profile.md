```toml
name = 'edit self profile'
method = 'PUT'
url = 'http://localhost:8000/api/auth/user/edit/'
sortWeight = 5000000
id = '8c70fd9d-e004-4690-b0ad-8771f62b2591'

[[headers]]
key = 'Authorization'
value = 'Token 44435ed10d6fa74fc4d1c688bdad2475c75256e8'

[body]
type = 'JSON'
raw = '''
{
  "first_name": "Johnathan",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "username": "john_doe",
  "password": "securePass123",
  "password2": "securePass123"
}
'''
```
