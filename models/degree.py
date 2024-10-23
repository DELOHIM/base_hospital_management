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


class Degree(models.Model):
    _name = 'hospital.degree'
    _description = 'Diplôme'
    _rec_name = 'degree'

    degree = fields.Char(string="Diplôme du Médecin", required="True")


class Specialization(models.Model):
    _name = 'hospital.specialization'
    _description = "Spécialisation du Médecin"
    _rec_name = 'specialization'

    specialization = fields.Char(string="Spécialisation du Médecin",
                                 required="True")


class Institution(models.Model):
    _name = 'hospital.institution'
    _description = "Institution du Médecin"
    _rec_name = 'institution'

    institution = fields.Char(string="Institution du Médecin", required="True")
