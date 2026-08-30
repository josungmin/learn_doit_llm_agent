from datetime import datetime
import pytz
import yfinance as yf

def get_current_time(timezone: str = 'Asia/Seoul'):
    tz = pytz.timezone(timezone) # 타임존 설정
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    now_timezone = f'{now} {timezone}'
    print(now_timezone)
    return now_timezone

def get_yf_stock_info(ticker: str):
    stock = yf.Ticker(ticker)
    info = stock.info
    print(info)
    return str(info)

def get_yf_stock_history(ticker: str, period: str):
    stock = yf.Ticker(ticker)
    history = stock.history(period=period)
    history_md = history.to_markdown() # 데이터프레임을 마크다운 형식으로 변환
    print(history_md)
    return history_md

def get_yf_stock_recommendations(ticker: str):
    stock = yf.Ticker(ticker)
    recommendations = stock.recommendations
    recommendations_md = recommendations.to_markdown() # 데이터프레임을 마크다운 형식으로 변환
    print(recommendations_md)
    return recommendations_md


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "해당 타임존의 날짜와 시간을 반환합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    'timezone': {
                        'type': 'string',
                        'description': '현재 날짜와 시간을 반환할 타임존을 입력하세요. (예: Asia/Seoul)',
                    },
                },
                "required": ['timezone'],
            },        
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_yf_stock_info",
            "description": "해당 종목의 Yahoo Finance 정보를 반환합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    'ticker': {
                        'type': 'string',
                        'description': 'Yahoo Finance 정보를 반환할 종목의 티커를 입력하세요. (예: AAPL)',
                    },
                },
                "required": ['ticker'],
            },        
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_yf_stock_history",
            "description": "해당 종목의 Yahoo Finance 주가 정보를 반환합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    'ticker': {
                        'type': 'string',
                        'description': 'Yahoo Finance 주가 정보를 반환할 종목의 티커를 입력하세요. (예: AAPL)',
                    },
                    'period': {
                        'type': 'string',
                        'description': '주가 정보를 조회할 기간을 입력하세요. (예: 1d, 5d, 1mo, 1y, 5y)',
                    },
                },
                "required": ['ticker', 'period'],
            },        
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_yf_stock_recommendations",
            "description": "해당 종목의 Yahoo Finance 추천 정보를 반환합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    'ticker': {
                        'type': 'string',
                        'description': 'Yahoo Finance 추천 정보를 반환할 종목의 티커를 입력하세요. (예: AAPL)',
                    },
                },
                "required": ['ticker'],
            },        
        }
    },
]


if __name__ == '__main__':
    # get_current_time('America/New_York')
    # info = get_yf_stock_info('AAPL')  

    get_yf_stock_history('AAPL', '5d')
    print('----')
    get_yf_stock_recommendations('AAPL')
  