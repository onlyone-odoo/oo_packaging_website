/** @odoo-module **/

/**
 * Modern cart packaging quantity handler (no legacy widgets).
 * Uses event delegation on the cart container for better compatibility with Odoo 18 OWL.
 * Enforces packaging quantity steps for +/- buttons and snaps manual inputs.
 */
export function setupCartPackagingQty() {
    const container = document.querySelector(".oe_cart") || document;

    let handlersAttached = false;

    const clickHandler = (ev) => {
        const link = ev.target.closest(".js_add_cart_json");
        if (!link) return;

        const input = link.closest(".input-group")?.querySelector("input.js_quantity");
        if (!input) return;

        const step = parseFloat(input.dataset.packagingQty || 0);
        if (step <= 0) return;

        ev.preventDefault();
        ev.stopImmediatePropagation();

        const current = parseFloat(input.value) || 0;
        const isMinus = link.querySelector(".fa-minus") !== null;
        const direction = isMinus ? -1 : 1;
        let next = current + (direction * step);

        if (next < step) {
            next = isMinus ? 0 : step;
        }

        input.value = Math.max(0, next);
        input.dispatchEvent(new Event("change", { bubbles: true }));
    };

    const changeHandler = (ev) => {
        const input = ev.target;
        if (!input.classList.contains("js_quantity")) return;

        const step = parseFloat(input.dataset.packagingQty || 0);
        if (step <= 0) return;

        let value = parseFloat(input.value) || 0;
        if (value > 0) {
            const snapped = Math.max(step, Math.round(value / step) * step);
            if (snapped !== value) {
                input.value = snapped;
                // Prevent infinite loop
                const originalHandler = input.onchange;
                input.onchange = null;
                input.dispatchEvent(new Event("change", { bubbles: true }));
                input.onchange = originalHandler;
            }
        }
    };

    // Attach listeners once
    if (!handlersAttached) {
        container.addEventListener("click", clickHandler, true);
        container.addEventListener("change", changeHandler, true);
        handlersAttached = true;
        console.debug("Cart packaging qty handler initialized (modern)");
    }
}

// Auto-initialize when the module loads (works on cart page)
setupCartPackagingQty();
