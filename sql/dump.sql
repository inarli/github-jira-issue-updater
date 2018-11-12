--
-- PostgreSQL database dump
--

CREATE TABLE public.pull_request_reviews (
    id integer NOT NULL,
    issue_id character varying NOT NULL,
    pr_id character varying NOT NULL,
    issue_owner_username character varying NOT NULL,
    reviewer_username character varying NOT NULL,
    created_on timestamp without time zone NOT NULL,
    action character varying NOT NULL
);

CREATE SEQUENCE public.pull_request_reviews_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE ONLY public.pull_request_reviews ALTER COLUMN id SET DEFAULT nextval('public.pull_request_reviews_id_seq'::regclass);

ALTER TABLE ONLY public.pull_request_reviews
    ADD CONSTRAINT pull_request_reviews_pkey PRIMARY KEY (id);