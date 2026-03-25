/** @odoo-module **/

import {
    Component,
    useState,
    onMounted,
    onWillUnmount,
    useRef,
} from "@odoo/owl";
import { registry } from "@web/core/registry";

export class PackagingSelector extends Component {
    static template = "oo_packaging_website.PackagingSelectorTemplate";
    static props = {
        packagingsByVariant: { type: Object, optional: true },
        forcePackagingByVariant: { type: Object, optional: true },
        /** @deprecated Legacy single flag; use forcePackagingByVariant when possible. */
        forcePackaging: { type: Boolean, optional: true },
        initialVariantId: { type: Number, optional: true },
    };

    setup() {
        this.rootRef = useRef("root");
        const initialVid =
            this.props.initialVariantId != null &&
            !Number.isNaN(Number(this.props.initialVariantId))
                ? Number(this.props.initialVariantId)
                : null;
        this.state = useState({
            currentProductId: initialVid,
            selectedPackagingId: "",
            currentDiscount: 0,
        });

        this.form = null;
        this.productIdInput = null;
        this.quantityInput = null;
        this.minusBtn = null;
        this.plusBtn = null;
        this._boundHandlers = [];

        onMounted(() => {
            const el = this.rootRef.el;
            if (el) {
                this.form = el.closest("form");
            }
            if (!this.form) return;

            this.productIdInput = this.form.querySelector("input[name='product_id']");
            this.quantityInput =
                this.form.querySelector("input[name='add_qty']") ||
                this.form.querySelector("input[name='set_qty']");

            const qtyDiv = this.form.querySelector(".css_quantity");
            if (qtyDiv) {
                const btns = qtyDiv.querySelectorAll(".js_add_cart_json");
                if (btns.length >= 2) {
                    this.minusBtn = btns[0];
                    this.plusBtn = btns[1];
                }
            }

            if (this.productIdInput) {
                const fromForm = parseInt(this.productIdInput.value, 10);
                if (!Number.isNaN(fromForm)) {
                    this.state.currentProductId = fromForm;
                }
                this._addListener(this.productIdInput, "change", () => {
                    this.state.currentProductId = parseInt(
                        this.productIdInput.value,
                        10
                    );
                    this._onVariantChanged();
                });
            }

            if (this.minusBtn) {
                this._addListener(
                    this.minusBtn,
                    "click",
                    (e) => this._onStepClick(e, -1),
                    true
                );
            }
            if (this.plusBtn) {
                this._addListener(
                    this.plusBtn,
                    "click",
                    (e) => this._onStepClick(e, 1),
                    true
                );
            }

            if (this.quantityInput) {
                this._addListener(this.quantityInput, "blur", () =>
                    this._snapToMultiple()
                );
            }

            this._onVariantChanged();
        });

        onWillUnmount(() => {
            for (const { el, event, handler, capture } of this._boundHandlers) {
                el.removeEventListener(event, handler, capture);
            }
            this._boundHandlers = [];
        });
    }

    _addListener(el, event, handler, capture = false) {
        el.addEventListener(event, handler, capture);
        this._boundHandlers.push({ el, event, handler, capture });
    }

    get forcePackagingForCurrentVariant() {
        const vid = this.state.currentProductId;
        const byVar = this.props.forcePackagingByVariant;
        if (byVar && vid != null) {
            const flag = byVar[vid];
            if (flag !== undefined) {
                return Boolean(flag);
            }
        }
        return Boolean(this.props.forcePackaging);
    }

    get showPackagingUi() {
        return this.availablePackagings.length > 0;
    }

    get availablePackagings() {
        if (!this.state.currentProductId || !this.props.packagingsByVariant) {
            return [];
        }
        return (
            this.props.packagingsByVariant[this.state.currentProductId] || []
        );
    }

    get selectedPackaging() {
        if (!this.state.selectedPackagingId) return null;
        return (
            this.availablePackagings.find(
                (p) => p.id === parseInt(this.state.selectedPackagingId, 10)
            ) || null
        );
    }

    _onVariantChanged() {
        if (!this.availablePackagings.length) {
            this._applyPackaging(null);
            return;
        }
        if (this.forcePackagingForCurrentVariant) {
            this._applyPackaging(this.availablePackagings[0]);
            return;
        }
        const selectedId = parseInt(this.state.selectedPackagingId, 10);
        if (
            selectedId &&
            !this.availablePackagings.find((p) => p.id === selectedId)
        ) {
            this._applyPackaging(null);
        }
    }

    onSelectChange(ev) {
        const val = ev.target.value;
        const pkg = val
            ? this.availablePackagings.find((p) => p.id === parseInt(val, 10))
            : null;
        this._applyPackaging(pkg);
    }

    _applyPackaging(pkg) {
        if (pkg) {
            this.state.selectedPackagingId = String(pkg.id);
            this.state.currentDiscount = pkg.discount || 0;
            if (this.quantityInput) {
                this.quantityInput.value = pkg.qty;
                this.quantityInput.dispatchEvent(
                    new Event("change", { bubbles: true })
                );
            }
        } else {
            this.state.selectedPackagingId = "";
            this.state.currentDiscount = 0;
            if (this.quantityInput && !this.forcePackagingForCurrentVariant) {
                this.quantityInput.value = 1;
                this.quantityInput.dispatchEvent(
                    new Event("change", { bubbles: true })
                );
            }
        }
    }

    /**
     * Intercept +/- clicks: when a packaging is active, step by packaging qty
     * instead of the default ±1 behaviour.
     */
    _onStepClick(e, direction) {
        const pkg = this.selectedPackaging;
        if (!pkg || !this.quantityInput) return;

        e.preventDefault();
        e.stopPropagation();

        const step = pkg.qty;
        const current = parseFloat(this.quantityInput.value) || step;
        const next = current + direction * step;

        if (next >= step) {
            this.quantityInput.value = next;
            this.quantityInput.dispatchEvent(
                new Event("change", { bubbles: true })
            );
        }
    }

    /**
     * On manual input blur, snap the value to the nearest valid packaging
     * multiple (minimum 1 pack).
     */
    _snapToMultiple() {
        const pkg = this.selectedPackaging;
        if (!pkg || !this.quantityInput) return;

        const step = pkg.qty;
        const current = parseFloat(this.quantityInput.value) || step;
        const snapped = Math.max(step, Math.round(current / step) * step);

        if (snapped !== current) {
            this.quantityInput.value = snapped;
            this.quantityInput.dispatchEvent(
                new Event("change", { bubbles: true })
            );
        }
    }
}

registry
    .category("public_components")
    .add("oo_packaging_website.PackagingSelector", PackagingSelector);
