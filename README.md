# Django Modular Entity & Mapping System

A Django REST Framework backend for managing **Vendors, Products, Courses, Certifications** and their mappings, built entirely with `APIView` and documented via `drf-yasg`.

---

## Project Structure

```
django_intern_project/
│
├── core/                            # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── utils.py                         # Shared: BaseModel, helpers
│
├── vendor/                          # Master app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── tests.py
│   └── management/commands/seed_data.py
│
├── product/                         # Master app
├── course/                          # Master app
├── certification/                   # Master app
│
├── vendor_product_mapping/          # Mapping app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── product_course_mapping/          # Mapping app
├── course_certification_mapping/    # Mapping app
│
├── requirements.txt
└── manage.py
```

---

## Setup Steps

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd django_intern_project
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py makemigrations vendor product course certification \
    vendor_product_mapping product_course_mapping course_certification_mapping
python manage.py migrate
```

### 5. Create superuser (for admin panel)

```bash
python manage.py createsuperuser
```

### 6. Seed sample data

```bash
python manage.py seed_data
```

### 7. Run the development server

```bash
python manage.py runserver
```

---

## Installed Apps

| App | Type |
|-----|------|
| `vendor` | Master |
| `product` | Master |
| `course` | Master |
| `certification` | Master |
| `vendor_product_mapping` | Mapping |
| `product_course_mapping` | Mapping |
| `course_certification_mapping` | Mapping |

---

## API Documentation

| URL | Description |
|-----|-------------|
| `http://localhost:8000/swagger/` | Swagger UI |
| `http://localhost:8000/redoc/` | ReDoc UI |
| `http://localhost:8000/swagger.json` | Raw OpenAPI schema |

---

## API Endpoints

### Master Entities

| Method | URL | Action |
|--------|-----|--------|
| GET | `/api/vendors/` | List vendors |
| POST | `/api/vendors/` | Create vendor |
| GET | `/api/vendors/<id>/` | Retrieve vendor |
| PUT | `/api/vendors/<id>/` | Full update |
| PATCH | `/api/vendors/<id>/` | Partial update |
| DELETE | `/api/vendors/<id>/` | Soft delete |

_(Same pattern for `/api/products/`, `/api/courses/`, `/api/certifications/`)_

### Mapping Endpoints

| Method | URL | Action |
|--------|-----|--------|
| GET/POST | `/api/vendor-product-mappings/` | List / Create |
| GET/PUT/PATCH/DELETE | `/api/vendor-product-mappings/<id>/` | Detail ops |
| GET/POST | `/api/product-course-mappings/` | List / Create |
| GET/PUT/PATCH/DELETE | `/api/product-course-mappings/<id>/` | Detail ops |
| GET/POST | `/api/course-certification-mappings/` | List / Create |
| GET/PUT/PATCH/DELETE | `/api/course-certification-mappings/<id>/` | Detail ops |

---

## Query Parameters (Filtering)

| Endpoint | Param | Example |
|----------|-------|---------|
| Any list | `is_active` | `?is_active=true` |
| Master list | `search` | `?search=alpha` |
| `/api/vendor-product-mappings/` | `vendor_id`, `product_id` | `?vendor_id=1` |
| `/api/product-course-mappings/` | `product_id`, `course_id` | `?product_id=2` |
| `/api/course-certification-mappings/` | `course_id`, `certification_id` | `?course_id=3` |
| Any mapping list | `primary_mapping` | `?primary_mapping=true` |

---

## Validation Rules

- `name` and `code` are required on all master entities
- `code` must be **unique** per entity type
- Duplicate `(parent, child)` mapping pairs are rejected
- Only **one `primary_mapping=True`** is allowed per parent entity at each mapping level
- All FKs are validated automatically by DRF

---

## Response Format

All responses follow a consistent envelope:

```json
// Success
{ "success": true, "data": { ... } }

// Error
{ "success": false, "errors": { "field": ["message"] } }

// Not found
{ "detail": "Vendor with id=999 not found." }
```

---

## Soft Delete

DELETE endpoints do **not** remove records from the database. They set `is_active = False`. Filter active records with `?is_active=true`.

---

## Running Tests

```bash
python manage.py test vendor vendor_product_mapping
```

---

## Tech Stack

- Python 3.10+
- Django 4.2
- Django REST Framework 3.14
- drf-yasg 1.21
- SQLite (default, swap for PostgreSQL in production)
