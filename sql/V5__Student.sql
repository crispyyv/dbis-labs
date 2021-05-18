

CREATE TABLE Student(
    student_id UUID PRIMARY KEY,
    Birth smallint,
    SexTypeName text,
    ExamYear SMALLINT,
    RegTypeName text,
    ClassProfileName text,
    ClassLangName text,
    region_id integer references region (region_id),
    school_id integer references school (school_id)
);
