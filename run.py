from flask import Flask

pre_path = '/pyapi'

app = Flask(__name__)


@app.route(pre_path + '/')
def hi():
    return 'hi flask'


import route.common_route as common_route
import route.admin_route as admin_route
import route.customer_route as customer_route
import route.account_route as account_route
import route.product_route as product_route
import route.product_plan_route as product_plan_route
import route.asset_route as asset_route

app.register_blueprint(common_route.bp)
app.register_blueprint(admin_route.bp)
app.register_blueprint(customer_route.bp)
app.register_blueprint(account_route.bp)
app.register_blueprint(product_route.bp)
app.register_blueprint(product_plan_route.bp)
app.register_blueprint(asset_route.bp)

if __name__ == '__main__':
    app.run(port=5003, debug=True)
