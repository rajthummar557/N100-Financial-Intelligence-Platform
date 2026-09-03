-- Query 1: Row counts

SELECT 'companies' AS table_name, COUNT(*) AS row_count
FROM companies

UNION ALL

SELECT 'profitandloss', COUNT(*)
FROM profitandloss

UNION ALL

SELECT 'balancesheet', COUNT(*)
FROM balancesheet

UNION ALL

SELECT 'cashflow', COUNT(*)
FROM cashflow

UNION ALL

SELECT 'analysis', COUNT(*)
FROM analysis

UNION ALL

SELECT 'documents', COUNT(*)
FROM documents

UNION ALL

SELECT 'prosandcons', COUNT(*)
FROM prosandcons

UNION ALL

SELECT 'sectors', COUNT(*)
FROM sectors

UNION ALL

SELECT 'stock_prices', COUNT(*)
FROM stock_prices

UNION ALL

SELECT 'financial_ratios', COUNT(*)
FROM financial_ratios

UNION ALL

SELECT 'market_cap', COUNT(*)
FROM market_cap

UNION ALL

SELECT 'peer_groups', COUNT(*)
FROM peer_groups;


-- Query 2: Missing company IDs

SELECT 'profitandloss' AS table_name, COUNT(*) AS missing_company_id
FROM profitandloss
WHERE company_id IS NULL

UNION ALL

SELECT 'balancesheet', COUNT(*)
FROM balancesheet
WHERE company_id IS NULL

UNION ALL

SELECT 'cashflow', COUNT(*)
FROM cashflow
WHERE company_id IS NULL

UNION ALL

SELECT 'documents', COUNT(*)
FROM documents
WHERE company_id IS NULL

UNION ALL

SELECT 'financial_ratios', COUNT(*)
FROM financial_ratios
WHERE company_id IS NULL

UNION ALL

SELECT 'market_cap', COUNT(*)
FROM market_cap
WHERE company_id IS NULL

UNION ALL

SELECT 'peer_groups', COUNT(*)
FROM peer_groups
WHERE company_id IS NULL

UNION ALL

SELECT 'prosandcons', COUNT(*)
FROM prosandcons
WHERE company_id IS NULL

UNION ALL

SELECT 'sectors', COUNT(*)
FROM sectors
WHERE company_id IS NULL

UNION ALL

SELECT 'stock_prices', COUNT(*)
FROM stock_prices
WHERE company_id IS NULL;

-- Query 3: Year coverage across core financial tables

SELECT
    c.id AS company_id,

    (
        SELECT COUNT(DISTINCT year)
        FROM profitandloss
        WHERE company_id = c.id
          AND year GLOB '????-??'
    ) AS pnl_years,

    (
        SELECT COUNT(DISTINCT year)
        FROM balancesheet
        WHERE company_id = c.id
          AND year GLOB '????-??'
    ) AS bs_years,

    (
        SELECT COUNT(DISTINCT year)
        FROM cashflow
        WHERE company_id = c.id
          AND year GLOB '????-??'
    ) AS cf_years

FROM companies c
ORDER BY c.id;


-- Query 4: Duplicate company-year records

SELECT
    'profitandloss' AS table_name,
    company_id,
    year,
    COUNT(*) AS record_count
FROM profitandloss
GROUP BY company_id, year
HAVING COUNT(*) > 1

UNION ALL

SELECT
    'balancesheet' AS table_name,
    company_id,
    year,
    COUNT(*) AS record_count
FROM balancesheet
GROUP BY company_id, year
HAVING COUNT(*) > 1

UNION ALL

SELECT
    'cashflow' AS table_name,
    company_id,
    year,
    COUNT(*) AS record_count
FROM cashflow
GROUP BY company_id, year
HAVING COUNT(*) > 1

ORDER BY record_count DESC, table_name, company_id, year;



-- Query 5: NULL values in core financial tables

SELECT
    'profitandloss' AS table_name,
    COUNT(*) AS total_rows,
    SUM(CASE WHEN year IS NULL THEN 1 ELSE 0 END) AS null_years,
    SUM(CASE WHEN sales IS NULL THEN 1 ELSE 0 END) AS null_sales,
    SUM(CASE WHEN net_profit IS NULL THEN 1 ELSE 0 END) AS null_net_profit
