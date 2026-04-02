/* =========================
   DROP TABLES (if exist)
   ========================= */

DROP TABLE IF EXISTS STUDENT_ASSESSMENT;
DROP TABLE IF EXISTS STUDENT_REGISTRATION;
DROP TABLE IF EXISTS ASSESSMENT;
DROP TABLE IF EXISTS COURSE;
DROP TABLE IF EXISTS STUDENT;


/* =========================
   STUDENT TABLE
   ========================= */

CREATE TABLE STUDENT (
    id_student INT PRIMARY KEY,
    gender VARCHAR(10),
    region VARCHAR(50),
    highest_education VARCHAR(50),
    imd_band VARCHAR(20),
    age_band VARCHAR(20),
    final_result VARCHAR(20)
);


/* =========================
   COURSE TABLE
   ========================= */

CREATE TABLE COURSE (
    code_module VARCHAR(10),
    code_presentation VARCHAR(10),
    module_presentation_length INT,
    PRIMARY KEY (code_module, code_presentation)
);


/* =========================
   ASSESSMENT TABLE
   ========================= */

CREATE TABLE ASSESSMENT (
    id_assessment INT PRIMARY KEY,
    code_module VARCHAR(10),
    code_presentation VARCHAR(10),
    assessment_type VARCHAR(20),
    date DATE,
    weight DECIMAL(5,2),

    FOREIGN KEY (code_module, code_presentation)
        REFERENCES COURSE(code_module, code_presentation)
);


/* =========================
   STUDENT_REGISTRATION TABLE
   ========================= */

CREATE TABLE STUDENT_REGISTRATION (
    id_student INT PRIMARY KEY,
    date_registration DATE,
    date_unregistration DATE,

    FOREIGN KEY (id_student)
        REFERENCES STUDENT(id_student)
);


/* =========================
   STUDENT_ASSESSMENT TABLE
   ========================= */

CREATE TABLE STUDENT_ASSESSMENT (
    id_student INT,
    id_assessment INT,
    date_submitted DATE,
    score DECIMAL(5,2),

    PRIMARY KEY (id_student, id_assessment),

    FOREIGN KEY (id_student)
        REFERENCES STUDENT(id_student),

    FOREIGN KEY (id_assessment)
        REFERENCES ASSESSMENT(id_assessment)
);