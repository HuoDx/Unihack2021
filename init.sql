CREATE TABLE IF NOT EXISTS public.users
(
    uid uuid NOT NULL,
    email character varying(64) COLLATE pg_catalog."default" NOT NULL,
    password character varying(256) COLLATE pg_catalog."default" NOT NULL,
    name character varying(32) COLLATE pg_catalog."default" NOT NULL,
    salt character varying(16) COLLATE pg_catalog."default",
    CONSTRAINT users_pkey PRIMARY KEY (uid)
)


CREATE TABLE IF NOT EXISTS public.spots
(
    _uid uuid NOT NULL,
    _owner uuid NOT NULL,
    lng double precision NOT NULL,
    lat double precision NOT NULL,
    location_description text COLLATE pg_catalog."default",
    capacity integer NOT NULL,
    registered integer NOT NULL,
    title character varying(32) COLLATE pg_catalog."default" NOT NULL,
    logo character varying(64) COLLATE pg_catalog."default",
    description text COLLATE pg_catalog."default",
    contact_number character varying(32) COLLATE pg_catalog."default" NOT NULL,
    created_at bigint NOT NULL,
    CONSTRAINT spots_pkey PRIMARY KEY (_uid),
    CONSTRAINT spots_fkey FOREIGN KEY (_owner)
        REFERENCES public.users (uid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

CREATE TABLE IF NOT EXISTS public.reservations
(
    name character varying(32) COLLATE pg_catalog."default" NOT NULL,
    contact character varying(32) COLLATE pg_catalog."default" NOT NULL,
    spot_uid uuid NOT NULL,
    CONSTRAINT reservations_fkey FOREIGN KEY (spot_uid)
        REFERENCES public.spots (_uid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)