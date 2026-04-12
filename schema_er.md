# ER Diagram

```mermaid
erDiagram
    CLASSIFICATION_OBJECT {
        bigint id PK
        text wikidata_id
        text french_name
        text latex_definition
        text nature
    }

    CLASSIFICATION_VARIABLE {
        bigint id PK
        bigint classification_object_id FK
        text latex_name
        text wikidata_id
    }

    HYPOTHESIS {
        bigint id PK
        text latex_formula
        numeric status
    }

    HYPOTHESIS_VARIABLE {
        bigint id PK
        bigint hypothesis_id FK
        bigint classification_object_id FK
        text latex_name
    }

    DATA_SOURCE {
        bigint id PK
        text content
        timestamptz created_at
    }

    DATA_RELATION {
        bigint id PK
        bigint data_a_id FK
        bigint data_b_id FK
    }

    SOURCE {
        bigint id PK
        date source_date
        text location
        text author
        text environment
    }

    SOURCE_DATA_LINK {
        bigint id PK
        bigint source_id FK
        bigint data_id FK
    }

    HYPOTHESIS_FOR_DATA {
        bigint id PK
        bigint hypothesis_id FK
        bigint data_id FK
    }

    HYPOTHESIS_AGAINST_DATA {
        bigint id PK
        bigint hypothesis_id FK
        bigint data_id FK
    }

    MATH_PREDICATE {
        bigint id PK
        text latex_formula
        text title
        text symbol
        boolean is_axiom
        text proof_latex
    }

    MATH_PREDICATE_REFERENCE {
        bigint id PK
        bigint math_predicate_id FK
        bigint referenced_object_id FK
        text reference_name
        bigint referenced_predicate_id FK
    }

    CLASSIFICATION_OBJECT ||--o{ CLASSIFICATION_VARIABLE : has
    CLASSIFICATION_OBJECT ||--o{ HYPOTHESIS_VARIABLE : maps_to
    HYPOTHESIS ||--o{ HYPOTHESIS_VARIABLE : has
    DATA_SOURCE ||--o{ DATA_RELATION : links
    SOURCE ||--o{ SOURCE_DATA_LINK : supports
    DATA_SOURCE ||--o{ SOURCE_DATA_LINK : is_supported_by
    HYPOTHESIS ||--o{ HYPOTHESIS_FOR_DATA : supports
    DATA_SOURCE ||--o{ HYPOTHESIS_FOR_DATA : is_for
    HYPOTHESIS ||--o{ HYPOTHESIS_AGAINST_DATA : opposes
    DATA_SOURCE ||--o{ HYPOTHESIS_AGAINST_DATA : is_against
    MATH_PREDICATE ||--o{ MATH_PREDICATE_REFERENCE : uses
    CLASSIFICATION_OBJECT ||--o{ MATH_PREDICATE_REFERENCE : referenced_object
    MATH_PREDICATE ||--o{ MATH_PREDICATE_REFERENCE : referenced_predicate
```

## Notes

- `DATA_RELATION` stores links between data items.
- `SOURCE_DATA_LINK` links a source to the data it supports.
- `HYPOTHESIS_FOR_DATA` and `HYPOTHESIS_AGAINST_DATA` store the relationship between hypotheses and data.
- `MATH_PREDICATE_REFERENCE` stores references used in proofs and formulas.
