```toml
name = 'Get access token through Refersh token'
method = 'POST'
url = 'http://localhost:8000/api/auth/token/refresh/'
sortWeight = 9000000
id = '237844dd-cf5a-42e9-8d0f-38e74b45f799'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwNzMyNzU3LCJpYXQiOjE3NTA3MzI0NTcsImp0aSI6IjAxMTg0NGNhZjBiZDRhODZiYmQ3OTRjMDUyYzJlYzZlIiwidXNlcl9pZCI6IjliN2YzMmMyLThlYmQtNGI2NS1hMTA5LWRhYjU4NGNhNThmNiJ9.OXE7OARgHtaCXiejkJWW_05lAGW3Kvba1LVyc3wFzFg'
disabled = true

[body]
type = 'JSON'
raw = '''
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MDg0NzY4MSwiaWF0IjoxNzUwNzYxMjgxLCJqdGkiOiJiNGRjZjA0N2U5YTc0MTVlOWU0NzNjZGVjNzA3ZjgzZCIsInVzZXJfaWQiOiI2ODhkMzliMy1iNmMyLTQ1NTAtYjljMy1kMmUyMmYzNWMxYjUifQ.a-IrXMHMU8gDnUKLyO48m-cPBGaQRmrmvBLJSjf_VSQ",
}
'''
```
