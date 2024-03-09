CREATE TABLE "SupplementaryData".crop_types (
	id serial4 NOT NULL,
	crop_name varchar NOT NULL,
	crop_color varchar NOT NULL,
	"comment" varchar NULL,
	CONSTRAINT "Suppl_crop_type_pkey" PRIMARY KEY (id),
	CONSTRAINT "Suppl_crop_type_un_crop_color" UNIQUE (crop_color),
	CONSTRAINT "Suppl_crop_type_un_name" UNIQUE (crop_name)
);