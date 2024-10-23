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


class Buildings(models.Model):
    _name = 'hospital.buildings'
    _description = 'Bâtiments'
    _rec_name = 'building_name'

    building_name = fields.Char(string="Bloc", required="True")
    institution_id = fields.Many2one('hospital.hospital', string="Institution")
    notes = fields.Text(string="Notes")

    buildings_seq = fields.Char(string='Code du Bloc', required=True,
                                copy=False, readonly=True, index=True,
                                default=lambda self: 'Nouveau')
    phone = fields.Char(string='Téléphone')
    mobile = fields.Char(string='Mobile')
    email = fields.Char(string='Email')
    bed_count = fields.Integer(string="Nombre de lits", compute="_compute_count")
    ward_count = fields.Integer(string="Nombre de services", compute="_compute_ward_count")

    @api.model
    def create(self, vals):
        if vals.get('buildings_seq', 'Nouveau') == 'Nouveau':
            vals['buildings_seq'] = self.env['ir.sequence'].next_by_code(
                'building.sequence') or 'Nouveau'
        result = super(Buildings, self).create(vals)
        return result

    def open_building_bed(self):
        """Création de lits dans les bâtiments"""
        return {
            'name': 'Lits',
            'domain': [('building_id', '=', self.id)],
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.beds',
            'view_mode': 'tree',
            'context': {'create': False},
        }

    def _compute_count(self):
        """Compter le nombre de lits"""
        count = self.env['hospital.beds'].search_count([(
            'building_id', '=', self.building_name)])
        self.bed_count = count

    def open_building_ward(self):
        """Création de services dans les bâtiments"""
        return {
            'name': 'Services',
            'domain': [('building_id', '=', self.building_name)],
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.wards',
            'view_mode': 'tree',
            'context': {'create': False},
        }

    def _compute_ward_count(self):
        """Compter les services dans le bâtiment"""
        count = self.env['hospital.wards'].search_count([(
            'building_id', '=', self.building_name)])
        self.ward_count = count
