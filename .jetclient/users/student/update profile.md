```toml
name = 'update profile'
description = '- partially update the student details '
method = 'PATCH'
url = '{{url}}/api/auth/update/student/profile/'
sortWeight = 6000000
id = 'f6e20d8a-8c77-4dda-bb80-7a00874b77ce'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxNDMyODkxLCJpYXQiOjE3NTEzNDY0OTEsImp0aSI6ImU4MzZmOGJjMTFiNzQ1NWViZDljMDYyZTgyNGMxM2I5IiwidXNlcl9pZCI6IjUxYjFmOTY4LWUyNjQtNDJhZi04MjFiLWQ4YTc1MDJlMTNkNCJ9.89OUl8fWIQswFrX8rpFLcMMylW24ML5MmL2hsD1e5dU'

[[body.formData]]
type = 'FILE'
key = 'profile_picture'
value = 'C:\Users\Acer\OneDrive\Pictures\Screenshots\Screenshot_2024-11-27-18-30-12-633_com.android.chrome.jpg'
```
