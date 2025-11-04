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


class WebsiteExtend(http.Controller):
    @http.route('/order/information', auth='public', website=True)
    def order_info(self, **kw):
        pt = get_partner()
        delivery_methods = req.env['delivery.carrier'].sudo().search([('website_published', '=', True)])
        currency_id = req.env.company.currency_id
        sale_order_id = req.session.get('sale_order_id')

        if not sale_order_id:
            return req.redirect('/shop')

        data = {
            'amount_untaxed': 0,
            'product_total': 0
        }

        if sale_order_id:
            order = req.env['sale.order'].sudo().search([('id', '=', sale_order_id)])
            data['amount_untaxed'] = order.amount_untaxed

            for l in order.order_line:
                product_template_id = l.product_template_id
                if product_template_id.type == 'consu':
                    data['product_total'] += l.price_subtotal

        print('data', data)

        json_data = json.dumps(data)
        payment_methods = req.env['payment.method'].sudo().search([])

        return req.render('jubba_website_extend.shop_customer_info', {
            'delivery_methods': delivery_methods,
            'currency_id': currency_id,
            'json_data': json_data,
            'pt': pt,
            'payment_methods': payment_methods,
            'data': data,
        })

    @http.route('/order/information/process', auth='public', website=True)
    def order_info_process(self, **kw):
        pt = get_partner()
        website = req.website
        payment_method = kw.get('payment_method')

        # req.session['alert_danger'] = 'Mobile number not valid'
        # return req.redirect('/order/information')

        if not payment_method:
            return 'payment_method not specified'

        # Create contact
        contact_values = {
            'name': kw.get('name'),
            'mobile': kw.get('mobile'),
            'street': kw.get('street'),
        }
        new_contact = req.env['res.partner'].sudo().create(contact_values)

        # Order
        sale_order_id = req.session.get('sale_order_id')
        order = None
        if sale_order_id:
            order = req.env['sale.order'].sudo().search([('id', '=', sale_order_id)])

        if pt:
            order.partner_id = pt.id
        elif order and new_contact:
            order.partner_id = new_contact.id

        if website:
            order.website_id = website.id

        # delivery_method
        delivery_method = kw.get('delivery_method')
        delivery = None

        if delivery_method:
            delivery = req.env['delivery.carrier'].sudo().search([('id', '=', int(delivery_method))])

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

            req.session.pop('website_sale_pricelist_time', None)
            req.session.pop('website_sale_shop_layout_mode', None)
            req.session.pop('website_sale_current_pl', None)
            req.session.pop('website_sale_cart_quantity', None)
            req.session.pop('sale_order_id', None)
            print('Session cleared')

        if order and delivery and product_template:
            order.action_confirm()
            req.session['last_order_id'] = order.id

            if payment_method == 'COD':
                return req.redirect(f'/order/confirmation')
            elif payment_method == 'SSLCOMMERZ':
                payment_url = req.env['sslcommerz.transaction'].sudo().create_sslcommerz_payment(order,
                                                                                                 order.partner_id)
                # print('payment_url', payment_url)
                if payment_url:
                    return redirect(payment_url)
                else:
                    return req.redirect('/')

            # Amarpay
            elif payment_method == 'AMARPAY':
                return req.redirect(f'/pay/amarpay?order_id={order.id}')

            return req.redirect(f'/')
        else:
            return req.redirect(f'/')

    @http.route('/order/confirmation/preprocess', type='http', auth='public', csrf=False, save_session=False, website=True)
    def order_confirmation_preprocess(self, **kw):
        return req.redirect(f'/order/confirmation')

    @http.route('/order/confirmation', type='http', auth='public', website=True)
    def order_confirmation(self, **kw):
        pt = get_partner()
        last_order_id = req.session.get('last_order_id')
        order = None
        if last_order_id:
            order = req.env['sale.order'].sudo().search([('id', '=', last_order_id)])

        if not order or not last_order_id:
            return req.redirect('/')

        related_invoices = req.env['account.move'].sudo().search([
            ('move_type', '=', 'out_invoice'),  # Filter for Customer Invoices
            ('invoice_origin', '=', order.name)  # Link by SO reference (e.g., 'S0001')
        ])

        print('related_invoices', related_invoices)
        for invoice in related_invoices:
            print('payment_state', invoice.payment_state)

        req.session.pop('last_order_id', None)
        print('order', order)

        return req.render('jubba_website_extend.order_confirmation', {
            'order': order,
            'pt': pt,
            'related_invoices': related_invoices,
        })
