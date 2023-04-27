CREATE TABLE IF NOT EXISTS measurements(
datetime    TEXT PRIMARY KEY NOT NULL,
temperature REAL             NOT NULL,
pressure    REAL             NOT NULL,
humidity    REAL             NOT NULL,
light       REAL             NOT NULL
);