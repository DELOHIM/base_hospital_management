# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-AUJOURD'HUI Cybrosys Technologies(<https://www.cybrosys.com>)
#    Auteur : Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    Vous pouvez le modifier selon les termes de la GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    Ce programme est distribué dans l'espoir qu'il sera utile,
#    mais SANS AUCUNE GARANTIE ; sans même la garantie implicite de
#    COMMERCIALISATION ou d'ADÉQUATION À UN BUT PARTICULIER. Voir la
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) pour plus de détails.
#
#    Vous devriez avoir reçu une copie de la GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) avec ce programme.
#    Sinon, consultez <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import models, fields, api


class ProductMedicine(models.Model):
    _inherit = 'product.template'
    marque = fields.Char('Marque')
    currency_id = fields.Many2one('res.currency', 'Monnaie',
                                   default=lambda self: self.env.user.company_id
                                   .currency_id.id,
                                   required=True)
    medicine_ok = fields.Boolean('Médicament')
    prix_produit = fields.Monetary('Prix', help="Prix des produits")

    @api.onchange('medicine_ok')
    def onchange_product_type(self):
        self.type = 'consu'
        self.list_price = self.prix_produit
