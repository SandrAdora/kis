# KIS-System 
Ein Kleins KIS-System der als Portfolio-Projekt und als Grundlage für ein echtes Krankenhaus-Informationssystem dienen kann.
Das System besteht aus mehreren Kernmodulen, die gemeinsam eine effiziente Verwaltung 
von Patientendaten, Terminen, klinischen Abläufen und Operationen ermöglichen.

## 1. Dashboard 
Ein zentrales Kontrollzentrum für alle Rollen im System.
Übersicht über Patienten, Termine, Stationen und Operationen
KPI‑Widgets (Belegung, Auslastung, OP‑Status, Tagesübersicht)
Rollenbasierte Zugriffe (Admin, Klinikpersonal, Viewer)

## 2. Kalender
Ein intelligenter, medizinischer Kalender zur Planung und Koordination.
Tages‑, Wochen‑ und Monatsansicht
Ressourcenplanung (Räume, Geräte, Personal)
Konflikterkennung (z. B. Doppelbelegung)
Synchronisation mit Terminverwaltung

## 3. Patientenverwaltung
Zentrale Verwaltung aller Patientendaten.
Patientenakte (Stammdaten, Diagnosen, Allergien, Versicherungsdaten)
Aufenthaltsverwaltung (Station, Zimmer, Bett)
Dokumentenverwaltung (Befunde, Berichte, Laborwerte)
Historie aller Aufenthalte und Behandlungen

## 4. Terminverwaltung
Planung und Koordination medizinischer Termine.
Ambulante und stationäre Termine
Zuweisung von Ärzt:innen, Räumen und Geräten
Automatische Konfliktprüfung
Integration mit Kalender & Patientenverwaltung
Statusverfolgung (geplant, bestätigt, abgeschlossen)

## 5. Klinischeverwaltung 
Abbildung klinischer Prozesse und Stationsabläufe.
Stationsübersicht (Belegung, Pflegebedarf, Prioritäten)
Pflegeplanung & Aufgabenverwaltung
Medikamentenverordnung (Basic‑Modul)
Übergabe‑ und Schichtberichte
Dokumentation klinischer Maßnahmen

## 6. Operationsverwaltung 
OP‑Planung (Saal, Team, Dauer, Priorität)
Prä‑OP‑Checklisten
Material‑ und Geräteplanung
Live‑Status (in Vorbereitung, im OP, Aufwachraum)
Post‑OP‑Dokumentation

# Architektur 
Das KIS-System ist modular aufgebaut und kann flexibel erweitert werden 
**Frontend**: *Framework*: Vanilla Html- Datei (index.html)  
**Backend**: *Framework*: Django mit Flask API
**Deployment**: Docker-basiert 
