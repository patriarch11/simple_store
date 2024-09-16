--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3
-- Dumped by pg_dump version 16.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: orderstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.orderstatus AS ENUM (
    'RESERVED',
    'COMPLETED',
    'CANCELLED'
);


ALTER TYPE public.orderstatus OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);


ALTER TABLE public.categories OWNER TO postgres;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categories_id_seq OWNER TO postgres;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    user_id integer NOT NULL,
    product_id integer NOT NULL,
    status public.orderstatus NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    quantity integer NOT NULL,
    amount double precision NOT NULL,
    product_price double precision NOT NULL,
    product_discount_pct double precision NOT NULL
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.orders_id_seq OWNER TO postgres;

--
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    id integer NOT NULL,
    category_id integer NOT NULL,
    subcategory_id integer NOT NULL,
    name character varying(255) NOT NULL,
    discount_pct double precision NOT NULL,
    price double precision NOT NULL,
    total_count integer NOT NULL,
    reserved_count integer NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);


ALTER TABLE public.products OWNER TO postgres;

--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.products_id_seq OWNER TO postgres;

--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: subcategories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subcategories (
    id integer NOT NULL,
    category_id integer NOT NULL,
    name character varying(255) NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);


ALTER TABLE public.subcategories OWNER TO postgres;

--
-- Name: subcategories_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subcategories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.subcategories_id_seq OWNER TO postgres;

--
-- Name: subcategories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.subcategories_id_seq OWNED BY public.subcategories.id;


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Name: subcategories id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subcategories ALTER COLUMN id SET DEFAULT nextval('public.subcategories_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
0001
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categories (id, name, created_at, updated_at) FROM stdin;
1	electronics	2024-08-30 23:46:58.949524+03	\N
2	clothes	2024-08-30 23:52:20.04068+03	\N
3	test	2024-09-16 10:09:51.133579+03	\N
4	test cat	2024-09-16 15:56:28.005879+03	\N
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (id, user_id, product_id, status, created_at, updated_at, quantity, amount, product_price, product_discount_pct) FROM stdin;
46	0	1	RESERVED	2024-09-16 13:06:49.124415+03	2024-09-16 13:15:58.121703+03	5	49.5	10	1
47	1	1	RESERVED	2024-09-16 13:08:42.227199+03	2024-09-16 13:15:58.121703+03	5	49.5	10	1
50	0	1	RESERVED	2024-09-16 18:54:55.444841+03	\N	15	148.5	10	1
51	3	6	RESERVED	2024-09-16 18:55:08.584498+03	\N	44	6600	150	0
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.products (id, category_id, subcategory_id, name, discount_pct, price, total_count, reserved_count, created_at, updated_at) FROM stdin;
14	1	1	grandmother's phone	10	100	95	0	2024-08-30 23:51:58.084966+03	2024-09-14 17:04:31.799359+03
15	2	4	white shirt	0	3252	100	0	2024-08-30 23:53:43.402405+03	2024-08-31 18:42:56.479956+03
3	1	3	raspberry pi 4	0	200	100	0	2024-08-30 23:49:09.932104+03	2024-08-31 18:41:49.926366+03
18	2	4	blue shirt	0	325	93	0	2024-08-30 23:54:01.633732+03	2024-08-31 22:08:25.776102+03
8	1	2	laptop 3	0	2352	100	0	2024-08-30 23:51:08.684058+03	2024-08-31 18:42:21.722369+03
5	1	3	banana pi	0	300	100	0	2024-08-30 23:49:34.078379+03	2024-08-31 18:41:59.461248+03
17	2	4	green shirt	0	235	100	0	2024-08-30 23:53:56.136687+03	2024-08-31 18:43:03.600421+03
10	1	2	laptop 5	0	523	100	0	2024-08-30 23:51:19.433281+03	2024-08-31 18:42:31.954064+03
2	1	3	raspberry pi 3	0	15	100	0	2024-08-30 23:49:05.600496+03	2024-08-31 18:41:44.50771+03
7	1	2	laptop 2	0	241	100	0	2024-08-30 23:51:02.469813+03	2024-08-31 18:42:14.805714+03
16	2	4	red shirt	0	235	100	0	2024-08-30 23:53:50.677785+03	2024-08-31 18:42:59.696794+03
13	1	1	mobile phone	0	235	100	0	2024-08-30 23:51:41.047829+03	2024-08-31 18:42:42.942005+03
9	1	2	laptop 4	0	235	98	0	2024-08-30 23:51:14.429154+03	2024-08-31 22:09:57.347966+03
4	1	3	raspberry pi 5	0	2000	100	0	2024-08-30 23:49:16.143224+03	2024-08-31 18:41:54.834983+03
12	1	1	cell phone	0	235	100	0	2024-08-30 23:51:33.961949+03	2024-08-31 18:42:39.345565+03
11	1	1	phone	0	235	99	0	2024-08-30 23:51:26.57478+03	2024-08-31 22:10:02.557206+03
1	1	3	arduino	1	10	100	25	2024-08-30 23:48:38.429025+03	2024-09-16 18:54:55.442278+03
6	1	2	chinese laptop	0	150	100	44	2024-08-30 23:50:26.532282+03	2024-09-16 18:55:08.583097+03
\.


--
-- Data for Name: subcategories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.subcategories (id, category_id, name, created_at, updated_at) FROM stdin;
1	1	phones	2024-08-30 23:47:25.06993+03	\N
2	1	laptops	2024-08-30 23:47:43.275518+03	\N
3	1	mini-computers	2024-08-30 23:48:03.944936+03	\N
4	2	shirts	2024-08-30 23:52:46.54733+03	\N
5	2	pants	2024-08-30 23:52:58.177444+03	\N
6	3	test	2024-09-16 10:10:17.084752+03	\N
7	4	test subcat	2024-09-16 15:56:47.590116+03	\N
\.


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categories_id_seq', 4, true);


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_id_seq', 51, true);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.products_id_seq', 23, true);


--
-- Name: subcategories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subcategories_id_seq', 7, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: categories categories_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_name_key UNIQUE (name);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: subcategories subcategories_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subcategories
    ADD CONSTRAINT subcategories_name_key UNIQUE (name);


--
-- Name: subcategories subcategories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subcategories
    ADD CONSTRAINT subcategories_pkey PRIMARY KEY (id);


--
-- Name: subcategories_category_id_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX subcategories_category_id_idx ON public.subcategories USING btree (category_id);


--
-- Name: orders orders_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: products products_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- Name: products products_subcategory_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_subcategory_id_fkey FOREIGN KEY (subcategory_id) REFERENCES public.subcategories(id);


--
-- Name: subcategories subcategories_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subcategories
    ADD CONSTRAINT subcategories_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- PostgreSQL database dump complete
--

