CREATE TABLE "SupplementaryData".field_owners (
	id serial4 NOT NULL,
	owner_name varchar NOT NULL,
	"comment" varchar NULL,
	CONSTRAINT "Suppl_field_owner_pkey" PRIMARY KEY (id),
	CONSTRAINT "Suppl_field_owner_un_name" UNIQUE (owner_name)
);