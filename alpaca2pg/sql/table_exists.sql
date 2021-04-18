SELECT exists(
    SELECT * FROM information_schema.tables WHERE table_name=%s
)