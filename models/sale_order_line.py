# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def write(self, vals):
        """Apply or clear packaging discount when product_packaging_id changes."""
        if "product_packaging_id" in vals:
            packaging_id = vals.get("product_packaging_id")
            packaging = (
                self.env["product.packaging"].browse(packaging_id)
                if packaging_id
                else self.env["product.packaging"]
            )
            if "discount" not in vals:
                if packaging and getattr(packaging, "packaging_discount", 0):
                    vals["discount"] = packaging.packaging_discount
                else:
                    vals["discount"] = 0.0
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
