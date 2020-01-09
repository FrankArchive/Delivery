from flask import Blueprint, render_template, request, redirect
import qrcode
import json
import uuid
import utils
import hashlib

shop = Blueprint('shop', __name__)

@shop.route('/buyer')
def buyer():
    return render_template('shop/buyer.html')

@shop.route('/seller')
def seller():
    order_id = str(request.args.get('id'))
    if len(order_id)!=32 or not order_id.isalnum():
        return utils.error_page(["order id incorrect"])
    print('select * from orders where order_id='+order_id)
    cur = utils.db_execute('select * from orders where order_id="'+order_id+'"')
    res = cur.fetchone()
    if not res:
        return utils.error_page(["order id does not exist"])

    info = json.loads(res[1])
    return render_template('shop/seller.html', qr_code=res[2], message=info['message'])

@shop.route('/confirm', methods=['POST'])
def confirm():
    form = request.form
    order_id = hashlib.md5(uuid.uuid4().hex.encode()).hexdigest()
    file = str(uuid.uuid4())+'.png'
    info = {
        'name': form['name'],
        'idnumber': form['idnumber'],
        'address': form['address'],
        'telnumber': form['telnumber'],
        'message': form['message']
    }
    from main import app
    qrcode.make(json.dumps(info)).save(app.static_folder+'/img/qr/'+file)

    conn = utils.db_conn()
    cursor = conn.cursor()
    cursor.execute(
        'insert into orders (order_id,order_info,order_qrcode) values (%s,%s,%s)',
        [order_id, json.dumps(info), file]
    )
    conn.commit()
    conn.close()

    return redirect('/seller?id='+order_id)
    
