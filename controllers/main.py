# -*- coding: utf-8 -*-

import babel.dates
import pytz
import re
from ast import literal_eval
from dateutil.parser import parse
from odoo import fields, http, _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)
from PyPDF2 import  PdfFileReader, PdfFileWriter
import base64
import werkzeug
from werkzeug import urls
import ast

class WebsitepartnerDocController(http.Controller):
    def sitemap_docs(env, rule, qs):
        if not qs or qs.lower() in '/partner_docs':
            yield {'loc': '/partner_docs'}
 

    # ------------------------------------------------------------
    # Partner Doc LIST
    # ------------------------------------------------------------

    @http.route(['/partner_docs'], type='http', auth="public", website=True, sitemap=sitemap_docs)
    def docs(self, page=1, **searches):
        _logger.warning('\n ok ok ********************************')
        Docs = request.env['res.partner.doc'].sudo().search([('is_published','=',True)])
        values = {
            'docs': Docs, 
        }
        return request.render("manage_partner_documents.index", values)


    @http.route(['/partner_doc/<int:doc>'], type='http', auth="public", website=True, sitemap=sitemap_docs)
    def one_doc(self, doc):
        _logger.warning('\n ok ok doc=>%s',doc)
        Doc = request.env['res.partner.doc'].sudo().search([('id','=',doc)])
        
        values = {
            'doc': Doc, 
        }

        return request.render("manage_partner_documents.partner_doc_one", values)



    @http.route(['/partner_doc/<int:doc>/registration/new'], type='http', auth="user",website=True,)
    def registration_new(self, doc):
        Doc = request.env['res.partner.doc'].sudo().search([('id','=',doc)])

        default_first_attendee = {
                "name":                      request.env.user.partner_id.name,
                "email":                     request.env.user.partner_id.email,
                "phone":                     request.env.user.partner_id.mobile or request.env.user.partner_id.phone,
                "countries":                 request.env['res.country'].sudo().search([]),
                "states":                    request.env['res.country.state'].sudo().search([]),
                "firstname":                 request.env.user.partner_id.firstname,      
                "lastname":                  request.env.user.partner_id.lastname,     
                "lastname2":                 request.env.user.partner_id.lastname2,   
                "gender":                    request.env.user.partner_id.gender,  
                "nationality_id":            request.env.user.partner_id.nationality_id.name, 
                "birthdate_date":            request.env.user.partner_id.birthdate_date, 
                "age":                       request.env.user.partner_id.age, 
                "family_situation":          request.env.user.partner_id.family_situation, 
                "country_of_birth_id":       request.env.user.partner_id.country_of_birth_id.name, 
                "Place_of_birth":            request.env.user.partner_id.Place_of_birth, 
                "Profession":                request.env.user.partner_id.Profession, 
                "passport_number":           request.env.user.partner_id.passport_number, 
                "delivered_by":              request.env.user.partner_id.delivered_by, 
                "Passport_delivery_date":    request.env.user.partner_id.Passport_delivery_date, 
                "Passport_expiration_date":  request.env.user.partner_id.Passport_expiration_date, 
                "Spouses_name":              request.env.user.partner_id.Spouses_name, 
                "Fathers_name":              request.env.user.partner_id.Fathers_name, 
                "document_type":             request.env.user.partner_id.document_type, 
                "foreigner_identity_number": request.env.user.partner_id.foreigner_identity_number, 
                "reasons":                   request.env.user.partner_id.reasons, 
                "specify":                   request.env.user.partner_id.specify,                                                    
                "place_of_presentation":     request.env.user.partner_id.place_of_presentation, 
                "building_no":               request.env.user.partner_id.building_no, 
                "floor_no":                  request.env.user.partner_id.floor_no, 
                "mothers_name":              request.env.user.partner_id.mothers_name, 
                "request_nie":               request.env.user.partner_id.request_nie, 

                        }

                        
        values = {
            'default_first_attendee': default_first_attendee,
            'doc': Doc,
        }    

          


        return request.render("manage_partner_documents.registration_attendee_details", values)

    @http.route(['/partner_doc/print/<model("res.partner.doc.request"):doc>'], type='http', auth="user", methods=['GEt'], website=True)
    def print_report(self, doc, **post): 
        pdf_writer = PdfFileWriter()
        partner = request.env.user.partner_id
        pdf_content = doc.doc_id.sudo().report_id.sudo()._render_qweb_pdf(partner.id)[0]        
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf_content)),('Content-Disposition', 'attachment; filename='+partner.name+'.pdf'),]
        return request.make_response(pdf_content, headers=pdfhttpheaders)    
    

    @http.route(['/partner_doc/<model("res.partner.doc"):doc>/registration/confirm'], type='http', auth="user", methods=['POST'], website=True)
    def registration_confirm(self, doc, **post):
        _logger.warning('\n ok ok post=>%s',post)
        _logger.warning('\n ok ok doc=>%s',doc)
        request.env.user.partner_id.write({
                    'lastname'                      : post.get('lastname'),
                    'lastname2'                     : post.get('lastname2'),
                    'firstname'                     : post.get('firstname'),
                    'family_situation'              : post.get('family_situation'),
                    'country_of_birth_id'           : post.get('country_of_birth_id'),
                    'Place_of_birth'                : post.get('Place_of_birth'),
                    'Profession'                    : post.get('Profession'),
                    'passport_number'               : post.get('passport_number'),
                    'delivered_by'                  : post.get('delivered_by'),
                    'Passport_delivery_date'        : post.get('Passport_delivery_date'),
                    'Passport_expiration_date'      : post.get('Passport_expiration_date'),
                    'Spouses_name'                  : post.get('Spouses_name'),
                    'Fathers_name'                  : post.get('Fathers_name'),
                    'document_type'                 : post.get('document_type'),
                    'reasons'                       : post.get('reasons'),
                    'specify'                       : post.get('specify'),                                                 
                    'place_of_presentation'         : post.get('place_of_presentation'),                                                                
                    'building_no'                   : post.get('building_no'),
                    'floor_no'                      : post.get('floor_no'),
                    'mothers_name'                  : post.get('mothers_name'),
                            }) 

        if doc.is_free:
            pdf_writer = PdfFileWriter()
            partner = request.env.user.partner_id
            pdf_content = doc.sudo().report_id.sudo()._render_qweb_pdf(partner.id)[0]        
            pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf_content)),('Content-Disposition', 'attachment; filename='+partner.name+'.pdf'),]
            return request.make_response(pdf_content, headers=pdfhttpheaders)    
            
        elif not(doc.is_free):
            product_id = request.env['product.product'].create({'name':doc.name,'detailed_type':'service','taxes_id':[],'list_price':doc.price,'standard_price':doc.price})
            new_order = request.env['sale.order'].create({
                    'partner_id': request.env.user.partner_id.id, 
                    # 'pricelist_id':False , # request.env.user.partner_id.pricelist_id, 
                    'payment_term_id': 1, 
                    'team_id': 2, 
                    'partner_invoice_id': request.env.user.partner_id.id, 
                    'partner_shipping_id': request.env.user.partner_id.id, 
                    'user_id': False, 
                    'website_id': request.website.id, 
                    'company_id': 1, 
                    # 'warehouse_id': 1, 
                    'name': '/1000/',
                    'order_line':[(0, 0,  { 
                        'product_id': product_id.id, 
                        'product_uom_qty': 1, 
                        'product_uom': 1, 
                        'price_unit': doc.price, 
                        'discount': 0, 
                        'customer_lead': 0.0, 
                        'name': doc.name, 
                        'tax_id': [], })]
                    })

            new_doc_request_id = request.env['res.partner.doc.request'].create({
                                        "partner_id"     : request.env.user.partner_id.id, 
                                        "doc_id"         : doc.id,
                                        "requested_date" : fields.Datetime.now(),
                                        "order_id"       : new_order.id
                                    })

            _logger.warning('\n ok ok new_order=>%s',new_order)

            return request.redirect("/shop/payment")
           