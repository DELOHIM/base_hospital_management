# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import models, fields


class Hospital(models.Model):
    _name = 'hospital.hospital'
    _description = 'Hôpital'
    _rec_name = 'hosp_name'
    
    hosp_name = fields.Char(string="Nom", help="Nom de l'hôpital")
    hosp_type = fields.Selection([('hospital', 'Hôpital'),
                                  ('multi', 'Multi-Hôpital'),
                                  ('nursing', 'Maison de retraite'),
                                  ('clinic', 'Clinique'),
                                  ('community', 'Centre de santé communautaire'),
                                  ('military', 'Centre médical militaire'),
                                  ('other', 'Autre')],
                                 string="Type d'institution")
    phone = fields.Char('Téléphone')
    mobile = fields.Char('Mobile')
    email = fields.Char('Email')
    hosp_phone = fields.Char('Téléphone')
    hosp_mobile = fields.Char('Mobile')
    hosp_email = fields.Char('Email')
    hosp_address = fields.Char('Adresse de travail')
    hosp_street = fields.Char('Rue')
    hosp_street2 = fields.Char('Rue 2')
    hosp_zip = fields.Char('Code postal')
    hosp_city = fields.Char('Ville')
    hosp_state_id = fields.Many2one("res.country.state", string='État')
    hosp_country_id = fields.Many2one('res.country', string='Pays')
    note = fields.Text('Note')
    image_129 = fields.Image(max_width=128, max_height=128)
