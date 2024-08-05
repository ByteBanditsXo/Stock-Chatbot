from transformers import pipeline
import yfinance as yf

nlp = pipeline('text-generation', model='microsoft/DialoGPT-medium')

def get_response(question):
    
    if "stock price" in question.lower():
        stock_symbol = extract_stock_symbol(question)
        if stock_symbol:
            stock_price = fetch_stock_price(stock_symbol)
            if stock_price:
                return f"The current price of {stock_symbol} is ${stock_price}."
            else:
                return "Sorry, I couldn't fetch the stock price at the moment."
        else:
            return "Please specify a valid stock symbol."
    else:
        
        result = nlp(question)
        return result[0]['generated_text']

def extract_stock_symbol(question):
    
    words = question.split()
    for word in words:
        if word.isupper() and len(word) <= 5:  
            return word
    return None

def fetch_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        stock_info = stock.history(period="1d")
        if not stock_info.empty:
            return round(stock_info['Close'].iloc[-1], 2)
    except Exception as e:
        print(f"Error fetching stock price: {e}")
    return None
