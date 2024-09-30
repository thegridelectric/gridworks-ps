CREATE OR REPLACE VIEW msg_pretty AS
SELECT
    payload, from_alias, type_name,
    to_timestamp(message_persisted_ms / 1000.0) AT TIME ZONE 'America/New_York' AS message_persisted,
    CASE
        WHEN message_created_ms IS NOT NULL THEN to_timestamp(message_created_ms / 1000.0) AT TIME ZONE 'America/New_York'
        ELSE NULL
    END AS message_created
FROM messages;


CREATE VIEW pprices AS
SELECT
    market_slot_name,
    value as price,
    to_char(to_timestamp(slot_start_s) AT TIME ZONE 'UTC' AT TIME ZONE 'America/New_York', 'YYYY-MM-DD HH24:MI:SS') AS local_start
FROM
    prices;
