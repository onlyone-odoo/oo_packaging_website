# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    website_force_packaging = fields.Boolean(
        string="Website: Only Sell by Packaging",
        default=False,
        help="When enabled, the product can only be purchased in packaging "
        "multiples on the website (the unit option is hidden and +/- "
        "buttons work in packaging steps).",
    )
