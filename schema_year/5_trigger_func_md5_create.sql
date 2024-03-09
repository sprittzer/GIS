do $$
declare
   year int = 2021;	--переменная для schema year
begin
	execute '
-- создаем функцию записи хэш-значения по геометрии поля, которая будет выполняться триггером
CREATE FUNCTION "' || year || '".hash_geom() RETURNS trigger AS $hash_geom$
    BEGIN
		NEW."hash_unique" = md5(ST_AsText(NEW."geom"));
   		RETURN NEW;
    END;
$hash_geom$ LANGUAGE plpgsql;

-- создаем тригер по функции на внесение данных или обновление
CREATE TRIGGER hash_geom BEFORE INSERT OR UPDATE ON "' || year || '"."' || year || '_fields"
    FOR EACH ROW EXECUTE function "' || year || '".hash_geom();';
end;
$$;