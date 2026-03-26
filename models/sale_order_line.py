# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html).

from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends("product_packaging_id")
    def _compute_discount(self):
        """Extend discount computation to apply packaging discount.

        The core compute sets discount from pricelist rules. We override it
        to use the packaging_discount when a packaging with a discount is
        selected, taking the higher of the two (pricelist vs packaging).
        """
        super()._compute_discount()
        for line in self:
            if not line.product_packaging_id:
                continue
            pkg_discount = getattr(
                line.product_packaging_id, "packaging_discount", 0
            )
            if pkg_discount and pkg_discount > line.discount:
                line.discount = pkg_discount

    @api.onchange("product_packaging_id")
    def _onchange_product_packaging_id_packaging_discount(self):
        """Suggest discount in backend when packaging is changed."""
        if self.product_packaging_id and getattr(
            self.product_packaging_id, "packaging_discount", 0
        ):
            self.discount = self.product_packaging_id.packaging_discount
