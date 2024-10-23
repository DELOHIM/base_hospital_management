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


class Diagnosis(models.Model):
    _name = 'hospital.diagnosis'
    _description = 'Diagnostic'
    _rec_name = 'diagnosis_seq'

    patient_name = fields.Char('Nom', related='patient_seq_id.name')
    dob = fields.Date('Date de Naissance', related='patient_seq_id.dob')
    diagnosis_date = fields.Datetime('Date', default=fields.Datetime.now,
                                     help="La date à laquelle le médecin consulte le patient")
    diagnosis_type = fields.Selection([
        ('home', 'Consultation à Domicile'),
        ('telephone', 'Consultation Téléphonique'),
        ('hospital', 'Consultation à l’Hôpital'),
        ('nursing', 'Consultation à Domicile de Soins'),
        ('clinic', 'Consultation en Clinique'),
        ('community', 'Consultation au Centre de Santé Communautaire'),
        ('other', 'Autre')],
        string="Mode de diagnostic")
    gender = fields.Selection('Genre', related='patient_seq_id.gender')
    patient_age = fields.Integer('Âge', related='patient_seq_id.patient_age')
    phone = fields.Char('Numéro de Téléphone', related='patient_seq_id.phone')
    mobile = fields.Char('Numéro de Mobile', related='patient_seq_id.mobile')
    email = fields.Char('Email', related='patient_seq_id.email')
    diagnosis_seq = fields.Char(string='N° SI', required=True, copy=False,
                                readonly=True, index=True,
                                default=lambda self: 'Nouveau')
    patient_seq_id = fields.Many2one('res.partner', 'Code du Patient')
    note = fields.Html('Note', sanitize_style=True)
    prescription_ids = fields.One2many('hospital.prescription', 'diagnosis_id', "Prescription")
    diagnosis_count = fields.Integer(string="Nombre", compute="_compute_count", help="Nombre total de consultations")
    payment_state = fields.Selection([('paid', 'Payé'), ('not_paid', 'Partiel'),
                                      ('in_payment', 'En Paiement')],
                                     default='not_paid')

    @api.constrains('prescription_ids')
    @api.onchange('prescription_ids')
    def onchange_medicine(self):
        """Création des médicaments dans l'ordonnance"""
        vals = []
        for rec in self.prescription_ids:

            if rec.pharmacy_id and rec.medicine_id:
                vals.append((0, 0, {'prescription_id': rec.id,
                                    'medicine_id': rec.medicine_id.id}))
                vals.append(vals)
            rec.prescription_ids = vals

    @api.model
    def create(self, vals):
        if vals.get('diagnosis_seq', 'Nouveau') == 'Nouveau':
            vals['diagnosis_seq'] = self.env['ir.sequence'].next_by_code(
                'patients.diagnosis') or 'Nouveau'
        result = super(Diagnosis, self).create(vals)
        return result
