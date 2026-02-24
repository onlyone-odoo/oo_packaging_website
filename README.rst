===============================
Website Packaging with Discount
===============================

.. |badge1| image:: https://img.shields.io/badge/maturity-Stable-brightgreen
    :target: https://odoo-community.org/page/development-status
    :alt: Stable
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

.. |badge3| image:: https://onlyone.odoo.com/web/image/website/1/logo/OnlyOne%20Soft?unique=dccda5b
    :target: https://onlyone.odoo.com/
    :alt: Be OnlyOne

|badge1| |badge2| |badge3| 

This module extends the functionality of Odoo's eCommerce to support product packagings directly on the website and to allow you to configure specific discounts for each packaging option.

**Table of contents**

.. contents::
   :local:

Installation
============

To install this module, you need to:

1. Clone or download the repository into your Odoo addons path.
2. Update your app list in Odoo.
3. Search for "Website Packaging with Discount" y click Install.

Configuration
=============

To configure this module, you need to:

1. Go to **Inventory > Configuration > Settings** and ensure "Product Packagings" is enabled.
2. Go to **Sales > Configuration > Settings** and ensure "Discounts" is enabled (so order line discounts are visible).
3. Go to any product form, under the **Inventory** tab, look for the **Packaging** section.
4. For each packaging, you can now set the **Website Discount (%)**, mark it as **Published on Website**, and optionally restrict it to specific websites.

Usage
=====

1. Go to the eCommerce product page for a product that has web-published packagings.
2. You will see a new "Packaging" selector dropdown below the product variants.
3. Select a packaging option (e.g., "BULTO (48 Unidades) — 5% discount").
4. The product quantity will automatically update to match the packaging size.
5. A "Save X%" badge will appear if the packaging has an associated discount.
6. Click "Add to Cart". The cart will display the selected packaging name and the discount badge next to the price.

Known issues / Roadmap
======================

* The discount is applied to the sale order line and replaces any manual discount. If the quantity is manually changed in the cart and no longer matches the packaging multiple, the packaging and its discount will be automatically removed by standard Odoo logic.
* Future roadmap: Allow stacking manual discounts with packaging discounts if needed.

Bug Tracker
===========

* For any issues or feature requests, please contact us through our website.

Credits
=======

Authors
~~~~~~~

* Be OnlyOne

Contributors
~~~~~~~~~~~~

* `Be OnlyOne <https://onlyone.odoo.com/>`_
  
  * Matías Bressanello

Maintainers
~~~~~~~~~~~

This module is maintained by Be OnlyOne.
