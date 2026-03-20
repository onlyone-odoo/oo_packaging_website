# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html).

import json

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSalePackaging(WebsiteSale):
    """Pass packaging_id from request to cart update for website packaging selector."""

    def _prepare_product_values(self, product, category, search, **kwargs):
        """Add website packagings per variant for the product page.

        Only variants that actually have published packagings will show the selector.
        This fixes the bug where packagings from one variant appeared on others.
        """
        values = super()._prepare_product_values(
            product, category, search, **kwargs
        )
        Packaging = request.env["product.packaging"].with_context(
            bin_size=False
        )
        website = request.website
        website_packagings_by_variant = {}
        has_any_packaging = False

        for variant in product.product_variant_ids:
            packagings = Packaging._get_website_packagings(variant, website)
            data = [
                {
                    "id": p.id,
                    "name": p.name,
                    "qty": p.qty,
                    "uom_name": p.product_uom_id.name,
                    "discount": p.packaging_discount or 0.0,
                }
                for p in packagings
            ]
            website_packagings_by_variant[variant.id] = data
            if data:
                has_any_packaging = True

        force_packaging = bool(product.website_force_packaging)
        values["website_packagings_by_variant"] = website_packagings_by_variant
        values["website_packagings_by_variant_json"] = json.dumps(
            {
                "packagingsByVariant": website_packagings_by_variant,
                "forcePackaging": force_packaging,
            }
        )
        values["has_website_packagings"] = has_any_packaging
        return values

    @http.route()
    def cart_update(
        self,
        product_id,
        add_qty=1,
        set_qty=0,
        product_custom_attribute_values=None,
        no_variant_attribute_value_ids=None,
        packaging_id=None,
        **kwargs
    ):
        """Validate that the packaging belongs to the selected product variant."""
        if packaging_id is not None:
            packaging = request.env["product.packaging"].browse(int(packaging_id)).exists()
            if packaging and packaging.product_id.id != int(product_id):
                # Invalid packaging for this variant - ignore it
                packaging_id = None
            else:
                kwargs["packaging_id"] = int(packaging_id)
                kwargs["product_packaging_id"] = int(packaging_id)
        return super().cart_update(
            product_id=product_id,
            add_qty=add_qty,
            set_qty=set_qty,
            product_custom_attribute_values=product_custom_attribute_values,
            no_variant_attribute_value_ids=no_variant_attribute_value_ids,
            **kwargs,
        )

    @http.route()
    def cart_update_json(
        self,
        product_id,
        line_id=None,
        add_qty=None,
        set_qty=None,
        display=True,
        packaging_id=None,
        **kwargs
    ):
        """Validate that the packaging belongs to the selected product variant."""
        if packaging_id is not None:
            packaging = request.env["product.packaging"].browse(int(packaging_id)).exists()
            if packaging and packaging.product_id.id != int(product_id):
                packaging_id = None  # Invalid for this variant
            else:
                kwargs["packaging_id"] = int(packaging_id)
                kwargs["product_packaging_id"] = int(packaging_id)
        return super().cart_update_json(
            product_id=product_id,
            line_id=line_id,
            add_qty=add_qty,
            set_qty=set_qty,
            display=display,
            **kwargs,
        )
