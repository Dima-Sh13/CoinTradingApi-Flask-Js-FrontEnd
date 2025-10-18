CREATE TABLE "movements" (
	"id"	INTEGER NOT NULL,
	"date"	TEXT NOT NULL,
	"time"	TEXT NOT NULL,
	"coin_from"	TEXT NOT NULL,
	"amount_from"	REAL NOT NULL,
	"coin_to"	TEXT NOT NULL,
	"amount_to"	REAL NOT NULL,
	"exchange_rate"	NUMERIC NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);