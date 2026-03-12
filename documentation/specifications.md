# Technical Specifications
## KIS – Krankenhausinformationssystem

**Version:** 1.0.0
**Date:** 2026-03-12
**Status:** Draft

---

## 1. System Architecture

The KIS system follows a two-tier client-server architecture:

```
┌─────────────────────────────────┐
│         Frontend (Browser)      │
│  Vanilla JS · HTML · CSS        │
│  Tailwind CSS · Chart.js        │
│       port 3000                 │
└──────────────┬──────────────────┘
               │ HTTP / JSON REST API
┌──────────────▼──────────────────┐
│         Backend (Django)        │
│  Django 6.0 · Django REST FW    │
│  SQLite (dev) · Python 3.11     │
│       port 8000                 │
└──────────────┬──────────────────┘
               │ ORM
┌──────────────▼──────────────────┐
│           Database              │
│   SQLite (dev) / PostgreSQL     │
└─────────────────────────────────┘
```

### 1.1 Backend Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Language | Python | 3.11+ |
| Web Framework | Django | 6.0.3 |
| REST API | Django REST Framework | 3.15+ |
| Database (dev) | SQLite | built-in |
| Database (prod) | PostgreSQL | 15+ |
| CORS | django-cors-headers | 4.x |

### 1.2 Frontend Stack

| Component | Technology |
|-----------|-----------|
| Language | Vanilla JavaScript (ES2022) |
| Styling | Tailwind CSS (CDN) + custom CSS |
| Charts | Chart.js 4.4.0 |
| HTTP Client | Fetch API (native browser) |
| Architecture | Single-Page Application (SPA) |

---

## 2. Project Structure

```
kis/
├── kis_backend/
│   ├── administrative/
│   │   ├── models.py          # Patient, Appointment, Station, Bed
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── clinical/
│   │   ├── models.py          # 12 clinical models
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── kis_backend/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   └── db.sqlite3
├── kis_frontend/
│   └── index.html             # Single-page application
└── documentation/
    ├── functional-requirements.md
    ├── non-functional-requirements.md
    └── specifications.md
```

---

## 3. Data Models

### 3.1 Administrative Module

#### Patient
| Field | Type | Constraints |
|-------|------|-------------|
| id | AutoField | PK |
| first_name | CharField(100) | required |
| last_name | CharField(100) | required |
| date_of_birth | DateField | required |
| gender | CharField(10) | choices: male, female, diverse |
| address | CharField(200) | optional |
| phone | CharField(30) | optional |
| email | EmailField | optional |
| insurance_number | CharField(50) | optional |
| insurance_provider | CharField(100) | optional |
| created_at | DateTimeField | auto |

#### Appointment
| Field | Type | Constraints |
|-------|------|-------------|
| id | AutoField | PK |
| patient | FK → Patient | CASCADE |
| date | DateField | required |
| time | TimeField | required |
| reason | CharField(255) | required |
| doctor | CharField(100) | optional |
| status | CharField(20) | choices: scheduled, completed, cancelled |
| notes | TextField | optional |
| created_at | DateTimeField | auto |

#### Station
| Field | Type | Constraints |
|-------|------|-------------|
| id | AutoField | PK |
| name | CharField(100) | required |
| description | TextField | optional |
| floor | CharField(50) | optional |

#### Bed
| Field | Type | Constraints |
|-------|------|-------------|
| id | AutoField | PK |
| station | FK → Station | CASCADE |
| bed_number | CharField(20) | required |
| room | CharField(50) | optional |
| status | CharField(20) | choices: free, occupied, reserved, maintenance |
| patient | FK → Patient | SET_NULL, optional |

### 3.2 Clinical Module

#### Admission
| Field | Type | Constraints |
|-------|------|-------------|
| id | AutoField | PK |
| patient | FK → Patient | CASCADE |
| bed | FK → Bed | SET_NULL, optional |
| admission_date | DateField | required |
| discharge_date | DateField | optional |
| discharge_type | CharField(20) | choices: home, transfer, deceased, other |
| reason | CharField(255) | required |
| notes | TextField | optional |
| is_active | @property | True if discharge_date is None |

#### Diagnosis
| Field | Type | Constraints |
|-------|------|-------------|
| patient | FK → Patient | CASCADE |
| admission | FK → Admission | SET_NULL, optional |
| icd_code | CharField(20) | required |
| description | CharField(255) | required |
| type | CharField(20) | choices: primary, secondary, admission |
| status | CharField(20) | choices: active, resolved, chronic |
| doctor | CharField(100) | optional |
| date | DateField | required |

