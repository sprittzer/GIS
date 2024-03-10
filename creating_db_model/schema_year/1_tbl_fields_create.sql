do $$
declare
   year int = 2021;
begin
	execute 'CREATE TABLE "' || year || '"."' || year || '_fields" (
	id serial4 NOT NULL,
	geom public.geometry(multipolygon, 4326) NOT NULL,
	reestr_number varchar NULL,
	"intern_number" varchar NULL,
	id_district int4 NULL,
	id_owner int4 NULL,
	area float8 NULL,
	id_crop_plan int4 NULL,
	id_crop_fact int4 NULL,
	"comment" varchar NULL,
	hash_unique	text,
	CONSTRAINT "' || year || '_fields_pkey" PRIMARY KEY (id),
	CONSTRAINT "' || year || '_fields_un_geom" UNIQUE (hash_unique));
CREATE INDEX "sidx_' || year || '_fields_geom" ON "' || year || '"."' || year || '_fields" USING gist (geom);';
end;
$$;