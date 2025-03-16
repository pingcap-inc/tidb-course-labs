DROP TABLE IF EXISTS vector_table;
CREATE TABLE vector_table (
    id BIGINT AUTO_RANDOM PRIMARY KEY,
    doc TEXT,
    embedding VECTOR(3)
);
INSERT INTO vector_table (doc, embedding)
SELECT NEXTVAL(vs_seq1),
    VEC_FROM_TEXT(
        CONCAT(
            '[',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ']'
        )
    );
INSERT INTO vector_table (doc, embedding)
SELECT NEXTVAL(vs_seq1),
    VEC_FROM_TEXT(
        CONCAT(
            '[',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ']'
        )
    )
FROM vector_table;
INSERT INTO vector_table (doc, embedding)
SELECT NEXTVAL(vs_seq1),
    VEC_FROM_TEXT(
        CONCAT(
            '[',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ']'
        )
    )
FROM vector_table;
INSERT INTO vector_table (doc, embedding)
SELECT NEXTVAL(vs_seq1),
    VEC_FROM_TEXT(
        CONCAT(
            '[',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ']'
        )
    )
FROM vector_table;
INSERT INTO vector_table (doc, embedding)
SELECT NEXTVAL(vs_seq1),
    VEC_FROM_TEXT(
        CONCAT(
            '[',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ']'
        )
    )
FROM vector_table;
INSERT INTO vector_table (doc, embedding)
SELECT NEXTVAL(vs_seq1),
    VEC_FROM_TEXT(
        CONCAT(
            '[',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ']'
        )
    )
FROM vector_table;
INSERT INTO vector_table (doc, embedding)
SELECT NEXTVAL(vs_seq1),
    VEC_FROM_TEXT(
        CONCAT(
            '[',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ']'
        )
    )
FROM vector_table;
INSERT INTO vector_table (doc, embedding)
SELECT NEXTVAL(vs_seq1),
    VEC_FROM_TEXT(
        CONCAT(
            '[',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ']'
        )
    )
FROM vector_table;
INSERT INTO vector_table (doc, embedding)
SELECT NEXTVAL(vs_seq1),
    VEC_FROM_TEXT(
        CONCAT(
            '[',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ']'
        )
    )
FROM vector_table;
INSERT INTO vector_table (doc, embedding)
SELECT NEXTVAL(vs_seq1),
    VEC_FROM_TEXT(
        CONCAT(
            '[',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ']'
        )
    )
FROM vector_table;
INSERT INTO vector_table (doc, embedding)
SELECT NEXTVAL(vs_seq1),
    VEC_FROM_TEXT(
        CONCAT(
            '[',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ']'
        )
    )
FROM vector_table;
INSERT INTO vector_table (doc, embedding)
SELECT NEXTVAL(vs_seq1),
    VEC_FROM_TEXT(
        CONCAT(
            '[',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ']'
        )
    )
FROM vector_table;
INSERT INTO vector_table (doc, embedding)
SELECT NEXTVAL(vs_seq1),
    VEC_FROM_TEXT(
        CONCAT(
            '[',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ']'
        )
    )
FROM vector_table;
INSERT INTO vector_table (doc, embedding)
SELECT NEXTVAL(vs_seq1),
    VEC_FROM_TEXT(
        CONCAT(
            '[',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ']'
        )
    )
FROM vector_table;
INSERT INTO vector_table (doc, embedding)
SELECT NEXTVAL(vs_seq1),
    VEC_FROM_TEXT(
        CONCAT(
            '[',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ']'
        )
    )
FROM vector_table;
INSERT INTO vector_table (doc, embedding)
SELECT NEXTVAL(vs_seq1),
    VEC_FROM_TEXT(
        CONCAT(
            '[',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ',',
            CONVERT(RAND(), CHAR),
            ']'
        )
    )
FROM vector_table;
ANALYZE TABLE vector_table;