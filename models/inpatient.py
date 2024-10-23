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
import datetime


class Patient(models.Model):
    _name = 'hospital.inpatient'
    _description = 'Patient'
    _rec_name = 'patient_id'
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']

    patient_id = fields.Many2one('res.partner', string="Nom du Patient", required=True)
    patient_name = fields.Char("Nom du Patient", related='patient_id.name')
    reason = fields.Char(string="Raison de l'Admission", help="Raison actuelle de l'hospitalisation du patient")
    building_id = fields.Many2one('hospital.buildings', string="Nom du Bloc", required=True)
    ward_id = fields.Many2one('hospital.wards', string='Service')
    bed_id = fields.Many2one('hospital.beds', string='Lit')
    room_no = fields.Many2one('patient.room')
    type_admission = fields.Selection([('emergency', 'Admission d Urgence'),
                                       ('routine', 'Admission Routinière')],
                                      string="Type d'Admission", required=True)
                                      
    attending_doctor = fields.Many2one('hr.employee', string="Médecin Responsable", domain="[('is_doctor','=','doctor')]")
    operating_doctor = fields.Many2one('hr.employee', string="Médecin Opérant", domain="[('is_doctor','=','doctor')]")
    hosp_date = fields.Date(string="Date d'Hospitalisation", required=True)
    discharge_date = fields.Date(string="Date de Sortie")
    condition = fields.Text(string="État Avant Hospitalisation", help="L'état du patient lors de son admission à l'hôpital")
    nursing_plan = fields.Text(string="Plan de Soins")
    discharge_plan = fields.Text(string="Plan de Sortie")
    notes = fields.Text(string="Notes")
    pvt_rooms = fields.Boolean("Chambres Privées")
    room_id = fields.Many2one('patient.room', string='Chambres')
    room_rent = fields.Monetary(string='Loyer', related='room_id.rent')
    bed_rent = fields.Monetary(string='Loyer', related='bed_id.bed_rent')
    facilities_ids = fields.Many2many(string='Installations', related='room_id.facilities_ids')
    ward_facilities_ids = fields.Many2many(string='Installations', related='ward_id.facilities')
    currency_id = fields.Many2one('res.currency', 'Monnaie',
                                   default=lambda self: self.env.user.company_id.currency_id.id,
                                   required=True)
    state = fields.Selection([('draft', 'Brouillon'), ('reserve', 'Réservé'),
                              ('Admit', 'Admis'), ('invoice', 'Facturé'), ('dis', 'Sorti')],
                             string='État', readonly=True,
                             default="draft")
    rent_amount = fields.Monetary(string="Montant du Loyer", compute='_compute_amount')
    bed_rent_amount = fields.Monetary(string="Montant du Loyer", compute='_bed_compute_amount')
    days = fields.Integer(string='Jours')
    invoice_id = fields.Many2one('account.move')
    admit_days = fields.Integer(string='Jours', compute='_compute_days')

    @api.onchange('bed_id')
    def onchange_bed(self):
        """Désassigner les lits"""
        val = self.env['hospital.beds'].search([('id', '=', self.bed_id.id)])
        for rec in val:
            rec.write({'state': 'not'})

    @api.onchange('discharge_date')
    def onchange_discharge(self):
        """Assigner les lits"""
        val = self.env['hospital.beds'].search([('id', '=', self.bed_id.id)])
        if val.date_bed_assign < self.discharge_date:
            for rec in val:
                rec.write({'state': 'avail'})
        else:
            for rec in val:
                rec.write({'state': 'not'})

    def action_invoice(self):
        self.state = 'invoice'

        inv_line_list = []
        for rec in self:
            inv_line = (0, 0, {'name': rec.patient_id.name,
                               'price_unit': rec.bed_rent_amount,
                               'quantity': rec.admit_days})
            inv_line_list.append(inv_line)
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'date': fields.Date.today(),
            'invoice_date': fields.Date.today(),
            'partner_id': self.patient_id.id,
            'invoice_line_ids': inv_line_list
        })
        self.invoice_id = invoice.id
        return {
            'name': 'Facture',
            'res_model': 'account.move',
            'view_mode': 'form',
            'view_Id': self.env.ref('account.view_move_form').id,
            'context': "{'move_type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'res_id': invoice.id
        }

    def _compute_days(self):
        if self.hosp_date:
            if self.discharge_date:
                self.admit_days = (self.discharge_date - self.hosp_date + datetime.timedelta(days=1)).days
            else:
                self.admit_days = (fields.Date.today() - self.hosp_date + datetime.timedelta(days=1)).days

    def _compute_amount(self):
        if self.hosp_date:
            if self.discharge_date:
                self.days = (self.discharge_date - self.hosp_date + datetime.timedelta(days=1)).days
                self.rent_amount = self.room_id.rent * self.days
            else:
                self.days = (fields.Date.today() - self.hosp_date + datetime.timedelta(days=1)).days
                self.rent_amount = self.room_id.rent * self.days
        else:
            self.rent_amount = self.room_id.rent

    def _bed_compute_amount(self):
        if self.hosp_date:
            if self.discharge_date:
                self.days = (self.discharge_date - self.hosp_date + datetime.timedelta(days=1)).days
                self.bed_rent_amount = self.bed_id.bed_rent * self.days
            else:
                self.days = (fields.Date.today() - self.hosp_date + datetime.timedelta(days=1)).days
                self.bed_rent_amount = self.bed_id.bed_rent * self.days
        else:
            self.bed_rent_amount = self.bed_id.bed_rent

    def action_admit(self):
        self.state = 'Admit'
        self.bed_id.state = "not"
        self.room_id.state = "not"

    def action_reserve(self):
        self.state = 'reserve'
        self.room_id.state = 'reserve'

    def action_discharge(self):
        self.state = 'dis'
        self.bed_id.state = "avail"
        self.room_id.state = 'avail'

    @api.onchange('building_id')
    def _onchange_ward(self):
        return {'domain': {
            'ward_id': [
                ('building_id', '=', self.building_id.id),
            ]}}

    @api.onchange('ward_id')
    def _onchange_ward_beds(self):
        return {'domain': {
            'bed_id': [
                ('ward_id', '=', self.ward_id.id),
                ('state', '=', 'avail')
            ]}}

    @api.onchange('ward_id')
    def _onchange_ward_rooms(self):
        return {'domain': {
            'room_id': [
                ('ward_id', '=', self.ward_id.id),
                ('state', '=', 'avail')
            ]}}
