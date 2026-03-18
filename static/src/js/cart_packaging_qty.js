/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

const WebsiteSaleWidget = publicWidget.registry.WebsiteSale;

if (WebsiteSaleWidget) {
    WebsiteSaleWidget.include({
        /**
         * Override +/- buttons: when the cart input carries
         * data-packaging-qty, step by that amount instead of ±1.
         */
        _onClickAddCartJSON(ev) {
            const $link = $(ev.currentTarget);
            const $input = $link.closest(".input-group").find("input");
            const step = parseFloat($input.data("packaging-qty") || 0);

            if (step > 0) {
                ev.preventDefault();
                const current = parseFloat($input.val()) || 0;
                const direction = $link.find(".fa-minus").length ? -1 : 1;
                const next = current + direction * step;

                if (next >= step) {
                    $input.val(next).trigger("change");
                } else if (direction === -1) {
                    $input.val(0).trigger("change");
                }
                return;
            }

            return this._super.apply(this, arguments);
        },

        /**
         * Override cart quantity change: snap manually typed values to the
         * nearest valid packaging multiple before the RPC fires.
         */
        _onChangeCartQuantity(ev) {
            const $input = $(ev.currentTarget);
            const step = parseFloat($input.data("packaging-qty") || 0);

            if (step > 0 && !$input.data("update_change")) {
                let value = parseFloat($input.val()) || 0;
                if (value > 0) {
                    const snapped = Math.max(
                        step,
                        Math.round(value / step) * step
                    );
                    if (snapped !== value) {
                        $input.val(snapped);
                    }
                }
            }

            return this._super.apply(this, arguments);
        },
    });
}
