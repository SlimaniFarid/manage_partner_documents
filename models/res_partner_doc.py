# -*- coding: utf-8 -*-


from datetime import datetime
import random
import json

from odoo import api, models, fields,tools, _
from odoo.addons.http_routing.models.ir_http import slug, unslug
from odoo.tools.translate import html_translate
from odoo.tools import html2plaintext

import logging
_logger = logging.getLogger(__name__)

class ResPartnerDoc(models.Model):
    _name = 'res.partner.doc'
    _inherit = [
        'mail.thread',
     
        'mail.activity.mixin'
    ]


    name            = fields.Char('Title',index=True, required=True,translate=True)
    subtitle        = fields.Char('Subtitle',translate=True)
    content         = fields.Html('Content', translate=True)
    partner_ids     = fields.Many2many('res.partner', string='Partners')
    is_published    = fields.Boolean('Is published')
    company_id      = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id     = fields.Many2one('res.currency', related='company_id.currency_id', string='Currency')
    report_id       = fields.Many2one('ir.actions.report', string='PDF Document')
    is_free         = fields.Boolean('Is free',default=True) 
    price           = fields.Monetary(string='Price',digits='Product Price',default=0.0)


    image_1920  = fields.Image("Image", max_width=1920, max_height=1920)
    image_1024  = fields.Image("Image 1024", related="image_1920", max_width=1024, max_height=1024, store=True)
    image_512   = fields.Image("Image 512", related="image_1920", max_width=512, max_height=512, store=True)
    image_256   = fields.Image("Image 256", related="image_1920", max_width=256, max_height=256, store=True)
    image_128   = fields.Image("Image 128", related="image_1920", max_width=128, max_height=128, store=True)
    can_image_1024_be_zoomed = fields.Boolean("Can Variant Image 1024 be zoomed", compute='_compute_can_image_1024_be_zoomed', store=True)
    
    @api.onchange('is_free')
    def _onchange_is_free(self):
        if self.is_free:
            self.price = 0.0
   

    @api.depends('image_1920', 'image_1024')
    def _compute_can_image_1024_be_zoomed(self):
        for rec in self:
            rec.can_image_1024_be_zoomed = rec.image_1920 and tools.is_image_size_above(rec.image_1920, rec.image_1024)



