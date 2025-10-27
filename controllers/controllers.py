# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request as req


class WebsiteExtend(http.Controller):
    @http.route('/order-info', auth='public', website=True)
    def order_info(self, **kw):
        delivery_methods = req.env['delivery.carrier'].sudo().search([('website_published', '=', True)])
        currency_id = req.env.company.currency_id
        print('delivery_methods', delivery_methods)

        return req.render('jubba_website_extend.shop_customer_info', {
            'delivery_methods': delivery_methods,
            'currency_id': currency_id,
        })
