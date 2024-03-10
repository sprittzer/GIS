CREATE TABLE "SupplementaryData".crop_varieties (
	id serial4 NOT NULL,
	crop_sort_name varchar NOT NULL,
	id_crop int4 not NULL,
	"comment" varchar NULL,
	CONSTRAINT "Suppl_crop_varietie_pkey" PRIMARY KEY (id),
	CONSTRAINT "Suppl_crop_varietie_un" UNIQUE (crop_sort_name, id_crop)
);