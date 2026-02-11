Anonymous Teaching-Learning Feedback System — Summary

This project is a Django-based real-time classroom feedback system designed to collect fully anonymous 
student feedback on teaching–learning sessions in a controlled and authentic manner.

The system involves two participants:

Teacher – creates and manages feedback sessions

Student – participates anonymously through QR-based access

The goal is to ensure genuine presence-based feedback, preventing fake or duplicate submissions.

Working Flow

Teacher creates a feedback session and prepares questions
(MCQ, radio, checkbox, rating, yes/no, descriptive)

System generates a QR code + shareable link

Student scans QR and clicks “I am Present”
→ teacher sees live headcount

Teacher verifies class attendance and clicks Start Feedback

Students submit feedback anonymously (one submission per device)

System locks submission after completion

Teacher views human-readable analytical report

🧠 Key Features Implemented
Authentication & Control

Teacher-controlled session opening/closing

Anonymous participation — no student identity stored

One submission per device (duplicate prevention)

Presence validation before feedback

Live Classroom Monitoring

Real-time attendance count (AJAX refresh)

Live feedback status (Open / Closed)

QR-based instant access

Smart Question Builder

Teachers can design feedback forms dynamically:

Radio buttons

Checkboxes

Yes / No

Star rating (1–5)

Short answer

Long answer

Questions are reorderable and editable.

Data Handling Model

Each response records:

Session → Response → Question → Selected Option


Option IDs are stored internally but converted to readable text in reports.

Analytics & Report

The report generates human-friendly insights:

Average rating

Option-wise percentage bars

Student comments

Total responses

Teacher name

Department

Session date & time

Example output:

Teacher: Dr. S. Chakraborty
Department: Computer Science
Responses: 48 Students
Average Rating: ⭐ 4.3 / 5

🔐 Why It Is Reliable

Unlike normal Google-form feedback, this system ensures:

Only physically present students can vote

Teacher verifies attendance before feedback

Anonymous yet authentic responses

No manipulation or bulk submission possible

🎯 Purpose

Designed for academic institutions to support:

Internal Quality Assurance (IQAC)

NAAC/NBA documentation

Course feedback monitoring

Teaching improvement analytics


