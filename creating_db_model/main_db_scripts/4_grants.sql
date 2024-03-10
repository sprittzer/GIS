--гранты для групп пользователей
DO $do$
DECLARE
    sch text;
BEGIN
    FOR sch IN SELECT nspname FROM pg_namespace where nspname not in (
                'information_schema',
                'pg_catalog',
                'public',
                'pg_toast')
    LOOP
        EXECUTE format($$ GRANT USAGE ON SCHEMA %I TO users $$, sch); --дать группе users права на usage всх схемы
        EXECUTE format($$ GRANT select on ALL TABLES in SCHEMA %I TO users $$, sch); --дать группе users все select на все таблицы во всех схемах
        
        EXECUTE format($$ GRANT ALL PRIVILEGES ON SCHEMA %I TO admins $$, sch); --дать группе admins все права на все схемы
        EXECUTE format($$ GRANT ALL privileges on ALL TABLES in SCHEMA %I TO admins $$, sch); --дать группе admins все гранты на все таблицы во всех схемах
        EXECUTE format($$ GRANT EXECUTE on ALL FUNCTIONs in SCHEMA %I TO admins $$, sch); --дать группе admins выполнение на все функции во всех схемах
        EXECUTE format($$ GRANT ALL PRIVILEGES on ALL SEQUENCES in SCHEMA %I TO admins $$, sch); --дать группе admins все гранты на все последовательности во всех схемах

    END LOOP;
END;
$do$;