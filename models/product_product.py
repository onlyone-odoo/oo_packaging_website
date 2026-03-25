# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    website_force_packaging = fields.Boolean(
        string="Website: Only Sell by Packaging",
        default=False,
        help="When enabled, this variant can only be purchased in packaging "
        "multiples on the website (the unit option is hidden and +/- "
        "buttons step by packaging quantity).",
    )
