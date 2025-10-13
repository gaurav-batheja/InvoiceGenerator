from flask import Flask, render_template, request
from datetime import datetime
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    with open('products.json') as f:
        products = json.load(f)

    if request.method == 'POST':
        invoice_number = request.form.get('invoice_number')
        client_name = request.form.get('client_name')
        client_address = request.form.get('client_address')
        payment_mode = request.form.get('payment_mode')
        billing_date = request.form.get('billing_date') or datetime.now().strftime("%d-%m-%Y")

        # Get product list
        product_names = request.form.getlist('product_name')
        qtys = request.form.getlist('qty')
        rates = request.form.getlist('rate')
        mrps = request.form.getlist('mrp')
        hsns = request.form.getlist('hsn')
        gsts = request.form.getlist('gst')

        items = []
        total_before_tax = 0
        total_tax = 0
        inc_amount = 0
        inc_rate=0
        for i in range(len(product_names)):
            qty = float(qtys[i])
            rate = float(rates[i])
            mrp = float(mrps[i])
            gst = float(gsts[i])
            amount = qty * rate
            

            items.append({
                'name': product_names[i],
                'qty': qty,
                'rate': round(rate/(1+((gst)/100)),2),
                'mrp': mrp,
                'hsn': hsns[i],
                'gst': gst,
                'amount': amount
            })
            tax_amount =( round(rate/(1+((gst)/100)),2) * gst / 100)*qty
            inc_amount+=amount
            inc_rate+=round(rate/(1+((gst)/100)),2)*qty

            # total_before_tax =  amount - tax_amount
            total_tax += tax_amount

        total_amount = inc_amount
        total_before_tax = inc_rate
        return render_template('invoice.html',
                               invoice_number=invoice_number,
                               client_name=client_name,
                               client_address=client_address,
                               payment_mode=payment_mode,
                               billing_date=billing_date,
                               items=items,
                               total_before_tax=round(total_before_tax,2),
                               total_tax=round(total_tax,2),
                               total_amount=total_amount)

    return render_template('form.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
