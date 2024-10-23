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
from odoo import models, fields, api
from datetime import date, timedelta


class Lab(models.Model):
    _name = 'hospital.labs'
    _description = 'Laboratoire'
    _rec_name = 'name'

    name = fields.Char('Laboratoire', required=True)
    institution_id = fields.Many2one('hospital.hospital', string="Institution", required=True)
    building_id = fields.Many2one('hospital.buildings', 'Bloc', required=True)
    ward_no = fields.Many2one('hospital.wards', 'Salle', required=True)
    notes = fields.Text('Notes')
    image_130 = fields.Image(max_width=128, max_height=128)
    phone = fields.Char('Téléphone')
    mobile = fields.Char('Mobile')
    labs_phone = fields.Char('Téléphone')
    labs_mobile = fields.Char('Mobile')
    labs_email = fields.Char('Email')
    labs_address = fields.Char('Adresse de travail')
    labs_street = fields.Char('Rue')
    labs_street2 = fields.Char('Rue 2')
    labs_zip = fields.Char('Code postal')
    labs_city = fields.Char('Ville')
    labs_state_id = fields.Many2one("res.country.state", string='État')
    labs_country_id = fields.Many2one('res.country', string='Pays')
    labs_note = fields.Text('Note')
    lab_seq = fields.Char(string='Séquence de laboratoire', required=True,
                          copy=False,
                          readonly=True,
                          index=True,
                          default=lambda self: 'New')
    technician_id = fields.Many2one('hr.employee', string="Technicien de laboratoire",
                                     domain=[('job_title', '=', 'Technicien de laboratoire')])

    @api.onchange('institution_id')
    def _ward_bed(self):
        """À partir de l'institution, les salles de lit sont calculées"""

        return {'domain': {
            'building_id': [
                ('institution_id', '=', self.institution_id.id),
            ]}}

    @api.onchange('building_id')
    def _ward(self):
        return {'domain': {
            'ward_id': [
                ('building_id', '=', self.building_id.id),
            ]}}

    @api.model
    def create(self, vals):
        if vals.get('lab_seq', 'New') == 'New':
            vals['lab_seq'] = self.env['ir.sequence'].next_by_code(
                'lab.sequence') or 'New'
        result = super(Lab, self).create(vals)
        return result
