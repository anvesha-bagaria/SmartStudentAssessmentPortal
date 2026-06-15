CREATE TABLE IF NOT EXISTS public.assessments
(
    assessment_id integer NOT NULL,
    title character varying(50) COLLATE pg_catalog."default",
    max_marks integer,
    class character varying(20) COLLATE pg_catalog."default",
    subject character varying(50) COLLATE pg_catalog."default",
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT assessments_pkey PRIMARY KEY (assessment_id)
)

CREATE TABLE IF NOT EXISTS public.options
(
    option_id integer NOT NULL DEFAULT nextval('options_option_id_seq'::regclass),
    question_id integer,
    option_text text COLLATE pg_catalog."default" NOT NULL,
    is_correct boolean NOT NULL,
    CONSTRAINT options_pkey PRIMARY KEY (option_id),
    CONSTRAINT options_question_id_fkey FOREIGN KEY (question_id)
        REFERENCES public.questions (question_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

CREATE TABLE IF NOT EXISTS public.questions
(
    question_id integer NOT NULL DEFAULT nextval('questions_question_id_seq'::regclass),
    assessment_id integer,
    question_number integer,
    question_text text COLLATE pg_catalog."default",
    question_type character varying(20) COLLATE pg_catalog."default",
    difficulty_level character varying(20) COLLATE pg_catalog."default",
    marks integer,
    CONSTRAINT questions_pkey PRIMARY KEY (question_id),
    CONSTRAINT fk_questions_assessment FOREIGN KEY (assessment_id)
        REFERENCES public.assessments (assessment_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

CREATE TABLE IF NOT EXISTS public.results
(
    result_id integer NOT NULL DEFAULT nextval('results_result_id_seq'::regclass),
    submission_id integer,
    total_marks integer,
    overall_feedback text COLLATE pg_catalog."default",
    CONSTRAINT results_pkey PRIMARY KEY (result_id),
    CONSTRAINT results_submission_id_fkey FOREIGN KEY (submission_id)
        REFERENCES public.submissions (submission_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

CREATE TABLE IF NOT EXISTS public.students
(
    student_id integer NOT NULL DEFAULT nextval('students_student_id_seq'::regclass),
    student_class character varying(20) COLLATE pg_catalog."default",
    name character varying(100) COLLATE pg_catalog."default",
    school character varying(100) COLLATE pg_catalog."default",
    email character varying(255) COLLATE pg_catalog."default",
    password character varying(255) COLLATE pg_catalog."default",
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT students_pkey PRIMARY KEY (student_id)
)

CREATE TABLE IF NOT EXISTS public.submissions
(
    submission_id integer NOT NULL DEFAULT nextval('submissions_submission_id_seq'::regclass),
    student_id integer,
    assessment_id integer,
    status character varying(50) COLLATE pg_catalog."default",
    submitted_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT submissions_pkey PRIMARY KEY (submission_id),
    CONSTRAINT submissions_assessment_id_fkey FOREIGN KEY (assessment_id)
        REFERENCES public.assessments (assessment_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT submissions_student_id_fkey FOREIGN KEY (student_id)
        REFERENCES public.students (student_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

CREATE TABLE IF NOT EXISTS public.submitted_answers
(
    answer_id integer NOT NULL DEFAULT nextval('submitted_answers_answer_is_seq'::regclass),
    submission_id integer,
    question_id integer,
    selected_option_id integer,
    answer_text text COLLATE pg_catalog."default",
    marks_awarded integer,
    feedback text COLLATE pg_catalog."default",
    CONSTRAINT submitted_answers_pkey PRIMARY KEY (answer_id),
    CONSTRAINT submitted_answers_question_id_fkey FOREIGN KEY (question_id)
        REFERENCES public.questions (question_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT submitted_answers_selected_option_id_fkey FOREIGN KEY (selected_option_id)
        REFERENCES public.options (option_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT submitted_answers_submission_id_fkey FOREIGN KEY (submission_id)
        REFERENCES public.submissions (submission_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
