CREATE OR REPLACE VIEW msg_pretty AS
SELECT
    payload, from_alias, type_name,
    to_timestamp(message_persisted_ms / 1000.0) AT TIME ZONE 'America/New_York' AS message_persisted,
    CASE
        WHEN message_created_ms IS NOT NULL THEN to_timestamp(message_created_ms / 1000.0) AT TIME ZONE 'America/New_York'
        ELSE NULL
    END AS message_created
FROM messages;
