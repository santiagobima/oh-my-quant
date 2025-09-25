WITH calendar AS (
    SELECT generate_series(
        (SELECT MIN(trade_date) FROM prices_eod p 
         JOIN instruments i ON p.instrument_id = i.id 
         WHERE i.symbol = 'AAPL'),
        (SELECT MAX(trade_date) FROM prices_eod p 
         JOIN instruments i ON p.instrument_id = i.id 
         WHERE i.symbol = 'AAPL'),
        interval '1 day'
    )::date AS dt
),
trading_days AS (
    SELECT dt
    FROM calendar
    WHERE EXTRACT(ISODOW FROM dt) < 6   -- excluye sábados (6) y domingos (7)
)
SELECT t.dt AS missing_date
FROM trading_days t
LEFT JOIN (
    SELECT DISTINCT trade_date
    FROM prices_eod p
    JOIN instruments i ON p.instrument_id = i.id
    WHERE i.symbol = 'AAPL'
) p
  ON t.dt = p.trade_date
WHERE p.trade_date IS NULL
ORDER BY t.dt;