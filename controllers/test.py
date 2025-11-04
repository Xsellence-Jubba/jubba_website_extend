# -*- coding: utf-8 -*-
import json
from odoo import http
from odoo.http import request as req
from werkzeug.utils import redirect


def get_partner():
    user = req.env.user
    if user and user.id != 4:
        return user.partner_id
    return None


class Test(http.Controller):
    @http.route('/t777', auth='public', website=True)
    def t777(self, **kw):
        order = req.env['sale.order'].sudo().search([('id', '=', 14)])
        print('order', order.order_line)

        # Del
        delivery = req.env['delivery.carrier'].sudo().search([('id', '=', 1)])

        product_template = None
        if delivery:
            product_template = delivery.product_id

        # Get the first product variant (required for order lines)
        if product_template:
            product = product_template.product_variant_id

            # Add product to the order lines
            req.env['sale.order.line'].sudo().create({
                'order_id': order.id,
                'product_id': product.id,
                'product_uom_qty': 1,
                'price_unit': product.list_price,
                'name': product.name,
            })
        return 't777'

    @http.route('/t8', auth='public', website=True)
    def t8(self, **kw):
        _id = kw.get('id')
        order = req.env['sale.order'].sudo().search([('id', '=', int(_id))])

        if not order:
            return 'order not found'

        print('partner_id', order.partner_id)

        payment_url= req.env['sslcommerz.transaction'].sudo().create_sslcommerz_payment(order, order.partner_id)
        print('payment_url', payment_url)

        # if payment_url:
        #     return redirect(payment_url)

        return 't8'

    @http.route('/t99', type='http', auth='public', csrf=False, save_session=False, website=True)
    def t99(self, **kw):
        # return req.render('jubba_website_extend.confirmation', {
        #     'delivery_methods': 'delivery_methods',
        # })
        tr = req.env['sslcommerz.transaction'].sudo().search([], order='id DESC', limit=1)
        print('tr', tr)

        return 't99'