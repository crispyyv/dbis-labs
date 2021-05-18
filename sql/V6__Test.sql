CREATE TABLE TestPass(
    test_pass_id SERIAL PRIMARY KEY,
    Lang text,
    TestStatus text,
    Ball100 smallint,
    Ball12 smallint,
    Ball smallint,
    DPALevel text,
    AdaptScale smallint default 0,
    school_id integer references school (school_id),
    subject_id integer references subject (subject_id),
    student_id uuid references student (student_id)
)