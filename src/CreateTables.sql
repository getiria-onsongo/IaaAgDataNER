-- USEFUL TIPS
-- Postgresql has three character types:
-- varchar(n) = variable length with limit
-- char(n) = fixed-length, blank padded
-- text = variable unlimited length

-- If you desire to store long strings with no specific upper limit, use text or character varying without a
-- length specifier, rather than making up an arbitrary length limit. There is no performance difference among
-- these three types, apart from increased storage space when using the blank-padded type, and a few extra
-- CPU cycles to check the length when storing into a length-constrained column. While character(n) has performance
-- advantages in some other database systems, there is no such advantage in PostgreSQL; in fact character(n) is
-- usually the slowest of the three because of its additional storage costs. In most situations text or
-- character varying should be used instead.

DROP TABLE IF EXISTS raw_data;
CREATE TABLE raw_data(
    date_time text,
    file_name text,
    variety_name text,
    category text,
    value text
);

DROP TABLE IF EXISTS document CASCADE;
CREATE TABLE document(
    doc_name text PRIMARY KEY,
    url text
);

DROP TABLE IF EXISTS crop CASCADE; 
CREATE TABLE crop(
    crop_name text PRIMARY KEY
);

DROP TABLE IF EXISTS crop_variety CASCADE;
CREATE TABLE crop_variety(
    cvar text PRIMARY KEY,
    crop_name text REFERENCES crop(crop_name)
);

-- id: integer in postgreSQL ranges from -2147483648 to +2147483647. Some of the values generated in the
-- tests for id e.g., -2576147415226899614 were outside integer range so we will use bigint
-- chunk: stores page numbers. I do not think there is a universe where you will have a PDF with more than
-- 32767 pages with is the range for small int.

DROP TABLE IF EXISTS cvar_data_source CASCADE;
CREATE TABLE cvar_data_source(
    id bigint PRIMARY KEY,
    chunk smallint,
    doc_name text REFERENCES document (doc_name),
    cvar text REFERENCES crop_variety (cvar)
);

DROP TABLE IF EXISTS ner_tag CASCADE;
CREATE TABLE ner_tag(
    id bigint REFERENCES cvar_data_source (id),
    label text,
    PRIMARY KEY (id, label)
);

DROP TABLE IF EXISTS crop_attribute;
CREATE TABLE crop_attribute(
    value text,
    id bigint,
    label text,
     FOREIGN KEY (id, label) REFERENCES ner_tag (id, label),
    PRIMARY KEY (value, id, label)
);


