# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _cart_find_product_line(self, product_id, line_id=None, **kwargs):
        """Include product_packaging_id so lines with same product but different packaging are separate."""
        lines = super()._cart_find_product_line(
            product_id, line_id=line_id, **kwargs
        )
        product_packaging_id = kwargs.get("product_packaging_id")
        if product_packaging_id is not None and lines:
            lines = lines.filtered(
                lambda l: l.product_packaging_id.id == product_packaging_id
            )
        return lines

    def _prepare_order_line_values(
        self, product_id, quantity, product_custom_attribute_values=None, **kwargs
    ):
        """Add product_packaging_id and discount when packaging_id is passed from website."""
        values = super()._prepare_order_line_values(
            product_id,
            quantity,
            product_custom_attribute_values=product_custom_attribute_values,
            **kwargs,
        )
        packaging_id = kwargs.get("product_packaging_id") or kwargs.get(
            "packaging_id"
        )
        if packaging_id:
            packaging = self.env["product.packaging"].browse(
                int(packaging_id)
            ).exists()
            if packaging and packaging.product_id.id == product_id:
                values["product_packaging_id"] = packaging.id
                values["product_packaging_qty"] = quantity / packaging.qty
                if getattr(packaging, "packaging_discount", 0):
                    values["discount"] = packaging.packaging_discount
        return values

    def _cart_update(
        self,
        product_id=None,
        line_id=None,
        add_qty=0,
        set_qty=0,
        product_packaging_id=None,
        packaging_id=None,
        **kwargs
    ):
        """Pass packaging_id through and enforce packaging qty multiples."""
        packaging_id = product_packaging_id or packaging_id
        if packaging_id is not None:
            kwargs["product_packaging_id"] = int(packaging_id)
            kwargs["packaging_id"] = int(packaging_id)

        set_qty = float(set_qty or 0)
        if set_qty > 0 and line_id:
            line = self.env["sale.order.line"].browse(int(line_id)).exists()
            if line.product_packaging_id and line.product_packaging_id.qty:
                step = line.product_packaging_id.qty
                set_qty = max(step, round(set_qty / step) * step)

        return super()._cart_update(
            product_id=product_id,
            line_id=line_id,
            add_qty=add_qty,
            set_qty=set_qty,
            **kwargs,
        )
