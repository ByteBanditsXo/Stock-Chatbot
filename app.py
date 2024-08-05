from flask import Flask, request, jsonify, render_template
from nlp_model import get_response

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
     data = request.json
     user_message = data.get("message")
     bot_response = get_response(user_message)
     return jsonify({"response": bot_response})
    
def get_stock_price(symbol):
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
    response = requests.get(url)
    data = response.json()
    try:
        stock_price = data['quoteResponse']['result'][0]['regularMarketPrice']
        return f"The current price of {symbol} is ${stock_price}."
    except (IndexError, KeyError):
        return "I couldn't find data for that stock symbol. Please try another."

def get_financial_news():
    url = "https://finance.yahoo.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find_all('h3', class_='Mb(5px)')
    news = []
    for headline in headlines[:5]:  
        news.append(headline.get_text())
    return "Here are the latest financial news headlines:\n" + "\n".join(news)
@app.route('/ask', methods=['POST'])
def ask():
    try:
        
        data = request.get_json()

        if 'question' not in data:
            return jsonify({'error': 'No question field provided'}), 400
        
        question = data['question']
        
        response = get_response(question)
        
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