#### Prescription
| Field | Type | Constraints |
|-------|------|-------------|
| patient | FK → Patient | CASCADE |
| admission | FK → Admission | SET_NULL, optional |
| drug_name | CharField(150) | required |
| dosage | CharField(50) | required |
| unit | CharField(30) | required |
| frequency | CharField(100) | required |
| route | CharField(20) | choices: oral, iv, im, topical, inhaled, other |
| start_date | DateField | required |
| end_date | DateField | optional |
| status | CharField(20) | choices: active, discontinued, completed |

#### LabResult
| Field | Type | Constraints |
|-------|------|-------------|
| patient | FK → Patient | CASCADE |
| admission | FK → Admission | SET_NULL, optional |
| test_name | CharField(150) | required |
| value | CharField(50) | required |
| unit | CharField(30) | optional |
| reference_range | CharField(50) | optional |
| status | CharField(20) | choices: normal, elevated, low, critical |
| sample_date | DateField | required |
| result_date | DateField | optional |
| ordering_doctor | CharField(100) | optional |

#### VitalSigns
| Field | Type | Constraints |
|-------|------|-------------|
| patient | FK → Patient | CASCADE |
| admission | FK → Admission | SET_NULL, optional |
| timestamp | DateTimeField | required |
| systolic_bp | IntegerField | optional (mmHg) |
| diastolic_bp | IntegerField | optional (mmHg) |
| heart_rate | IntegerField | optional (bpm) |
| temperature | DecimalField(4,1) | optional (°C) |
| oxygen_sat | DecimalField(5,1) | optional (%) |
| weight | DecimalField(5,1) | optional (kg) |
| height | DecimalField(5,1) | optional (cm) |
| bmi | @property | calculated from weight/height |
| measured_by | CharField(100) | optional |

#### Allergy
| Field | Type | Constraints |
|-------|------|-------------|
| patient | FK → Patient | CASCADE |
| substance | CharField(150) | required |
| reaction | CharField(255) | optional |
| severity | CharField(20) | choices: mild, moderate, severe |
| noted_at | DateField | required |

#### PreExistingCondition
| Field | Type | Constraints |
|-------|------|-------------|
| patient | FK → Patient | CASCADE |
| name | CharField(200) | required |
| icd_code | CharField(20) | optional |
| since | DateField | optional |
| notes | TextField | optional |

#### Surgery
| Field | Type | Constraints |
|-------|------|-------------|
| patient | FK → Patient | CASCADE |
| procedure | CharField(255) | required |
| ops_code | CharField(20) | optional |
| date | DateField | required |
| hospital | CharField(150) | optional |
| surgeon | CharField(100) | optional |

#### ClinicalNote
| Field | Type | Constraints |
|-------|------|-------------|
| patient | FK → Patient | CASCADE |
| admission | FK → Admission | SET_NULL, optional |
| appointment | FK → Appointment | SET_NULL, optional |
| note_type | CharField(20) | choices: initial, followup, discharge, consultation, other |
| content | TextField | required |
| author | CharField(100) | required |
| created_at | DateTimeField | auto |

#### Procedure
| Field | Type | Constraints |
|-------|------|-------------|
| patient | FK → Patient | CASCADE |
| admission | FK → Admission | SET_NULL, optional |
| name | CharField(255) | required |
| ops_code | CharField(20) | optional |
| date | DateField | required |
| doctor | CharField(100) | optional |

#### Referral
| Field | Type | Constraints |
|-------|------|-------------|
| patient | FK → Patient | CASCADE |
| admission | FK → Admission | SET_NULL, optional |
| referring_doctor | CharField(100) | required |
| specialist | CharField(100) | required |
| specialty | CharField(100) | optional |
| reason | CharField(255) | required |
| date | DateField | required |
| status | CharField(20) | choices: pending, completed, cancelled |
| result_notes | TextField | optional |

#### DischargeLetter
| Field | Type | Constraints |
|-------|------|-------------|
| patient | FK → Patient | CASCADE |
| admission | OneToOneField → Admission | CASCADE |
| diagnosis_summary | TextField | required |
| treatment_summary | TextField | required |
| followup_instructions | TextField | optional |
| medication_on_discharge | TextField | optional |
| author | CharField(100) | required |
| created_at | DateTimeField | auto |

---

## 4. REST API Endpoints

Base URL: `http://localhost:8000`

