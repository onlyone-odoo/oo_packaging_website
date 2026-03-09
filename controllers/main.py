# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

import json

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSalePackaging(WebsiteSale):
    """Pass packaging_id from request to cart update for website packaging selector."""

    def _prepare_product_values(self, product, category, search, **kwargs):
        """Add website packagings per variant for the product page."""
        values = super()._prepare_product_values(
            product, category, search, **kwargs
        )
        Packaging = request.env["product.packaging"].with_context(
            bin_size=False
        )
        website = request.website
        website_packagings_by_variant = {}
        for variant in product.product_variant_ids:
            packagings = Packaging._get_website_packagings(variant, website)
            website_packagings_by_variant[variant.id] = [
                {
                    "id": p.id,
                    "name": p.name,
                    "qty": p.qty,
                    "uom_name": p.product_uom_id.name,
                    "discount": p.packaging_discount or 0.0,
                }
                for p in packagings
            ]
        values["website_packagings_by_variant"] = website_packagings_by_variant
        values["website_packagings_by_variant_json"] = json.dumps(
            {"packagingsByVariant": website_packagings_by_variant}
        )
        values["has_website_packagings"] = any(website_packagings_by_variant.values())
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
        if packaging_id is not None:
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
        if packaging_id is not None:
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
