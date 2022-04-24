# -*- coding: utf-8 -*-

from venv import create
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    reports_name      = fields.Text('reports name') 
    
    firstname         = fields.Char("First name", index=True)
    lastname          = fields.Char("Last name", index=True)
    lastname2         = fields.Char("Second last name",)   
    gender            = fields.Selection([("male", "Male"), ("female", "Female"), ("other", "Other")])
    nationality_id    = fields.Many2one("res.country", "Nationality")
    birthdate_date    = fields.Date("Birthdate")
    age               = fields.Integer(string="Age", readonly=True, compute="_compute_age")
    family_situation  = fields.Selection(string='Family situation',selection=[('single', 'Single'),
                                                                             ('married', 'Married'),
                                                                             ('divorced', 'Divorced'),
                                                                             ('widow','Widow / Widower'),
                                                                             ('separated','Separated'),
                                                                             ])
  
    country_of_birth_id = fields.Many2one('res.country',string='Country of birth')
    Place_of_birth      = fields.Char('Place of birth')
    Profession          = fields.Selection(string='Profession',selection=[('entrepreneur','Entrepreneur'),('student','Student'),('employee','Employee'),('sector','Sector'),('retired','Retired'),])
    passport_number  = fields.Char('Passport number')
    delivered_by     = fields.Char('Delivered by') 
    Passport_delivery_date   = fields.Date('Passport delivery date')
    Passport_expiration_date = fields.Date('Passport expiration date')
    Spouses_name     = fields.Char("Spouse's name")
    Fathers_name     = fields.Char("Father's name")
    document_type    = fields.Char("Document type")
    foreigner_identity_number = fields.Char('Foreigner Identity Number (NIE)')
    reasons    = fields.Selection(string='For economic interests',selection=[('For_economic_interests','For economic interests'),
                                                                             ('for_professional_interests','For professional interests'),
                                                                             ('for_social_interests','For social interests'),
                                                                                    
                                                                                    ] )
    specify = fields.Selection(string='Specify',selection=[('company_creation','Company creation'),
                                                                             ('studies','studies'),
                                                                             ('buy_hous','Buy hous'),
                                                                             ('open_bank_account','Open bank account'),
                                                                             ('other','Other'),
                                                                                    ])                                                                               
    place_of_presentation =  fields.Selection(string='Place of presentation',selection=[('immigration_Office','Immigration Office'),
                                                                             ('police_station','Police station'),
                                                                             ('consular_office','Consular office'),
                                                                    
                                                                                    ])   
    ######################                                                                                
    building_no           =  fields.Char('Building N°')   
    floor_no              =  fields.Char('Floor N°')   
    mothers_name          =  fields.Char("Mother's name")   
    request_nie           =  fields.Date('Request NIE')    


    @api.onchange('firstname','lastname','lastname2')
    def _onchange_firstname_lastname_lastname2(self):
       self.name = " ".join(p for p in (self.firstname, self.lastname,self.lastname2) if p)

      
       

    @api.depends("birthdate_date")
    def _compute_age(self):
        for record in self:
            age = 0
            if record.birthdate_date:
                age = relativedelta(fields.Date.today(), record.birthdate_date).years
            record.age = age

    def do_print_report(self,id):
       report_obj = self.env['ir.actions.report']
       # report = report_obj._get_report_from_name('account.account_invoices')
       # return {
       #      'doc_ids': [1],
       #      'doc_model': 'account.move',
       #      'docs': self,
       #  }
       # return self.env.ref('').report_action(id)



class SaleOrder(models.Model):
    _inherit = 'sale.order' 
    
    
    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        _logger.warning('\n ok ok vals=>%s',vals)
        return res

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line' 
    
    
    @api.model
    def create(self, vals):
        res = super(SaleOrderLine, self).create(vals)
        _logger.warning('\n ok ok vals line=>%s',vals)
        return res