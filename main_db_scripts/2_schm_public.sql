 -- удаляем у роли public права на схему public
REVOKE ALL ON SCHEMA public FROM public;
--немножко оставляем
GRANT usage ON SCHEMA public to public;
GRANT usage ON SCHEMA pg_catalog to public;
GRANT usage ON SCHEMA information_schema to public;
GRANT EXECUTE ON all FUNCTIONs in schema public TO public;
grant select on all tables in schema "public" to public;