# Functional Requirements
## KIS – Krankenhausinformationssystem

**Version:** 1.0.0
**Date:** 2026-02-12
**Status:** Draft

---

## 1. Administrative Module

### 1.1 Patient Management

| ID | Requirement |
|----|-------------|
| FR-ADM-01 | The system shall allow creating new patient records with mandatory fields: first name, last name, date of birth, and gender. |
| FR-ADM-02 | The system shall allow storing optional patient information: address, phone number, email, insurance number, and insurance provider. |
| FR-ADM-03 | The system shall display a searchable and filterable list of all patients. |
| FR-ADM-04 | The system shall allow viewing a detailed patient profile including all associated appointments. |
| FR-ADM-05 | The system shall support quick-access appointment creation directly from the patient list. |

### 1.2 Appointment Management

| ID | Requirement |
|----|-------------|
| FR-ADM-06 | The system shall allow creating appointments for existing patients with date, time, reason, and optional doctor assignment. |
| FR-ADM-07 | The system shall support three appointment statuses: Scheduled, Completed, and Cancelled. |
| FR-ADM-08 | The system shall display all appointments in a calendar view with day, week, and month perspectives. |
| FR-ADM-09 | The system shall allow filtering appointments by date, calendar week, and month. |
| FR-ADM-10 | The dashboard shall display the next upcoming open appointments. |

### 1.3 Stations & Beds

| ID | Requirement |
|----|-------------|
| FR-ADM-11 | The system shall allow creating hospital stations with name, description, and floor information. |
| FR-ADM-12 | The system shall allow adding beds to stations with bed number, room, and status. |
| FR-ADM-13 | Each bed shall support four statuses: Free, Occupied, Reserved, and Out of Service. |
| FR-ADM-14 | A bed may optionally be assigned to a patient. |
| FR-ADM-15 | The system shall display a visual bed grid per station with colour-coded status indicators. |
| FR-ADM-16 | Each station shall display a real-time occupancy progress bar. |

### 1.4 Dashboard

| ID | Requirement |
|----|-------------|
| FR-ADM-17 | The dashboard shall display aggregate statistics: total patients, today's appointments, open appointments, and free/total bed ratio. |
| FR-ADM-18 | The dashboard shall display a doughnut chart of bed occupancy by status. |
| FR-ADM-19 | The dashboard shall list the next 10 upcoming scheduled appointments. |

---

## 2. Clinical Module

### 2.1 Admissions

| ID | Requirement |
|----|-------------|
| FR-CLN-01 | The system shall allow recording patient admissions with admission date, reason, and optional bed assignment. |
| FR-CLN-02 | The system shall allow recording discharge date and discharge type (home, transfer, deceased, other). |
| FR-CLN-03 | The system shall indicate whether an admission is currently active (no discharge date set). |

### 2.2 Diagnoses

| ID | Requirement |
|----|-------------|
| FR-CLN-04 | The system shall allow recording diagnoses with ICD-10 code, description, type, and status. |
| FR-CLN-05 | Diagnosis types shall include: Primary, Secondary, and Admission diagnosis. |
| FR-CLN-06 | Diagnosis statuses shall include: Active, Resolved, and Chronic. |
| FR-CLN-07 | A diagnosis may be linked to a specific admission. |

### 2.3 Prescriptions / Medications

| ID | Requirement |
|----|-------------|
| FR-CLN-08 | The system shall allow recording prescriptions with drug name, dosage, unit, frequency, and route of administration. |
| FR-CLN-09 | Supported routes shall include: oral, intravenous, intramuscular, topical, inhaled, and other. |
| FR-CLN-10 | Prescriptions shall have a start date and an optional end date. |
| FR-CLN-11 | Prescription statuses shall include: Active, Discontinued, and Completed. |

### 2.4 Lab Results

| ID | Requirement |
|----|-------------|
| FR-CLN-12 | The system shall allow recording lab results with test name, value, unit, and reference range. |
| FR-CLN-13 | Lab result statuses shall include: Normal, Elevated, Low, and Critical. |
| FR-CLN-14 | The system shall store sample date, result date, and ordering doctor. |

### 2.5 Vital Signs

| ID | Requirement |
|----|-------------|
| FR-CLN-15 | The system shall allow recording vital signs including systolic/diastolic blood pressure, heart rate, temperature, oxygen saturation, weight, and height. |
| FR-CLN-16 | The system shall automatically calculate BMI from recorded weight and height. |
| FR-CLN-17 | Each vital signs record shall store a timestamp and the name of the measuring staff member. |

### 2.6 Medical History

| ID | Requirement |
|----|-------------|
| FR-CLN-18 | The system shall allow recording patient allergies with substance, reaction description, and severity (mild, moderate, severe). |
| FR-CLN-19 | The system shall allow recording pre-existing conditions with optional ICD-10 code and onset date. |
| FR-CLN-20 | The system shall allow recording past surgeries with procedure name, OPS code, date, hospital, and surgeon. |

### 2.7 Clinical Notes

| ID | Requirement |
|----|-------------|
| FR-CLN-21 | The system shall allow creating free-text clinical notes linked to a patient. |
| FR-CLN-22 | Note types shall include: Initial Examination, Follow-up, Discharge Note, Consultation, and Other. |
| FR-CLN-23 | Notes shall record the author and creation timestamp. |
| FR-CLN-24 | A note may optionally be linked to an admission or appointment. |

### 2.8 Procedures

| ID | Requirement |
|----|-------------|
| FR-CLN-25 | The system shall allow recording medical procedures with name, OPS code, date, and responsible doctor. |

### 2.9 Referrals / Consultations

| ID | Requirement |
|----|-------------|
| FR-CLN-26 | The system shall allow recording referrals to specialists with referring doctor, specialist, specialty, and reason. |
| FR-CLN-27 | Referral statuses shall include: Pending, Completed, and Cancelled. |
| FR-CLN-28 | The system shall allow storing consultation result notes. |

### 2.10 Discharge Letters

| ID | Requirement |
|----|-------------|
| FR-CLN-29 | The system shall allow creating a discharge letter linked to a specific admission. |
| FR-CLN-30 | A discharge letter shall include: diagnosis summary, treatment summary, discharge medication, and follow-up instructions. |
| FR-CLN-31 | Each discharge letter shall be unique per admission (one-to-one relationship). |

### 2.11 Clinical Summary View

| ID | Requirement |
|----|-------------|
| FR-CLN-32 | The system shall provide a unified clinical summary view per patient showing all clinical data grouped in tabs. |
| FR-CLN-33 | Each tab shall display the count of entries for that category. |
| FR-CLN-34 | The system shall provide a single API endpoint that returns all clinical data for a patient in one request. |
