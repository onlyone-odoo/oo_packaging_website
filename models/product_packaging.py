# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    packaging_discount = fields.Float(
        string="Website Discount (%)",
        digits=(5, 2),
        default=0.0,
        help="Discount percentage applied when this packaging is selected on the website (e.g. 5 for 5%).",
    )
    website_published = fields.Boolean(
        string="Published on Website",
        default=False,
        help="If checked, this packaging option is shown in the eCommerce product page.",
    )
    website_ids = fields.Many2many(
        comodel_name="website",
        relation="product_packaging_website_rel",
        column1="packaging_id",
        column2="website_id",
        string="Websites",
        help="Leave empty to show on all websites of the company. Otherwise, restrict to selected websites.",
    )

    _sql_constraints = [
        (
            "packaging_discount_range",
            "CHECK(packaging_discount >= 0 AND packaging_discount <= 100)",
            "Website discount must be between 0 and 100%.",
        ),
    ]

    @api.constrains("packaging_discount")
    def _check_packaging_discount(self):
        for packaging in self:
            if not 0 <= packaging.packaging_discount <= 100:
                raise ValidationError(
                    _("Website discount must be between 0 and 100%%.")
                )

    @api.model
    def _get_website_packagings(self, product, website=None):
        """
        Return packagings available for the given product on the given website.

        Filters by: sales=True, website_published=True, company compatible,
        and website_ids empty or containing the given website.

        :param product: product.product record
        :param website: website record or None (then no website filter)
        :return: product.packaging recordset
        """
        if not product:
            return self.browse()
        packagings = product.packaging_ids.filtered(
            lambda p: p.sales and p.website_published
        )
        if not packagings:
            return self.browse()
        # Company: packaging must be compatible with product and (if website) website company
        company = website.company_id if website else product.company_id
        if company:
            packagings = packagings.filtered(
                lambda p: (p.company_id == company or not p.company_id)
                and (not p.product_id.company_id or p.product_id.company_id == company)
            )
        if website and packagings:
            # Restrict to website_ids empty or containing this website
            packagings = packagings.filtered(
                lambda p: not p.website_ids or website in p.website_ids
            )
        return packagings.sorted(key=lambda p: (p.sequence, p.id))
