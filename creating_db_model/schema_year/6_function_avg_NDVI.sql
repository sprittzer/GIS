CREATE OR REPLACE FUNCTION "2021".avg_ndvi_21_20(
  name_crop text,
  id_field text,
  extra_arg text DEFAULT ''
)
RETURNS TABLE (week text, average_ndvi double precision) AS $$DECLARE
  query_template text;
  column_name1 text;
  query_condition text;
  id_crop_plan int;
  cl double precision;
begin
  if name_crop != '' then
	select id from "SupplementaryData"."crop_types" where "SupplementaryData"."crop_types".crop_name=name_crop INTO id_crop_plan;
  else 
  	id_crop_plan := -1;
  end if;
  if (id_field != '') and (id_crop_plan != -1) then
  	query_condition := '"2021"."2021_fields".id=' || id_field || ' and "2021"."2021_fields".id_crop_fact=' || id_crop_plan;
  end if;
  if (id_field != '') and (id_crop_plan = -1) then
  	query_condition := '"2021"."2021_fields".id=' || id_field;
  end if;
  if (id_field = '') and (id_crop_plan != -1) then
  	query_condition := '"2021"."2021_fields".id_crop_fact=' || id_crop_plan;
  end if;
  if extra_arg != '' then
    query_condition := extra_arg;
  end if;
  query_template := 'SELECT AVG("column_name") FROM "2021"."2021_NDVI_20" JOIN "2021"."2021_fields" ON "2021"."2021_NDVI_20".id_field = "2021"."2021_fields".id WHERE ' || query_condition;
  FOR column_name1 IN (
    SELECT column_name FROM information_schema.columns WHERE table_name = '2021_NDVI_20' AND column_name ~ 'NDV\d+'
  ) LOOP
    EXECUTE REPLACE(query_template, 'column_name', column_name1) INTO cl;
   	if cl != 0 THEN
  	  RAISE NOTICE 'Result: %', cl;
      RETURN QUERY SELECT regexp_replace(column_name1, '[^0-9]', '', 'g'), cl;
    end if;
  END LOOP;

  return;
END;
$$ LANGUAGE plpgsql;