# Non-Functional Requirements
## KIS – Krankenhausinformationssystem

**Version:** 1.0.0
**Date:** 2026-03-12
**Status:** Draft

---

## 1. Performance

| ID | Requirement |
|----|-------------|
| NFR-PER-01 | API responses shall be returned within 500 ms under normal load (up to 50 concurrent users). |
| NFR-PER-02 | The dashboard statistics endpoint shall respond within 1 second including all aggregated data. |
| NFR-PER-03 | Patient list and appointment list queries shall support pagination to limit response payload size. |
| NFR-PER-04 | The clinical summary endpoint shall return all patient clinical data within 1 second. |
| NFR-PER-05 | Database queries shall use `select_related()` and `prefetch_related()` where applicable to avoid N+1 query problems. |

---

## 2. Security

| ID | Requirement |
|----|-------------|
| NFR-SEC-01 | All API endpoints shall require authentication before access in production. |
| NFR-SEC-02 | Passwords shall be stored using a secure hashing algorithm (e.g., bcrypt or PBKDF2). |
| NFR-SEC-03 | The application shall protect against SQL injection by using parameterized queries via the ORM. |
| NFR-SEC-04 | The application shall protect against Cross-Site Request Forgery (CSRF) using CSRF tokens. |
| NFR-SEC-05 | The secret key shall never be stored in version control and shall be loaded from environment variables in production. |
| NFR-SEC-06 | CORS shall be restricted to known frontend origins in production (not `CORS_ALLOW_ALL_ORIGINS = True`). |
| NFR-SEC-07 | Debug mode shall be disabled in production (`DEBUG = False`). |
| NFR-SEC-08 | Patient data access shall be restricted based on user roles (e.g., doctor, nurse, administrator). |
| NFR-SEC-09 | All data transmission shall be encrypted via HTTPS in production. |

---

## 3. Usability

| ID | Requirement |
|----|-------------|
| NFR-USE-01 | The user interface shall be operable without prior technical training for standard hospital staff workflows. |
| NFR-USE-02 | Forms shall display inline validation errors clearly next to the relevant field. |
| NFR-USE-03 | Success and error feedback shall be provided within 300 ms of form submission. |
| NFR-USE-04 | The interface shall be responsive and usable on screens with a minimum width of 1024 px. |
| NFR-USE-05 | Navigation between modules shall require no more than two clicks from any page. |
| NFR-USE-06 | The system shall provide visual status indicators (colour coding) for bed status, appointment status, and lab result status. |
| NFR-USE-07 | All date inputs shall follow the DD.MM.YYYY format for German-speaking users. |

---

## 4. Reliability & Availability

| ID | Requirement |
|----|-------------|
| NFR-REL-01 | The system shall have a target uptime of 99.5% during operational hours (06:00–22:00). |
| NFR-REL-02 | The system shall handle unexpected errors gracefully and display user-friendly error messages. |
| NFR-REL-03 | No patient data shall be lost due to a single server failure; database backups shall be taken daily. |
| NFR-REL-04 | Database transactions shall be atomic; partial writes shall be rolled back on failure. |

---

## 5. Maintainability

| ID | Requirement |
|----|-------------|
| NFR-MAI-01 | The backend shall follow Django best practices with apps separated by domain (administrative, clinical). |
| NFR-MAI-02 | Each Django app shall have its own models, serializers, views, and URL configuration. |
| NFR-MAI-03 | Common patterns (e.g., `FilterByPatientMixin`) shall be extracted into reusable base classes. |
| NFR-MAI-04 | All models shall include a `created_at` timestamp for audit purposes. |
| NFR-MAI-05 | The codebase shall include inline comments for non-obvious logic. |
| NFR-MAI-06 | Database schema changes shall be managed via Django migrations with no manual SQL. |

---

## 6. Compatibility

| ID | Requirement |
|----|-------------|
| NFR-COM-01 | The backend shall run on Python 3.11 or higher. |
| NFR-COM-02 | The application shall use Django 6.0+ and Django REST Framework 3.15+. |
| NFR-COM-03 | The frontend shall function correctly in the latest versions of Chrome, Firefox, and Edge. |
| NFR-COM-04 | The REST API shall communicate using JSON (application/json). |
| NFR-COM-05 | The system shall be deployable on Linux-based server environments. |

---

## 7. Scalability

| ID | Requirement |
|----|-------------|
| NFR-SCA-01 | The system architecture shall support replacing SQLite with PostgreSQL for production without application code changes. |
| NFR-SCA-02 | The API shall be stateless to allow horizontal scaling behind a load balancer. |
| NFR-SCA-03 | The system shall support at least 10,000 patient records without degradation in list query performance. |
