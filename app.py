from flask import Flask, render_template, request
import pandas as pd 

#initialize the flask app
app = Flask(__name__)

#load csv file
data = pd.read_csv('car_data.csv')

# define the root URL that will renders the home page
@app.route('/')
def index():
    brands = sorted(data['brand'].dropna().unique())
    return render_template('index.html', brands = brands)

#Handles form submission from index.html page
@app.route('/search', methods=['POST'])
def search():
    brand = request.form.get('brand')
    price_input = request.form.get('price')

    filtered = data.copy()

    if brand:
        #filter the row that match the selected brand
        filtered = filtered[filtered['brand'] == brand]

    try:
        price = float(price_input) if price_input else float('inf')
        filtered = filtered[filtered['price'] <= price]

    except ValueError:
        pass
    
    if 'image' not in filtered.columns:
        filtered['image'] = filtered.apply(lambda row: f"{row['brand'].strip().lower().replace(' ', '_')}_{row['model'].strip().lower().split()[0]}.jpg", axis=1)


    return render_template('results.html', cars=filtered.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)