# -*- coding: utf-8 -*-
{
    'name': "Jubba Website Extend",
    'summary': """
        Jubba Website Extend""",

    'description': """
                           Jubba Website Extend
                       """,
    'author': "Abdur Razzak",
    'website': "https://www.xsellencebdltd.com/",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'website', 'website_sale', 'sslcommerz_payment_gateway', 'amarpay_payment_gateway'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/order_information.xml',
        'views/order_confirmation.xml',
    ],
    # 'assets': {
    #     'web.assets_frontend': [
    #         # 'jubba_website_extend/static/js/jquery.min.js',
    #         'jubba_website_extend/static/js/order-information.js',
    #     ]
    # }
}
