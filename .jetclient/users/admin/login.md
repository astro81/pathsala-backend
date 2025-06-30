```toml
name = 'login'
description = '- login the admin which is create via script'
method = 'POST'
url = '{{url}}/api/auth/login/'
sortWeight = 1000000
id = 'ffd2206e-8e7c-4003-9de6-e77e8ddabcb5'

[body]
type = 'JSON'
raw = '''
{
  "username": "admin",
  "password": "1234"
  
//  "username": "mod1",
//  "password": "Mod@1234"
}'''
```
