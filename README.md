# Job Board API (Django REST + JWT + Celery)

A backend API for a job board platform with employer and applicant roles. Built using Django REST Framework, JWT auth, Celery (for async tasks), PostgreSQL, and Docker.


## 🚀 Features

- 👥 User registration & login with roles: `employer` and `applicant`
- 🔐 JWT Authentication
- 💼 Employers can post jobs and review applicants
- 📝 Applicants can apply to jobs and track their applications
- ✉️ Email notifications on application submissions (via Celery)
- 🧹 Automated cleanup of expired jobs (Celery Beat)
- 🐳 Dockerized for consistent local development
- 📬 Async job processing using Redis + Celery
- ✅ Custom permissions (e.g., IsEmployer, IsApplicant)

## 🧱 Project Structure (Key Components)

```plaintext
├── jobboard/
│   ├── settings.py            # Django settings incl. Celery setup
│   ├── celery.py              # Celery app config
│   ├── urls.py                # Project-wide URL routing
├── jobs/                      # App for job board logic
│   ├── models.py              # Job, Application, Profile models
│   ├── views.py               # Views for jobs and applications
│   ├── urls.py                # App-specific routing
│   ├── tasks.py               # Celery tasks (email, cleanup)
│   ├── permissions.py         # Custom permissions (IsEmployer, IsApplicant)
│   ├── signals.py             # Auto-creates Profile on user creation
│   └── serializers/           # Modularized serializers
│       ├── __init__.py
│       ├── application.py
│       ├── job.py
│       ├── profile.py
│       └── user.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
```

## 📦 Tech Stack

- Python 3, Django, Django REST Framework
- JWT (SimpleJWT)
- PostgreSQL
- Celery + Redis
- Docker, Docker Compose
- Django Signals
- Celery Beat (scheduled tasks)


## 🐳 Getting Started (Docker)

### 1. Clone the repository

```bash
git clone https://github.com/kkig/job-board-api.git
cd job-board-apic
```

### 2. Create a .env file
```bash
cp .env.example .env
# Then, update credentials like DB name, user, password
```

### 3. Build and start containers

```bash
docker-compose up --build
```

### 4. Apply migrations & create superuser

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### 5. Access the app
```
# API: http://localhost:8000/api/
# Admin: http://localhost:8000/admin/
```

## 🔁 Background Tasks (Celery + Redis)
- Celery worker: Handles async tasks (e.g., email)
- Celery Beat: Periodically marks jobs older than 30 days as expired

Start them in Docker:
```
docker-compose up celery
docker-compose up celery-beat
```

## ⏰ Scheduled Cleanup (Celery Beat)

Jobs older than 30 days are marked as expired automatically.  
This is managed by a Celery Beat task (`mark_expired_jobs`) and requires the `django-celery-beat` package.

## 📌 API Endpoints

### 🔐 Authentication & User

- **POST** `/api/register/`  
  Register a new user.  
  **Required fields**:  
  - `username` (string)  
  - `password` (string)  
  - `email` (string)  
  - `role` (`applicant` or `employer`)  

- **POST** `/api/token/`  
  Obtain JWT access and refresh tokens.  
  **Required fields**:  
  - `username`  
  - `password`  

- **GET** `/api/profile/`  
  Get the authenticated user’s profile.  
  **Returns**:  
  - `username`  
  - `email`  
  - `role`


---

### 💼 Jobs

- **GET** `/api/jobs/`  
  List all available jobs.  
  **Returns**:
  ```json
  [
    {
      "id": 1,
      "title": "Backend Developer",
      "description": "Build APIs...",
      "company": "Ack Corp",
      "location": "Remote",
      "job_type": "FT",
      "posted_at": "2024-05-01T12:34:56Z",
      "created_by": 3,
      "is_expired": false
    }
  ]
  ```

- **GET** `/api/my-jobs/`  _(Employer only)_  
    List jobs created by the currently logged-in employer. 
- **POST** `/api/jobs/` _(Employer only)_  
Create a new job.  
  **Required fields**:  
  - `title` 
  - `description` 
  - `company` 
  - `location` 
  - `job_type`

- **POST** `/api/jobs/` _(Employer only)_  
  Create a new job.  
  **Required fields**:
  - `title`
  - `description`
  - `company`
  - `location`
  - `job_type`

---

### 📄 Applications
- **POST** `/api/jobs/<id>/apply/` 
  _(Applicant only)_  
  Apply to a job. (Resume upload not implemented yet)  
  **Required fields**:  
  - `cover_letter`

- **GET** `/api/my-applications/` _(Applicant only)_  
  View all jobs the current applicant has applied to.

- **GET** `/api/jobs/<id>/applicants/` _(Employer only)_  
  View all applicants for a specific job posting.

- **PATCH** `/api/jobs/<id>/update_status/` _(Employer only)_  
  Update an applicant’s status for a job.  
  **Required fields**:
  - `application_id` (int)
  - `status`: one of `pending`, `accepted`, `rejected`

## 🔐 Permissions Summary
| Endpoint                              | Role      | Auth Required |
| ------------------------------------- | --------- | ------------- |
| `POST /api/register/`                 | Any       | ❌             |
| `POST /api/token/`                    | Any       | ❌             |
| `GET /api/profile/`                   | Any       | ✅             |
| `GET /api/jobs/`                      | Any       | ❌             |
| `GET /api/my-jobs/`                   | Employer  | ✅             |
| `POST /api/jobs/`                     | Employer  | ✅             |
| `POST /api/jobs/<id>/apply/`          | Applicant | ✅             |
| `GET /api/my-applications/`           | Applicant | ✅             |
| `GET /api/jobs/<id>/applicants/`      | Employer  | ✅             |
| `PATCH /api/jobs/<id>/update_status/` | Employer  | ✅             |


## 🧑‍💻 Author

kkig — [GitHub](https://github.com/kkig)  
Built as a hands-on full-stack backend project to demonstrate Django, Celery, and REST API design.


## 📜 License

MIT
