# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from operator import itemgetter

from odoo import http, _
from odoo.http import request
from odoo.osv.expression import AND, OR
from odoo.tools import groupby as groupbyelem

from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager
import logging
_logger = logging.getLogger(__name__)


class AppointmentPortal(portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'docs_count' in counters:
            docs = request.env['res.partner.doc.request'].search([])
            nb=0
            for d in docs:
                if d.partner_id.id == request.env.user.partner_id.id:
                    if d.doc_id.is_free or d.doc_id.order_id.state=='darft':
                        nb+=1
            values['docs_count'] =   nb    
        return values

    @http.route(['/my/documents'], type='http', auth="user", website=True)
    def portal_my_documents(self,**kw):
        values = self._prepare_portal_layout_values()
        AccountInvoice = request.env['account.move']
        docs = request.env['res.partner.doc.request'].search([])
        nb=0
        docs_list = []
        for d in docs:
            if d.partner_id.id == request.env.user.partner_id.id:
                if d.doc_id.is_free or d.doc_id.order_id.state=='darft':
                    docs_list.append(d)
      
       
       

        searchbar_sortings = {
            'date': {'label': _('Date'), 'order': 'invoice_date desc'},
            'duedate': {'label': _('Due Date'), 'order': 'invoice_date_due desc'},
            'name': {'label': _('Reference'), 'order': 'name desc'},
            'state': {'label': _('Status'), 'order': 'state'},
        }
       
       
       
       
        values.update({
            'Docs': docs_list,
            'searchbar_sortings': {},
            'sortby': {},
            'searchbar_filters': {},
            'filterby':{},
        })
        return request.render("manage_partner_documents.portal_my_documents", values)

   
   