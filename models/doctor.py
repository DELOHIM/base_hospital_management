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


class HospitalDoctors(models.Model):
    _inherit = 'hr.employee'

    is_doctor = fields.Selection(string='Désignation',
                                 selection=[('employee', 'Employé'), ('doctor', 'Médecin')],
                                 default='employee')
    pharmacy_id = fields.Many2one('hospital.pharmacy', string="Pharmacie", required=True)
    consultancy_charge = fields.Monetary(string="Frais de Consultation")
    consultancy_type = fields.Selection([('resident', 'Résident'),
                                         ('special', 'Spécialiste')],
                                        string="Type de Consultation")
    currency_id = fields.Many2one('res.currency', 'Devise',
                                  default=lambda self: self.env.user.company_id
                                  .currency_id.id,
                                  required=True)
    degrees = fields.Many2many('hospital.degree', string="Diplômes")
    institute = fields.Many2many('hospital.institution',
                                 string="Nom de l'Institution")
    specialization = fields.Many2many('hospital.specialization',
                                      string="Spécialisation", help="Spécialisation des médecins dans un domaine")
    prescription_ids = fields.One2many('hospital.prescription', 'pharmacy_id', 'Ordonnance')
    pharmacy_ids = fields.One2many('hospital.pharmacy', 'doctor_id', 'Pharmacie')
