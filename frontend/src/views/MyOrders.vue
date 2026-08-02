<template>
  <div class="container my-orders-page">
    <h1>سفارش‌های من</h1>

    <AppLoader v-if="loading" />
    <div v-else-if="orders.length === 0" class="empty-state">
      <div class="icon">📦</div>
      <p>هنوز سفارشی ثبت نکرده‌اید.</p>
      <router-link to="/products" class="btn btn-primary">شروع خرید</router-link>
    </div>

    <div v-else class="orders-list">
      <div v-for="order in orders" :key="order.id" class="order-card card">
        <div class="order-card__head">
          <div>
            <span class="text-muted">سفارش #{{ order.id }}</span>
            <h3>{{ formatDate(order.created_at) }}</h3>
          </div>
          <span class="badge" :class="statusBadgeClass(order.status)">{{ order.status_display }}</span>
        </div>

        <div v-if="order.status !== 'cancelled'" class="status-track">
          <div
            v-for="(step, idx) in steps"
            :key="step.key"
            class="status-track__step"
            :class="{ done: idx <= currentStepIndex(order.status) }"
          >
            <span class="status-track__dot" />
            <span class="status-track__label">{{ step.label }}</span>
          </div>
        </div>

        <ul class="order-items">
          <li v-for="item in order.items" :key="item.id">
            {{ item.product_name }} <span v-if="item.variant_label">({{ item.variant_label }})</span>
            <span class="text-muted">× {{ item.quantity }}</span>
          </li>
        </ul>

        <div class="order-card__foot">
          <span>مبلغ کل</span>
          <strong>{{ formatPrice(order.total_price) }} تومان</strong>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

const STEPS = [
  { key: "pending", label: "در حال بررسی" },
  { key: "paid", label: "پرداخت شده" },
  { key: "shipped", label: "ارسال شده" },
  { key: "delivered", label: "تحویل شده" },
];

export default {
  name: "MyOrdersView",
  components: { AppLoader },
  data() {
    return { orders: [], loading: true, steps: STEPS };
  },
  async created() {
    try {
      const { data } = await api.get("/orders/my/");
      this.orders = data.results || data;
    } finally {
      this.loading = false;
    }
  },
  methods: {
    formatPrice(v) {
      return Number(v).toLocaleString("fa-IR");
    },
    formatDate(v) {
      return new Date(v).toLocaleDateString("fa-IR");
    },
    currentStepIndex(status) {
      return STEPS.findIndex((s) => s.key === status);
    },
    statusBadgeClass(status) {
      return `badge-status-${status}`;
    },
  },
};
</script>

<style scoped>
.my-orders-page {
  padding: 36px 20px 60px;
}
.my-orders-page h1 {
  font-size: 1.6rem;
  margin-bottom: 26px;
}
.orders-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.order-card {
  padding: 20px 22px;
}
.order-card__head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 18px;
}
.order-card__head h3 {
  font-size: 1rem;
  margin-top: 2px;
}
.status-track {
  display: flex;
  margin-bottom: 18px;
}
.status-track__step {
  flex: 1;
  text-align: center;
  position: relative;
}
.status-track__step::before {
  content: "";
  position: absolute;
  top: 5px;
  right: 50%;
  width: 100%;
  height: 2px;
  background: var(--color-border);
  z-index: 0;
}
.status-track__step:first-child::before {
  display: none;
}
.status-track__step.done::before {
  background: var(--color-accent);
}
.status-track__dot {
  display: block;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--color-border);
  margin: 0 auto 6px;
  position: relative;
  z-index: 1;
}
.status-track__step.done .status-track__dot {
  background: var(--color-accent);
}
.status-track__label {
  font-size: 0.72rem;
  color: var(--color-text-muted);
}
.status-track__step.done .status-track__label {
  color: var(--color-primary);
  font-weight: 700;
}
.order-items {
  list-style: none;
  padding: 0;
  margin: 0 0 16px;
  font-size: 0.87rem;
  color: var(--color-text-muted);
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.order-card__foot {
  display: flex;
  justify-content: space-between;
  border-top: 1px dashed var(--color-border);
  padding-top: 14px;
  font-size: 0.92rem;
}
</style>
