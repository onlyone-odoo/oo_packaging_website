# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html).

from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def write(self, vals):
        """Apply or clear packaging discount when product_packaging_id changes.

        We copy vals to avoid mutating the caller's dictionary (good practice).
        This works for both single and multi-record writes.
        """
        if "product_packaging_id" in vals and "discount" not in vals:
            packaging_id = vals.get("product_packaging_id")
            packaging = self.env["product.packaging"].browse(packaging_id).exists()
            discount = packaging.packaging_discount if packaging else 0.0
            vals = dict(vals, discount=discount)
        return super().write(vals)

    @api.onchange("product_packaging_id")
    def _onchange_product_packaging_id_packaging_discount(self):
        """Suggest discount in backend when packaging is changed."""
        if self.product_packaging_id and getattr(
            self.product_packaging_id, "packaging_discount", 0
        ):
            self.discount = self.product_packaging_id.packaging_discount
        elif self.product_packaging_id:
            self.discount = 0.0
