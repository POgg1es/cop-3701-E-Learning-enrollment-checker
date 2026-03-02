<img width="1536" height="1024" alt="database_er md" src="https://github.com/user-attachments/assets/158904ad-89cd-4326-b409-fe1ae6aef3c6" />

# Revised ER Diagram – Final Normalized Relational Schema (BCNF)

This document reflects the final relational schema after BCNF verification.  
All relations satisfy Boyce-Codd Normal Form. No further decomposition was required.

---

## 1. STUDENT

**STUDENT**
- id_student (PK)
- gender
- region
- highest_education
- imd_band (Optional)
- age_band
- final_result

Functional Dependency:
id_student → gender, region, highest_education, imd_band, age_band, final_result

---

## 2. COURSE

**COURSE**
- code_module (PK)
- code_presentation (PK)
- module_presentation_length

Functional Dependency:
(code_module, code_presentation) → module_presentation_length

---

## 3. ASSESSMENT

**ASSESSMENT**
- id_assessment (PK)
- code_module (FK → COURSE)
- code_presentation (FK → COURSE)
- assessment_type
- date (Optional)
- weight

Functional Dependency:
id_assessment → code_module, code_presentation, assessment_type, date, weight

---

## 4. STUDENT_REGISTRATION

**STUDENT_REGISTRATION**
- id_student (PK, FK → STUDENT)
- date_registration
- date_unregistration (Optional)

Functional Dependency:
id_student → date_registration, date_unregistration

---

## 5. STUDENT_ASSESSMENT

**STUDENT_ASSESSMENT**
- id_student (FK → STUDENT)
- id_assessment (FK → ASSESSMENT)
- date_submitted (Optional)
- score (Optional)

Primary Key:
(id_student, id_assessment)

Functional Dependency:
(id_student, id_assessment) → date_submitted, score

---

# Relationship Summary

STUDENT (1) —— (1) STUDENT_REGISTRATION  
STUDENT (1) —— (M) STUDENT_ASSESSMENT  
ASSESSMENT (1) —— (M) STUDENT_ASSESSMENT  
COURSE (1) —— (M) ASSESSMENT  

---

# Normalization Conclusion

All relations are in BCNF because every non-trivial functional dependency
has a determinant that is a superkey.

There are:
- No partial dependencies
- No transitive dependencies
- No redundancy caused by non-key determinants

The schema is fully normalized and free from update, insertion, and deletion anomalies.
