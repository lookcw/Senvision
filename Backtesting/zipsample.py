import zipline

def preview(df):
    log.info(df.head())
    return df

def initialize(context):
    context.investment_size = (context.portfolio.cash / 10.0)
    context.stop_loss_pct = 0.995
    set_symbol_lookup_date('2012-10-01')
    fetch_csv('http://sentdex.com/api/finance/sentiment-signals/sample/', pre_func = preview)
    context.stocks = symbols('AAPL', 'MCD', 'FB', 'GME', 'INTC', 'SBUX', 'T', 'MGM', 'SHLD', 'NKE', 'NFLX', 'PFE', 'GS', 'TGT', 'NOK', 'SNE', 'TXN', 'JNJ', 'KO', 'VZ', 'XOM', 'WMT', 'MCO', 'TWTR', 'URBN', 'MCP', 'MSFT', 'HD', 'KSS', 'AMZN', 'S', 'BA', 'F', 'JPM', 'QCOM', 'TSLA', 'YHOO', 'BBRY', 'GM', 'IBM', 'C', 'ZNGA', 'BAC', 'DIS', 'SCHW', 'UA', 'CSCO', 'ORCL', 'SYMC', 'WFC', 'TM', 'EBAY', 'SCHL', 'MS', 'NDAQ', 'TIF', 'AIG', 'DAL', 'JCP', 'MRK', 'CA', 'SIRI', 'AMD', 'CVX', 'FSLR', 'LMT', 'P', 'CBS', 'TWX', 'PEP', 'LNKD', 'CMG', 'NVDA', 'BBY', 'TWC', 'M', 'RHT', 'ACN', 'CRM', 'PETS', 'CELG', 'BLK', 'GD', 'DOW', 'YUM', 'GE', 'MA', 'DTV', 'DDD', 'CAT', 'FDX', 'GRPN', 'ACE', 'BK', 'GILD', 'V', 'DUK', 'FFIV', 'WFM', 'CVS', 'UNH', 'LUV', 'CBG', 'AFL', 'CHK', 'BRCM', 'HPQ', 'LULU', 'ATVI', 'RTN', 'EMC', 'NOC', 'MAR', 'X', 'BMY', 'LOW', 'COST', 'HON', 'SPLS', 'BKS', 'AA', 'AXP', 'AMGN', 'GPS', 'MDT', 'LLY', 'CME', 'MON', 'WWWW', 'MU', 'DG', 'TRIP', 'HAL', 'COH', 'WYNN', 'PCLN', 'HTZ', 'CLF', 'DD', 'ACI', 'FCX', 'AON', 'GMCR', 'CSX', 'ADBE', 'PRU', 'PG', 'MYL', 'STT', 'PPG', 'EXPE', 'KORS', 'JNPR', 'UTX', 'HOT', 'SNDK', 'CCL', 'DRI', 'BIIB', 'MHFI', 'BBT', 'APA', 'A', 'TDC', 'ANF', 'MTB', 'PPL', 'ABT', 'GNW', 'KMI', 'MET', 'FE', 'DVA', 'ETFC', 'GLW', 'NRG', 'INTU', 'KR', 'ARNA', 'VALE', 'MSI', 'EOG', 'AET', 'MAT', 'HST', 'COP', 'MO', 'IVZ', 'HUM', 'NUE', 'CI')

# Will be called on every trade event for the securities you specify. 
def handle_data(context, data):
    
    
    cash = context.portfolio.cash
    try:
        for s in data:
            
            if 'sentiment_signal' in data[s]:
                sentiment = data[s]['sentiment_signal']
                current_position = context.portfolio.positions[s].amount
                current_price = data[s].price
                
                if (sentiment > 5) and (current_position == 0):
                    if cash > context.investment_size:
                        order_value(s, context.investment_size, style=StopOrder(current_price * context.stop_loss_pct))
                        cash -= context.investment_size
                        
                        
                elif (sentiment <= -1) and (current_position > 0):
                    order_target(s,0)

    except Exception as e:
        print(str(e))
