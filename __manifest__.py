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
    'depends': ['base', 'website', 'website_sale'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'jubba_website_extend/static/js/order-info.js',
        ]
    }
}