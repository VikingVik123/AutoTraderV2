from autotrader.data.get_history import Get_history
from autotrader.dataframes.data import Price2DataFrame
from autotrader.strategies.default import DefaultStrategy
from autotrader.indicators.technical import Technical_Indicators

def main():
    # Get historical data
    price2df = Price2DataFrame()
    df = price2df.to_dataframe()
    #print(df)

    # Apply technical indicators FIRST
    indicators = Technical_Indicators()
    df = indicators.get_indicators()  # This ensures 'ema50' and others exist
    #print(df.head())  # Check if ema50 is present

    # Run default strategy
    strategy = DefaultStrategy()
    strategy.data = df  # Assign DataFrame with indicators
    strategy.long_signal()
    strategy.short_signal()
    print(strategy.data)

if __name__ == "__main__":
    main()
