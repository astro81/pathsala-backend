```toml
name = 'add course'
method = 'POST'
url = 'http://127.0.0.1:8000/api/courses/add-course/'
sortWeight = 2000000
id = '53c86376-5da4-4fe3-b68d-a794ee016325'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwODU2ODk4LCJpYXQiOjE3NTA4NTY1OTgsImp0aSI6ImZmZjA5MTI1M2ExNDRiNzA5ZmVmODYxMTAwYWQwYTQxIiwidXNlcl9pZCI6IjUxNmNlZGRmLWY0MmYtNDM4OS1iMGExLWM4YjQ1ODY3ZDBhNyJ9.GxVg89H2-ixXquplWVpfEBF9_XNRWxA0dAkfbcDhcfE'

[body]
type = 'JSON'
raw = '''
{
  "name": "devops-engineering-2024",
  "title": "Modern DevOps Engineering Bootcamp",
  "duration_value": 6,
  "duration_unit": "months",
  "price": "15000.00",
  "rating": 4.6,
  "training_level": "intermediate",
  "class_type": "online",
  "career_prospect": "DevOps Engineer | Site Reliability Engineer | Cloud Architect",
  "description": {
    "course_introduction": "Master CI/CD pipelines, infrastructure as code, and cloud-native tooling",
    "course_overview": "Hands-on training with Docker, Kubernetes, Terraform, and AWS/GCP",
    "course_requirements": "Linux basics and fundamental programming concepts",
    "course_context": "For software engineers transitioning to DevOps roles"
  },
  "syllabus": {
    "title": "DevOps Engineering Curriculum",
    "syllabus_title_indexing": 8,
    "title_content": [
      {
        "title_content": "Linux & Shell Scripting",
        "syllabus_title_content_indexing": 1,
        "details": "Advanced bash, system administration, process management"
      },
      {
        "title_content": "Containerization with Docker",
        "syllabus_title_content_indexing": 2,
        "details": "Image creation, Dockerfiles, multi-stage builds"
      },
      {
        "title_content": "Kubernetes Orchestration",
        "syllabus_title_content_indexing": 3,
        "details": "Pods, deployments, services, helm charts"
      },
      {
        "title_content": "Infrastructure as Code",
        "syllabus_title_content_indexing": 4,
        "details": "Terraform modules, state management, cloud provisioning"
      },
      {
        "title_content": "CI/CD Pipelines",
        "syllabus_title_content_indexing": 5,
        "details": "GitHub Actions, ArgoCD, Jenkins configuration"
      },
      {
        "title_content": "Cloud Monitoring",
        "syllabus_title_content_indexing": 6,
        "details": "Prometheus, Grafana, ELK stack implementation"
      }
    ]
  }
}'''
```
