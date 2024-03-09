
do $$
declare
	year int = 2021;	
	size int = 20;		
begin
	execute '
-- for table xxxx_fields
ALTER TABLE "' || year || '"."' || year || '_fields" ADD CONSTRAINT "' || year || '_fields_FK_crop_fact" FOREIGN KEY (id_crop_fact) REFERENCES "SupplementaryData".crop_types(id);
ALTER TABLE "' || year || '"."' || year || '_fields" ADD CONSTRAINT "' || year || '_fields_FK_crop_plan" FOREIGN KEY (id_crop_plan) REFERENCES "SupplementaryData".crop_types(id);
ALTER TABLE "' || year || '"."' || year || '_fields" ADD CONSTRAINT "' || year || '_fields_FK_district" FOREIGN KEY (id_district) REFERENCES "SupplementaryData".municipal_districts(id);
ALTER TABLE "' || year || '"."' || year || '_fields" ADD CONSTRAINT "' || year || '_fields_FK_owner" FOREIGN KEY (id_owner) REFERENCES "SupplementaryData".field_owners(id);
-- for table "xxxx_NDVI_xx_x "
ALTER TABLE "' || year || '"."' || year || '_NDVI_' || size || '" ADD CONSTRAINT "' || year || '_NDVI_' || size || '_FK_id_field" FOREIGN KEY (id_field) REFERENCES "' || year || '"."' || year || '_fields"(id);
ALTER TABLE "' || year || '"."' || year || '_NDVI_' || size || '" ADD CONSTRAINT "' || year || '_NDVI_' || size || '_FK_pixel_result" FOREIGN KEY (id_crop_pixel_result) REFERENCES "SupplementaryData".crop_types(id)';
end;
$$;