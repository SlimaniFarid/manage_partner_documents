# -*- coding: utf-8 -*-
{
    'name': "Manage Partners Documents",

    'summary': """ """,

    'description': """
        
    """,

    'author': "Imazighen",
    'website': "",
    'license': 'OPL-1',
    'category': 'Tools',
    'version': '1.0',

    'depends': ['base','mail','web','website','sale','portal'],
    'images': ['static/description/cpu_icon.PNG'],
    # always loaded
    'data': [
        'data/website_data.xml',
        # 'data/product.xml',
        # 'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/res_partner_doc.xml',
        'views/res_partner_doc_requist.xml',
        'views/res_partner.xml',
        'menu/menu.xml',

        #website
        'views/doc_templates_index.xml',
        'views/doc_templates_list.xml',
        'views/doc_templates_one.xml',
        'views/doc_templates_page_registration.xml',
        'views/doc_portal.xml',
      
    ],
    
    'assets': {
         'web.assets_qweb': [
            
        ],

        "web.assets_backend": [

        ],
        'web.assets_frontend': [
              'manage_partner_documents/static/src/js/res_doc_registration.js',
          ]
    },
  
}
