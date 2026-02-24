/** @odoo-module **/

import { Component, useState, onMounted, onWillUnmount, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class PackagingSelector extends Component {
    static template = "oo_packaging_website.PackagingSelectorTemplate";
    static props = {
        packagingsByVariant: { type: Object, optional: true },
    };

    setup() {
        this.state = useState({
            currentProductId: null,
            selectedPackagingId: "",
            currentDiscount: 0,
        });

        this.form = null;
        this.productIdInput = null;
        this.quantityInput = null;

        onMounted(() => {
            // Find parent form
            const wrapper = document.getElementById("oo_packaging_selector_wrapper");
            if (wrapper) {
                this.form = wrapper.closest("form");
            }
            if (this.form) {
                this.productIdInput = this.form.querySelector("input[name='product_id']");
                this.quantityInput = this.form.querySelector("input[name='add_qty']") || this.form.querySelector("input[name='set_qty']");
                
                if (this.productIdInput) {
                    // Initial product ID
                    this.state.currentProductId = parseInt(this.productIdInput.value, 10);
                    
                    // Listen for product variant changes
                    this.onChangeVariant = () => {
                        this.state.currentProductId = parseInt(this.productIdInput.value, 10);
                        // Reset packaging if not available for new variant
                        const available = this.availablePackagings;
                        if (!available.find(p => p.id === parseInt(this.state.selectedPackagingId, 10))) {
                            this.state.selectedPackagingId = "";
                            this.state.currentDiscount = 0;
                        }
                    };
                    this.productIdInput.addEventListener("change", this.onChangeVariant);
                }
            }
        });

        onWillUnmount(() => {
            if (this.productIdInput && this.onChangeVariant) {
                this.productIdInput.removeEventListener("change", this.onChangeVariant);
            }
        });
    }

    get availablePackagings() {
        if (!this.state.currentProductId || !this.props.packagingsByVariant) {
            return [];
        }
        return this.props.packagingsByVariant[this.state.currentProductId] || [];
    }

    onSelectChange(ev) {
        const val = ev.target.value;
        this.state.selectedPackagingId = val;
        
        if (val) {
            const pkg = this.availablePackagings.find(p => p.id === parseInt(val, 10));
            if (pkg) {
                this.state.currentDiscount = pkg.discount;
                if (this.quantityInput) {
                    this.quantityInput.value = pkg.qty;
                    // Trigger change event to notify other scripts
                    this.quantityInput.dispatchEvent(new Event("change", { bubbles: true }));
                }
            }
        } else {
            this.state.currentDiscount = 0;
            if (this.quantityInput) {
                this.quantityInput.value = 1;
                this.quantityInput.dispatchEvent(new Event("change", { bubbles: true }));
            }
        }
    }
}

registry.category("public_components").add("oo_packaging_website.PackagingSelector", PackagingSelector);