FROM profitandloss

UNION ALL

SELECT
    'balancesheet',
    COUNT(*),
    SUM(CASE WHEN year IS NULL THEN 1 ELSE 0 END),
    SUM(CASE WHEN total_assets IS NULL THEN 1 ELSE 0 END),
    SUM(CASE WHEN total_liabilities IS NULL THEN 1 ELSE 0 END)
FROM balancesheet

UNION ALL

SELECT
    'cashflow',
    COUNT(*),
    SUM(CASE WHEN year IS NULL THEN 1 ELSE 0 END),
    SUM(CASE WHEN operating_activity IS NULL THEN 1 ELSE 0 END),
    SUM(CASE WHEN net_cash_flow IS NULL THEN 1 ELSE 0 END)
FROM cashflow;

-- QUERY 6 
select c.id as company_id,
c.company_name from companies c
left join cashflow cf on c.id = cf.company_id
where cf.company_id is null order by c.id

-- Query 7: Top 10 companies by ROE

SELECT
    id AS company_id,
    company_name,
    roe_percentage
FROM companies
WHERE roe_percentage IS NOT NULL
ORDER BY roe_percentage DESC
LIMIT 10;


-- Query 8: Companies with no debt

SELECT
    company_id,
    year,
    total_debt_cr
FROM financial_ratios
WHERE total_debt_cr = 0
ORDER BY company_id, year;


-- Query 9: Companies with positive free cash flow

SELECT
    company_id,
    year,
    free_cash_flow_cr
FROM financial_ratios
WHERE free_cash_flow_cr > 0
ORDER BY company_id, year;

--Query 10
select distinct  c.id as company_id,
c.company_name from companies c 
left join documents d on c.id = d.company_id
where d.Annual_Report is null
order by c.id;

select p.company_id,p.year , count(*) as row_count from profitandloss p
inner join balancesheet b on b.company_id = p.company_id
and b.year = p.year
inner join cashflow c on c.company_id = p.company_id
and c.year = p.year 
group by p.company_id,p.year 
having count(*)>1
order by row_count desc;

SELECT company_id, year, COUNT(*) AS row_count
FROM cashflow
GROUP BY company_id, year
HAVING COUNT(*) > 1
ORDER BY row_count DESC;

SELECT *
FROM profitandloss
WHERE company_id = 'PNB'
  AND year = '2024-03';

SELECT *
FROM profitandloss
WHERE company_id = 'ABB'
  AND year = '2024-03';
  SELECT *
FROM cashflow
WHERE company_id = 'PNB'
  AND year = '2024-03';

SELECT
    p.company_id,
    p.year,
    p.sales,
    p.net_profit,
    p.operating_profit,
    p.other_income,
    p.interest,
    p.depreciation,
    p.eps,
    p.dividend_payout,
    b.equity_capital,
    b.reserves,
    b.investments,
    b.borrowings,
    b.total_assets,
    c.operating_activity,
    c.investing_activity,
    c.financing_activity
FROM
(
    SELECT
        company_id,
        year,
        MAX(sales) AS sales,
        MAX(net_profit) AS net_profit
    FROM profitandloss
    GROUP BY company_id, year
) p

INNER JOIN
(
    SELECT
        company_id,
        year,
        MAX(equity_capital) AS equity_capital,
        MAX(reserves) AS reserves,
        MAX(borrowings) AS borrowings,
        MAX(total_assets) AS total_assets
    FROM balancesheet
    GROUP BY company_id, year
) b
    ON b.company_id = p.company_id
   AND b.year = p.year

INNER JOIN
(
    SELECT
        company_id,
        year,
        MAX(operating_activity) AS operating_activity,
        MAX(investing_activity) AS investing_activity,
        MAX(financing_activity) AS financing_activity
    FROM cashflow
    GROUP BY company_id, year
) c
    ON c.company_id = p.company_id
   AND c.year = p.year;