-- 1. Student Profile Page
SELECT 
    id_student,
    gender,
    region,
    highest_education,
    imd_band,
    age_band,
    final_result
FROM STUDENT
WHERE id_student = ?;

-- 2. Assessment Results Page
SELECT 
    a.id_assessment,
    a.assessment_type,
    a.date,
    a.weight,
    sa.id_student,
    sa.score
FROM ASSESSMENT a
JOIN STUDENT_ASSESSMENT sa
    ON a.id_assessment = sa.id_assessment
WHERE a.id_assessment = ?
ORDER BY a.id_assessment, sa.id_student;

-- 4. Student Performance Dashboard
SELECT 
    s.id_student,
    s.final_result,
    AVG(sa.score) AS average_score,
    MAX(sa.score) AS highest_score,
    MIN(sa.score) AS lowest_score
FROM STUDENT s
JOIN STUDENT_ASSESSMENT sa
    ON s.id_student = sa.id_student
GROUP BY s.id_student, s.final_result
ORDER BY s.id_student;

-- 5. Top Students Leaderboard
SELECT 
    s.id_student,
    s.final_result,
    AVG(sa.score) AS average_score
FROM STUDENT s
JOIN STUDENT_ASSESSMENT sa
    ON s.id_student = sa.id_student
GROUP BY s.id_student, s.final_result
ORDER BY average_score DESC;

-- 9. Search Page
SELECT 
    id_student,
    gender,
    region,
    highest_education,
    imd_band,
    age_band,
    final_result
FROM STUDENT
WHERE id_student = ?;