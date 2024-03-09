ALTER TABLE "SupplementaryData".crop_varieties ADD CONSTRAINT crop_types_fk FOREIGN KEY (id_crop) REFERENCES "SupplementaryData".crop_types(id);

