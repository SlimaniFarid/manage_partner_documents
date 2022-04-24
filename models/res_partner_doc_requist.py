# -*- coding: utf-8 -*-


from datetime import datetime
import random
import json
from sre_parse import State

from odoo import api, models, fields,tools, _
from odoo.addons.http_routing.models.ir_http import slug, unslug
from odoo.tools.translate import html_translate
from odoo.tools import html2plaintext

import logging
_logger = logging.getLogger(__name__)

class ResPartnerDocrequest(models.Model):
    _name = 'res.partner.doc.request'
    _description = 'Server Monitoring'
    _rec_name="partner_id"
    _inherit = [
        'mail.thread',
        'website.seo.metadata',
        'website.multi.mixin',
        'website.cover_properties.mixin',
        'website.searchable.mixin',
        'mail.activity.mixin'
    ]
   


    partner_id     = fields.Many2one('res.partner',string="Partner",index=True, required=True)
    doc_id         = fields.Many2one('res.partner.doc',string="Document model")
    requested_date = fields.Datetime('Requisted date')
    state          = fields.Selection([('draft', 'Draft'),('free', 'Free'),('paid', 'Paid')], string='State',compute="get_state") 
    order_id       = fields.Many2one('sale.order',"Sale")     

    def get_state(self):
        for rec in self:
            rec.state = 'draft'
            if rec.doc_id.is_free:
                rec.state = 'free' 
            elif rec.order_id:
                if rec.order_id.state!='draft':
                    rec.state = 'paid'

