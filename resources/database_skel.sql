PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

DROP TABLE "machine";
CREATE TABLE "machine" (
  "id"         INTEGER PRIMARY KEY ASC,
  "name"       TEXT,
  "model"      INTEGER DEFAULT (null),
  "serial"     TEXT DEFAULT (null),
  "unit_value" REAL,
  "invoice"    TEXT,
  "cap_date"   DATETIME,
  "rack"       INTEGER NOT NULL DEFAULT (0),
  "base"       REAL NOT NULL DEFAULT (0.0),
  "hbase"      REAL DEFAULT (0.0),
  "state"      INTEGER NOT NULL DEFAULT 1
);


DROP TABLE "machine_type";
CREATE TABLE "machine_type" (
  "id"         INTEGER PRIMARY KEY ASC,
  "type"       TEXT
);
INSERT INTO table VALUES(1,'Server');
INSERT INTO table VALUES(2,'Storage');
INSERT INTO table VALUES(3,'Power Unit');
INSERT INTO table VALUES(4,'Switch');
INSERT INTO table VALUES(5,'KVM');


DROP TABLE "machine_model";
CREATE TABLE "machine_model" (
  "id"         INTEGER PRIMARY KEY ASC,
  "name"       TEXT,
  "type"       INTEGER DEFAULT (null),
  "type_num"   TEXT DEFAULT (null),
  "model_num"  TEXT DEFAULT (null),
  "size"       REAL,
  "horizontal_space" REAL,
  "brand"      INTEGER
);

INSERT INTO machine_model VALUES(1, 'Generic','','1U','', 1.0, 1.0, NULL);
INSERT INTO machine_model VALUES(2, 'Generic','','2U','', 2.0, 1.0, NULL);
INSERT INTO machine_model VALUES(3, 'Generic','','3U','', 3.0, 1.0, NULL);
INSERT INTO machine_model VALUES(4, 'Generic','','4U','', 4.0, 1.0, NULL);
INSERT INTO machine_model VALUES(5, 'Generic','','5U','', 5.0, 1.0, NULL);
INSERT INTO machine_model VALUES(6, 'Generic','','6U','', 6.0, 1.0, NULL);
INSERT INTO machine_model VALUES(7, 'Generic','','7U','', 7.0, 1.0, NULL);
INSERT INTO machine_model VALUES(8, 'Generic','','8U','', 8.0, 1.0, NULL);
INSERT INTO machine_model VALUES(9, 'Generic','','9U','', 9.0, 1.0, NULL);
INSERT INTO machine_model VALUES(10,'Generic','','10U','',10.0,1.0, NULL);


DROP TABLE "machine_brand";
CREATE TABLE "machine_brand" (
  "id" INTEGER PRIMARY KEY ,
  "name" TEXT
);


DROP TABLE "rack";
CREATE TABLE "rack" (
  "id"       INTEGER PRIMARY KEY ASC,
  "name"     TEXT,
  "size"     INTEGER,
  "sort"     INTEGER DEFAULT (null),
  "state"    INTEGER NOT NULL DEFAULT 1
);

DROP TABLE "state";
CREATE TABLE "state" (
  "id" INTEGER PRIMARY KEY ASC,
  "name" TEXT NOT NULL
);
INSERT INTO state VALUES(1, 'In Use');
INSERT INTO state VALUES(2, 'Disposed');
INSERT INTO state VALUES(3, 'Invalid');


DROP VIEW "machine_list";
CREATE VIEW "machine_list" AS SELECT
  machine.id AS id,
  machine.name,
  machine_model.id AS model_id,
  machine_model.name AS model_name,
  machine_model.type AS type,
  machine_model.type_num AS type_num,
  machine_model.model_num AS model_num,
  machine_model.size AS size,
  machine_model.horizontal_space AS hspace,
  machine.serial AS serial,
  machine.unit_value AS unit_value,
  machine.invoice AS invoice,
  machine.cap_date AS cap_date,
  machine.rack AS rack_id,
  rack.name AS rack_name,
  rack.sort AS rack_sort,
  rack.state AS rack_del,
  machine.base,
  machine.hbase,
  machine.state
FROM machine, machine_model
LEFT OUTER JOIN rack
WHERE (machine.rack IS 0 OR machine.rack = rack.rowid)
AND machine.model = machine_model.rowid
GROUP BY machine.id
ORDER BY machine.name COLLATE NOCASE ASC;


DROP VIEW "rack_list";
CREATE VIEW "rack_list" AS SELECT
  rack.*,
  SUM(mmm.used) AS used
FROM rack
LEFT JOIN (SELECT m.rack, MAX(mm.size) AS used
           FROM machine m, machine_model mm
           WHERE m.model = mm.rowid
           GROUP BY rack, base) AS mmm
ON rack.id = mmm.rack
WHERE (mmm.rack IS NULL OR mmm.rack = rack.id)
AND rack.state == 1
GROUP BY rack.id
ORDER BY sort, name COLLATE NOCASE ASC;

COMMIT;
