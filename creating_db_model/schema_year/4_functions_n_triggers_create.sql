do $$
declare
   year int = 2021;	--переменная для schema year
   size int = 20;	--переменная размера пикселя NDVI
begin
	execute '
-- создаем функцию записи координаты точки, которая будет выполняться триггером
CREATE FUNCTION "' || year || '".point_coordinate() RETURNS trigger AS $point_coordinate$
    BEGIN
	    -- Записать в текущую строку в столбец "geom" посчитанное значение координаты точки:
		NEW.geom = ST_SetSRID(ST_MakePoint(NEW."X",NEW."Y"), 4326);
   		RETURN NEW;
    END;
$point_coordinate$ LANGUAGE plpgsql;

-- создаем тригер по функции на внесение данных или обновление
CREATE TRIGGER point_coordinate BEFORE INSERT OR UPDATE ON "' || year || '"."' || year || '_NDVI_' || size || '"
    FOR EACH ROW EXECUTE function "' || year || '".point_coordinate();
    
--=======================================================================

-- создаем функцию подсчета площади поля, которая будет выполняться триггером
CREATE FUNCTION "' || year || '".area_insert() RETURNS trigger AS $area_insert$
    BEGIN
		-- Записать в текущую строку в столбец "area" посчитанное значение площади "geom": 
		NEW."area" = ST_Area(new."geom");
    	RETURN NEW;
    END;
$area_insert$ LANGUAGE plpgsql;

-- создаем тригер по функции на внесение данных или обновление
CREATE TRIGGER area_insert BEFORE INSERT OR UPDATE ON "' || year || '"."' || year || '_fields"
    FOR EACH ROW EXECUTE function "' || year || '".area_insert();

--=======================================================================
   
-- создаем функцию которая внесет в таблицу xxxx_NDVI_xx_x значение id_corp_plan из таблицы xxxx_fields , которая будет выполняться триггером
CREATE FUNCTION "' || year || '".id_corp_plan_insert() RETURNS trigger AS $corp_plan_insert$
    BEGIN
		-- Записать в текущую строку в столбец "id_corp_plan" значение из талицы полей: 
		NEW."id_crop_plan" = (select "id_crop_plan" from "' || year || '"."' || year || '_fields" where "id" = NEW."id_field"); 
     	RETURN NEW;
    END;
$corp_plan_insert$ LANGUAGE plpgsql;

-- создаем тригер по функции на внесение данных или обновление
CREATE TRIGGER corp_plan_insert BEFORE INSERT OR UPDATE ON "' || year || '"."' || year || '_NDVI_' || size || '" 
    FOR EACH ROW EXECUTE function "' || year || '".id_corp_plan_insert();';
end;
$$;
   
   