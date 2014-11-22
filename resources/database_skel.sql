PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

DROP TABLE "rack";
DROP TABLE "machine_brand";
DROP TABLE "machine_model";
DROP TABLE "machine";

CREATE TABLE "machine" (
  "id"         INTEGER PRIMARY KEY ASC,
  "name"       TEXT,
  "model"      INTEGER DEFAULT (null),
  "serial"     TEXT DEFAULT (null),
  "unit_value" REAL,
  "invoice"    TEXT,
  "cap_date"   DATETIME,
  "rack"       INTEGER,
  "base"       REAL NOT NULL DEFAULT (0.0),
  "hbase"      REAL DEFAULT (0.0)
);

CREATE TABLE "machine_model" (
  "id" INTEGER PRIMARY KEY ASC,
  "name" TEXT,
  "type_model" TEXT,
  "size" REAL,
  "horizontal_space" REAL,
  "brand" INTEGER
);

CREATE TABLE "machine_brand" (
  "id" INTEGER PRIMARY KEY ,
  "name" TEXT
);

CREATE TABLE "rack" (
  "id" INTEGER PRIMARY KEY ASC,
  "name" TEXT,
  "size" INTEGER,
  "sort" INTEGER DEFAULT (null),
  "del" BOOL NOT NULL  DEFAULT 0
);

DROP VIEW "machine_list";
CREATE VIEW "machine_list" AS SELECT
  machine.id AS id,
  machine.name,
  machine.base,
  machine.hbase,
  machine_model.size AS size,
  machine_model.horizontal_space AS hspace,
  machine_model.id AS model_id,
  machine_model.name AS model_name,
  machine_model.type_model AS type_model,
  machine.serial AS serial,
  rack.id AS rack_id,
  rack.name AS rack_name,
  rack.del AS rack_del
FROM machine, machine_model, rack
WHERE machine.rack = rack.rowid
AND machine.model = machine_model.rowid
ORDER BY machine.name COLLATE NOCASE ASC;

DROP VIEW "rack_list";
CREATE VIEW "rack_list" AS SELECT
  r.*,
  SUM(mmm.used) AS used
FROM (SELECT m.rack, MAX(mm.size) AS used
      FROM machine m, machine_model mm
      WHERE m.model = mm.rowid
      GROUP BY rack, base) AS mmm, rack r
WHERE r.rowid = mmm.rack
AND r.del = 0
GROUP BY r.name
ORDER BY sort, name COLLATE NOCASE ASC;

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
AND rack.del = 0
GROUP BY rack.id 
ORDER BY sort, name COLLATE NOCASE ASC;

INSERT INTO machine_model VALUES(1,'Generic','1U',1.0,1.0,NULL);
INSERT INTO machine_model VALUES(2,'Generic','2U',2.0,1.0,NULL);
INSERT INTO machine_model VALUES(3,'Generic','3U',3.0,1.0,NULL);
INSERT INTO machine_model VALUES(4,'Generic','4U',4.0,1.0,NULL);
INSERT INTO machine_model VALUES(5,'Generic','5U',5.0,1.0,NULL);
INSERT INTO machine_model VALUES(6,'Generic','6U',6.0,1.0,NULL);
INSERT INTO machine_model VALUES(7,'Generic','7U',7.0,1.0,NULL);
INSERT INTO machine_model VALUES(8,'Generic','8U',8.0,1.0,NULL);
INSERT INTO machine_model VALUES(9,'Generic','9U',9.0,1.0,NULL);
INSERT INTO machine_model VALUES(10,'Generic','10U',10.0,1.0,NULL);

COMMIT;
