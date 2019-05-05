
import os

from flask import Flask, request, jsonify

import pandas as pd

app = Flask(__name__)


@app.route('/beers', methods = ['get'])
def get_param():
    
    beer_type = request.args.get('beer_type')
    
    beer_type = str(beer_type)
    
    beer_type = beer_type.replace("_", " ")
    
    beer_type = beer_type.title()
    
    beers = pd.read_csv('beer_joined_v0.1.csv')
    
    beers_filt = beers.query("style_name == @beer_type")
    
    reccomendations = pd.Series(beers_filt.iloc[:, 0].sample(5)).to_json()
    
    keywords = beers_filt.iloc[0, 3:22].sample(5).to_json()
    
    abv = pd.Series(beers_filt['abv'].mean()).to_json()
     
    beers_json = jsonify(reccomendations, keywords, abv)
    
    return beers_json
    
if __name__ == '__main__':
    if 'PORT' in os.environ:
        app.run(host='0.0.0.0', port=int(os.environ['PORT']))
    else:
        app.run(debug=True)