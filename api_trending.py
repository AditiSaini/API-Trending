from flask import Flask 
from flask_restful import Api, Resource, reqparse
import pandas as pd

app = Flask(__name__)
api = Api(app)

data = pd.read_csv('trending')

sorted_result = data.sort_values(by = 'shop_id')
sorted_shop_id = sorted_result['shop_id'].tolist()

trendy_shop = {}
temp = []
for idx in range(len(sorted_shop_id)):
    temp = sorted_result[sorted_result['shop_id']== sorted_shop_id[idx]].sort_values(by='trend', ascending=False)['product_id'].tolist()
    trendy_shop[sorted_shop_id[idx]] = temp
    

class Trend(Resource):
    
    def get(self, shop_id):
        if shop_id in sorted_shop_id:
            return {'product_ids': trendy_shop[shop_id]}
        else:
            return {'product_ids': []}

        
class TrendDtl(Resource):
       
    def get(self, shop_id):
        if shop_id in sorted_shop_id:
            temp = sorted_result[sorted_result['shop_id']== shop_id].sort_values(by='trend', ascending=False)[['product_id', 'product_price', 'min_order', 'product_name', 'sum_qt', 'total_customers']]
            return temp.to_json(orient='records')
        else:
            return {"product_id":' ',"product_price":' ' ,"min_order":' ' ,"product_name":' ',"sum_qt":' ',"total_customers":' '}

api.add_resource(Trend, "/shop_id/<int:shop_id>")
api.add_resource(TrendDtl, "/shop_id_dtl/<int:shop_id>")
app.run(debug=True, port=5002)