### 4.1 Administrative

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/patients/` | List all patients |
| POST | `/api/patients/` | Create patient |
| GET | `/api/patients/{id}/` | Retrieve patient with appointments |
| PUT/PATCH | `/api/patients/{id}/` | Update patient |
| DELETE | `/api/patients/{id}/` | Delete patient |
| GET | `/api/appointments/` | List appointments (`?date=`, `?month=YYYY-MM`, `?week=YYYY-WNN`) |
| POST | `/api/appointments/` | Create appointment |
| GET | `/api/appointments/{id}/` | Retrieve appointment |
| PUT/PATCH | `/api/appointments/{id}/` | Update appointment |
| DELETE | `/api/appointments/{id}/` | Delete appointment |
| GET | `/api/stations/` | List stations with bed counts |
| POST | `/api/stations/` | Create station |
| GET | `/api/stations/{id}/` | Retrieve station with nested beds |
| GET | `/api/beds/` | List all beds |
| POST | `/api/beds/` | Create bed |
| PATCH | `/api/beds/{id}/` | Update bed status / patient assignment |
| GET | `/api/dashboard-stats/` | Dashboard aggregate statistics |

### 4.2 Clinical

All clinical endpoints support `?patient={id}` filter. Most also support `?admission={id}`.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/clinical/admissions/` | List / create admissions |
| GET/PATCH | `/api/clinical/admissions/{id}/` | Retrieve / update admission |
| GET/POST | `/api/clinical/diagnoses/` | List / create diagnoses |
| GET/POST | `/api/clinical/prescriptions/` | List / create prescriptions |
| GET/POST | `/api/clinical/lab-results/` | List / create lab results |
| GET/POST | `/api/clinical/vital-signs/` | List / create vital signs |
| GET/POST | `/api/clinical/allergies/` | List / create allergies |
| GET/POST | `/api/clinical/conditions/` | List / create pre-existing conditions |
| GET/POST | `/api/clinical/surgeries/` | List / create surgeries |
| GET/POST | `/api/clinical/notes/` | List / create clinical notes |
| GET/POST | `/api/clinical/procedures/` | List / create procedures |
| GET/POST | `/api/clinical/referrals/` | List / create referrals |
| GET/POST | `/api/clinical/discharge-letters/` | List / create discharge letters |
| GET | `/api/clinical/patients/{id}/summary/` | All clinical data for one patient |

### 4.3 Dashboard Stats Response Schema

```json
{
  "total_patients": 120,
  "todays_appointments": 8,
  "open_appointments": 14,
  "total_beds": 60,
  "free_beds": 22,
  "upcoming_appointments": [
    {
      "id": 1,
      "patient_name": "Max Mustermann",
      "date": "2026-03-12",
      "time": "09:00:00",
      "reason": "Blutabnahme",
      "doctor": "Dr. Schneider",
      "status": "scheduled"
    }
  ]
}
```

---

## 5. Frontend Architecture

The frontend is a single-page application (SPA) contained in a single `index.html` file.

### 5.1 Navigation Pattern

```javascript
const PAGES = ['dashboard', 'calendar', 'patients', ...];

function showPage(id) {
    PAGES.forEach(p => document.getElementById(p).classList.add('hidden'));
    document.getElementById(id).classList.remove('hidden');
    // Trigger data loading per page
}
```

### 5.2 API Base URLs

```javascript
const API = 'http://127.0.0.1:8000/api';
const CLIN_API = 'http://127.0.0.1:8000/api/clinical';
```

### 5.3 Clinical Summary

The clinical summary page loads all data in a single API call and renders 11 tabs:

```javascript
async function loadClinicalSummary(patientId) {
    const data = await fetch(`${CLIN_API}/patients/${patientId}/summary/`).then(r => r.json());
    // Renders: admissions, diagnoses, prescriptions, labResults,
    //          vitalSigns, allergies, conditions, surgeries,
    //          notes, procedures, referrals
}
```

### 5.4 Page Inventory

| Page ID | Description |
|---------|-------------|
| dashboard | Statistics cards, bed chart, upcoming appointments |
| calendar | Month / week / day appointment calendar |
| patients | Searchable patient list |
| new-patient | Create patient form |
| new-appointment | Create appointment form |
| stations | Station grid with bed status |
| new-station | Create station & bed form |
| clinical | Patient clinical summary (tabbed) |
| new-admission | Create admission form |
| new-diagnosis | Create diagnosis form |
| new-prescription | Create prescription form |
| new-lab | Create lab result form |
| new-vitals | Create vital signs form |
| new-allergy | Create allergy form |
| new-condition | Create pre-existing condition form |
| new-surgery | Create surgery form |
| new-note | Create clinical note form |
| new-procedure | Create procedure form |
| new-referral | Create referral form |
| new-discharge | Create discharge letter form |

---

## 6. Development Setup

### 6.1 Backend

```bash
cd kis_backend
python3 -m venv venv
source venv/bin/activate
pip install django djangorestframework django-cors-headers
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### 6.2 Frontend

```bash
cd kis_frontend
python3 -m http.server 3000
# Open http://localhost:3000
```

---

## 7. Known Limitations (Development Version)

- Authentication is not implemented; all endpoints are publicly accessible.
- SQLite is used as the database; not suitable for concurrent production use.
- `CORS_ALLOW_ALL_ORIGINS = True` allows any origin; must be restricted in production.
- `DEBUG = True` exposes detailed error pages; must be disabled in production.
- The frontend is served as a static file; no build toolchain (no bundler, no TypeScript).
