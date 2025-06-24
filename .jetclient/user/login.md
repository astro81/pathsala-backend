```toml
name = 'login'
method = 'POST'
url = 'http://localhost:8000/api/auth/login/'
sortWeight = 2000000
id = '2f231e11-bbee-425d-956c-ae180ceb2f77'

[body]
type = 'JSON'
raw = '''
{
  "username": "admin",
  "password": "12345678"
}
'''
```
