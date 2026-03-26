# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html).
{

    "name": "Website Packaging with Discount",
    "summary": """
        Product packaging selector with discounts for eCommerce""",
    "author": "Be OnlyOne",
    "maintainers": ["onlyone-odoo"],
    "website": "https://onlyone.odoo.com/",
    "license": "AGPL-3",
    "category": "Website/Website",
    "version": "18.0.9.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,

    "depends": ["website_sale", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_packaging_views.xml",
        "views/templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "oo_packaging_website/static/src/xml/packaging_selector.xml",
            "oo_packaging_website/static/src/js/packaging_selector.js",
            "oo_packaging_website/static/src/js/cart_packaging_qty.js",
            "oo_packaging_website/static/src/scss/packaging.scss",
        ],
    },
}
