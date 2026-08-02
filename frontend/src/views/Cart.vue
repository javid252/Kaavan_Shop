<template>
  <div class="container cart-page">
    <h1>سبد خرید</h1>

    <div v-if="isEmpty" class="empty-state">
      <div class="icon">🛒</div>
      <p>سبد خرید شما خالی است.</p>
      <router-link to="/products" class="btn btn-primary">مشاهده محصولات</router-link>
    </div>

    <div v-else class="cart-layout">
      <div class="cart-items">
        <div v-if="validated && validated.has_issue" class="form-error-box">
          برخی از آیتم‌های سبد خرید شما تغییر کرده‌اند (تغییر قیمت یا کمبود موجودی). لطفاً قبل از پرداخت بررسی کنید.
        </div>

        <div v-for="line in displayLines" :key="line.key" class="cart-line card">
          <div class="cart-line__image">
            <img v-if="line.image" :src="line.image" :alt="line.name" />
            <span v-else>📦</span>
          </div>
          <div class="cart-line__info">
            <router-link :to="`/products/${line.slug || ''}`" class="cart-line__name">{{ line.name }}</router-link>
            <span v-if="line.variant_label" class="text-muted">{{ line.variant_label }}</span>
            <span v-if="line.invalid" class="field-error">{{ line.issueText }}</span>
          </div>
          <div class="qty-control">
            <button @click="updateQty(line, line.quantity - 1)">−</button>
            <span>{{ line.quantity }}</span>
            <button @click="updateQty(line, line.quantity + 1)">+</button>
          </div>
          <div class="cart-line__price">{{ formatPrice(line.price * line.quantity) }} تومان</div>
          <button class="cart-line__remove" @click="remove(line)" aria-label="حذف">🗑</button>
        </div>
      </div>

      <aside class="cart-summary card">
        <h3>خلاصه سفارش</h3>
        <div class="summary-row">
          <span>جمع کل ({{ itemCount }} کالا)</span>
          <span>{{ formatPrice(subtotal) }} تومان</span>
        </div>
        <RouteDivider margin="16px 0" />
        <div class="summary-row summary-row--total">
          <span>مبلغ قابل پرداخت</span>
          <span>{{ formatPrice(subtotal) }} تومان</span>
        </div>
        <button class="btn btn-primary btn-block" :disabled="validating" @click="goCheckout">
          ادامه فرآیند خرید
        </button>
      </aside>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapState } from "vuex";
import RouteDivider from "@/components/RouteDivider.vue";

export default {
  name: "CartView",
  components: { RouteDivider },
  computed: {
    ...mapState("cart", ["items", "validated", "validating"]),
    ...mapGetters("cart", ["itemCount", "isEmpty"]),
    displayLines() {
      return this.items.map((item) => {
        const serverLine = this.validated
          ? this.validated.items.find(
              (l) => l.product_id === item.product_id && (l.variant_id || null) === (item.variant_id || null)
            )
          : null;
        return {
          key: `${item.product_id}-${item.variant_id || 0}`,
          product_id: item.product_id,
          variant_id: item.variant_id,
          name: serverLine ? serverLine.product_name : item.name,
          slug: serverLine ? serverLine.product_slug : null,
          variant_label: serverLine ? serverLine.variant_label : item.variant_label,
          image: item.image,
          quantity: item.quantity,
          price: serverLine ? serverLine.unit_price : item.price,
          invalid: !!(serverLine && !serverLine.valid),
          issueText:
            serverLine && !serverLine.valid
              ? `فقط ${serverLine.available_stock} عدد موجود است`
              : "",
        };
      });
    },
    subtotal() {
      return this.displayLines.reduce((sum, l) => sum + l.price * l.quantity, 0);
    },
  },
  created() {
    this.$store.dispatch("cart/validateCart");
  },
  methods: {
    formatPrice(v) {
      return Number(v).toLocaleString("fa-IR");
    },
    updateQty(line, quantity) {
      if (quantity <= 0) {
        this.remove(line);
        return;
      }
      this.$store.dispatch("cart/setQuantity", {
        product_id: line.product_id,
        variant_id: line.variant_id,
        quantity,
      });
      this.$store.dispatch("cart/validateCart");
    },
    remove(line) {
      this.$store.dispatch("cart/removeItem", { product_id: line.product_id, variant_id: line.variant_id });
      this.$store.dispatch("cart/validateCart");
    },
    goCheckout() {
      this.$router.push("/checkout");
    },
  },
};
</script>

<style scoped>
.cart-page {
  padding: 36px 20px 60px;
}
.cart-page h1 {
  font-size: 1.6rem;
  margin-bottom: 26px;
}
.cart-layout {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 30px;
  align-items: start;
}
.cart-items {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.cart-line {
  display: grid;
  grid-template-columns: 70px 1fr auto auto auto;
  align-items: center;
  gap: 16px;
  padding: 14px;
}
.cart-line__image {
  width: 70px;
  height: 70px;
  border-radius: var(--radius-sm);
  background: var(--color-sand);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  font-size: 1.6rem;
}
.cart-line__image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.cart-line__info {
  display: flex;
  flex-direction: column;
  gap: 3px;
}
.cart-line__name {
  font-weight: 700;
  font-size: 0.92rem;
}
.cart-line__price {
  font-weight: 800;
  white-space: nowrap;
}
.cart-line__remove {
  background: none;
  border: none;
  font-size: 1rem;
  color: var(--color-text-muted);
}
.cart-line__remove:hover {
  color: var(--color-danger);
}
.qty-control {
  display: flex;
  align-items: center;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-sm);
  overflow: hidden;
}
.qty-control button {
  width: 28px;
  height: 28px;
  background: var(--color-sand);
  border: none;
}
.qty-control span {
  width: 32px;
  text-align: center;
  font-size: 0.88rem;
  font-weight: 700;
}
.cart-summary {
  padding: 20px;
  position: sticky;
  top: calc(var(--header-height) + 20px);
}
.cart-summary h3 {
  font-size: 1rem;
  margin-bottom: 16px;
}
.summary-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: var(--color-text-muted);
  margin-bottom: 8px;
}
.summary-row--total {
  color: var(--color-text);
  font-weight: 800;
  font-size: 1.05rem;
  margin-bottom: 18px;
}

@media (max-width: 800px) {
  .cart-layout {
    grid-template-columns: 1fr;
  }
  .cart-line {
    grid-template-columns: 56px 1fr;
    grid-template-areas: "image info" "image qty" "image price";
  }
}
</style>
