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
from odoo.fields import Date


class Beds(models.Model):
    _name = 'hospital.beds'
    _description = 'Lits'
    _rec_name = 'bed_no'

    bed_no = fields.Char(string="Numéro de lit", required="True")
    _sql_constraints = [('unique_room', 'unique (bed_no)',
                         'Le numéro de lit doit être unique !')]
    bed_type = fields.Selection([('gatch', 'Lit à treillis'),
                                 ('electric', 'Lit électrique'),
                                 ('stretcher', 'Brancard'),
                                 ('low', 'Lit bas'),
                                 ('air', 'Lit à basse perte d\'air'),
                                 ('circo', 'Circo électrique'),
                                 ('clinitron', 'Clinitron'),
                                 ], string="Type de lit",
                                )
    note = fields.Text(string="Notes")
    date_bed_assign = fields.Date(default=Date.today(), string='Date d\'affectation')
    ward_id = fields.Many2one('hospital.wards', string="Numéro de service")
    institution_id = fields.Many2one('hospital.hospital', string="Institution")
    building_id = fields.Many2one('hospital.buildings', string="Bloc")

    currency_id = fields.Many2one('res.currency', 'Monnaie',
                                  default=lambda self: self.env.user.company_id.currency_id.id,
                                  required=True)
    repair_charge = fields.Monetary(string='Frais de réparation', help="Frais de réparation en cas de dommage")
    bed_rent = fields.Monetary(string='Loyer', help="Frais pour le lit")
    repair_date = fields.Date(string='Date de réparation', help="Date de la prochaine réparation")
    state = fields.Selection([('avail', 'Disponible'), ('not', 'Indisponible')], string='État', readonly=True,
                             default="avail")

    @api.onchange('institution_id')
    def _onchange_ward_bed(self):
        """bâtiment"""
        return {'domain': {
            'building_id': [
                ('institution_id', '=', self.institution_id.id),
            ]}}

    @api.onchange('building_id')
    def _onchange_ward(self):
        """service"""
        return {'domain': {
            'ward_id': [
                ('building_id', '=', self.building_id.id),
            ]}}

    def action_assign(self):
        """changement d'état"""
        self.state = "not"
