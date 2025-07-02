```toml
name = 'register'
method = 'POST'
url = '{{url}}/api/auth/register/student/'
sortWeight = 1000000
id = 'a1ebd693-d67e-4e90-84c1-8f40996d3b1a'

[body]
type = 'JSON'
raw = '''
{
    "username": "test11",
    "email": "test11@example.com",
    "password": "StrongPass!23",
    "password2": "StrongPass!23",
    "first_name": "John",
    "last_name": "Student",
    "address": "123 Campus Rd",
    "phone_no": "+1234567890",
    "profile_picture": null,
  
}
'''
```
