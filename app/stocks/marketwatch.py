from .helpers import fetch_data
from .models import Competitor, MarketCap, PerformanceData

MARKETWATCH_URL = "https://www.marketwatch.com/investing/stock/{}"

MARKETWATCH_HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'en-US,en;q=0.6',
    'cache-control': 'no-cache',
    'cookie': 'letsGetMikey=enabled; refresh=off; mw_loc=%7B%22Region%22%3A%22SC%22%2C%22Country%22%3A%22BR%22%2C%22Continent%22%3A%22NA%22%2C%22ApplicablePrivacy%22%3A0%7D; gdprApplies=false; ab_uuid=9801a756-390f-48bf-8286-91ecb8197439; fullcss-home=site-6339f8c9e6.min.css; icons-loaded=true; letsGetMikey=enabled; fullcss-section=section-5b7e2ade8e.min.css; fullcss-quote=quote-86ec49efa6.min.css; recentqsmkii=Stock-US-AAPL|Stock-US-KHC; refresh=off; optimizelyEndUserId=oeu1732027112776r0.22299912173075476; pxcts=f29db0b5-a683-11ef-89ca-ba5b15bb8563; _pxvid=f29d9cf4-a683-11ef-89ca-238f0b2c4504; utag_main__sn=1; utag_main__se=1%3Bexp-session; utag_main__ss=1%3Bexp-session; utag_main__st=1732028913209%3Bexp-session; utag_main_ses_id=1732027113209%3Bexp-session; utag_main__pn=1%3Bexp-session; _pcid=%7B%22browserId%22%3A%22m3ok82bjz0ek42a2%22%7D; cX_P=m3ok82bjz0ek42a2; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAEzIE4AmHgZi4CsvAIwB2DqIAMADkHTRvEAF8gA; utag_main__prevpage=MWCC_Customer Resource_Free Registration%3Bexp-1732030714286; utag_main_vapi_domain=marketwatch.com; _px3=69540a41c5348c542e03ec09f05f17d99bd933b81d261f2b42e53f4f10660eae:uybg3HbbUqziXY1FGLCWajQ3XopnOE1LglJ7NDqjjyK2fKpyEJ88ML49TQjxGPE5KVCOXQmYpEopTyjXHqzBvQ==:1000:wNF6zl9vH+pgZy/BxaimL4fV1nn1yCVOTxC7KqbqjJaNObMMdlesKlY6bZsWz3j9bjpOGMzdFAwh6Vnd/1OdJefKzJ9O2xjAofHaEIFORfgUWmvtnk3fs+0sQfWsHEr+rRDctdTX9l3+o6zcyza/VHbXdqCNatPzCPXCHjZZLGwIl57X2Ude25RDpGwpGPjLh7YDpOvbU0tU1PAIxqgl/DJ1ZyWWow5Un9epZMuOQak=; ajs_anonymous_id=7ac3aa93-ef46-4a7d-a9c9-fca62808a1eb; s_ecid=MCMID%7C09811680903199510713670063607068560812; AMCVS_CB68E4BA55144CAA0A4C98A5%40AdobeOrg=1; _meta_cross_domain_id=c63a7feb-5067-44fd-8eea-a1b3a4f0420c; gpv_pn=MWCC_Customer%20Resource_Free%20Registration; s_vnum=1763563116106%26vn%3D1; s_invisit=true; s_vmonthnum=1733022000110%26vn%3D1; s_monthinvisit=true; s_cc=true; AMCV_CB68E4BA55144CAA0A4C98A5%40AdobeOrg=1585540135%7CMCIDTS%7C20047%7CMCMID%7C09811680903199510713670063607068560812%7CMCAID%7CNONE%7CMCOPTOUT-1732034316s%7CNONE%7CvVersion%7C4.4.0',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://www.marketwatch.com/investing/stock/aapl',
    'sec-ch-ua': '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}


async def fetch_marketwatch_webpage(stock_symbol):
    return await fetch_data(MARKETWATCH_URL.format(stock_symbol), MARKETWATCH_HEADERS, "text")


def scrap_competitors_data(html):
    competitors_table = html.find('table', {'aria-label': 'Competitors data table'})
    competitors = []
    if competitors_table:
        rows = competitors_table.find('tbody').find_all('tr')
        for row in rows:
            name_cell = row.find('td', {'class': 'table__cell w50'})
            market_cap_cell = row.find('td', {'class': 'table__cell w25 number'})

            name = name_cell.text.strip()

            market_cap_text = market_cap_cell.text.strip()
            currency = market_cap_text[0]
            value = market_cap_text[1:]

            # Convert to float, handling commas
            value = value.replace(',', '').upper()
            if 'T' in value:
                value = float(value.replace('T', '')) * 1_000_000_000_000
            elif 'B' in value:
                value = float(value.replace('B', '')) * 1_000_000_000

            competitors.append(Competitor(name=name, market_cap=MarketCap(currency=currency, value=value)))

    return competitors


def scrap_performance_data(html):
    performance_table = html.find('div', class_='element element--table performance')
    if not performance_table:
        return None

    performance_map = {
        "5 Day": "five_days",
        "1 Month": "one_month",
        "3 Months": "three_months",
        "YTD": "year_to_date",
        "1 Year": "one_year"
    }

    performance_values = {
        "five_days": 0.0,
        "one_month": 0.0,
        "three_months": 0.0,
        "year_to_date": 0.0,
        "one_year": 0.0
    }

    rows = performance_table.find_all('tr', class_='table__row')
    for row in rows:
        period_column = row.find('td', class_='table__cell')
        if period_column:
            period_name = period_column.text.strip()
            value_column = row.find_all('td', class_='table__cell')[1]
            if value_column:
                performance_value = value_column.text.strip().replace('%', '')
                if period_name in performance_map:
                    field_name = performance_map[period_name]
                    performance_values[field_name] = float(performance_value)

    return PerformanceData(**performance_values)
