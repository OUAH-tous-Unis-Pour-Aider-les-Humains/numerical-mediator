-- Minimal PostgreSQL schema for the numerical-mediator proof of concept.
-- The schema follows the concepts described in structure_BDD.md.

BEGIN;

CREATE TABLE classification_object (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    wikidata_id TEXT NOT NULL UNIQUE,
    french_name TEXT NOT NULL,
    latex_definition TEXT,
    nature TEXT NOT NULL
);

CREATE TABLE classification_variable (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    classification_object_id BIGINT NOT NULL REFERENCES classification_object(id) ON DELETE CASCADE,
    latex_name TEXT NOT NULL,
    wikidata_id TEXT,
    UNIQUE (classification_object_id, latex_name)
);

CREATE TABLE hypothesis (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    latex_formula TEXT NOT NULL,
    status NUMERIC(5,4) NOT NULL DEFAULT 0,
    CHECK (status >= 0 AND status <= 1)
);

CREATE TABLE hypothesis_variable (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    hypothesis_id BIGINT NOT NULL REFERENCES hypothesis(id) ON DELETE CASCADE,
    classification_object_id BIGINT NOT NULL REFERENCES classification_object(id),
    latex_name TEXT NOT NULL,
    UNIQUE (hypothesis_id, latex_name),
    UNIQUE (hypothesis_id, classification_object_id)
);

CREATE TABLE data_source (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE data_relation (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    data_a_id BIGINT NOT NULL REFERENCES data_source(id) ON DELETE CASCADE,
    data_b_id BIGINT NOT NULL REFERENCES data_source(id) ON DELETE CASCADE,
    UNIQUE (data_a_id, data_b_id),
    CHECK (data_a_id <> data_b_id)
);

CREATE TABLE source (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_date DATE,
    location TEXT,
    author TEXT,
    environment TEXT
);

CREATE TABLE source_data_link (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_id BIGINT NOT NULL REFERENCES source(id) ON DELETE CASCADE,
    data_id BIGINT NOT NULL REFERENCES data_source(id) ON DELETE CASCADE,
    UNIQUE (source_id, data_id)
);

CREATE TABLE hypothesis_for_data (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    hypothesis_id BIGINT NOT NULL REFERENCES hypothesis(id) ON DELETE CASCADE,
    data_id BIGINT NOT NULL REFERENCES data_source(id) ON DELETE CASCADE,
    UNIQUE (hypothesis_id, data_id)
);

CREATE TABLE hypothesis_against_data (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    hypothesis_id BIGINT NOT NULL REFERENCES hypothesis(id) ON DELETE CASCADE,
    data_id BIGINT NOT NULL REFERENCES data_source(id) ON DELETE CASCADE,
    UNIQUE (hypothesis_id, data_id)
);

CREATE TABLE math_predicate (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    latex_formula TEXT NOT NULL,
    title TEXT NOT NULL,
    symbol TEXT,
    is_axiom BOOLEAN NOT NULL DEFAULT FALSE,
    proof_latex TEXT
);

CREATE TABLE math_predicate_reference (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    math_predicate_id BIGINT NOT NULL REFERENCES math_predicate(id) ON DELETE CASCADE,
    referenced_object_id BIGINT NOT NULL REFERENCES classification_object(id),
    reference_name TEXT NOT NULL,
    referenced_predicate_id BIGINT REFERENCES math_predicate(id),
    UNIQUE (math_predicate_id, reference_name)
);

COMMIT;
