<template>
  <div class="admin-dashboard">
    <h1>داشبورد</h1>

    <AppLoader v-if="loading" />
    <template v-else-if="stats">
      <div class="stat-grid">
        <div class="stat-card card">
          <span class="stat-card__label">تعداد محصولات</span>
          <span class="stat-card__value">{{ stats.total_products }}</span>
        </div>
        <div class="stat-card card">
          <span class="stat-card__label">کل سفارش‌ها</span>
          <span class="stat-card__value">{{ stats.total_orders }}</span>
        </div>
        <div class="stat-card card">
          <span class="stat-card__label">سفارش‌های در انتظار</span>
          <span class="stat-card__value">{{ stats.pending_orders }}</span>
        </div>
        <div class="stat-card card">
          <span class="stat-card__label">تعداد کاربران</span>
          <span class="stat-card__value">{{ stats.total_users }}</span>
        </div>
        <div class="stat-card card stat-card--accent">
          <span class="stat-card__label">درآمد کل</span>
          <span class="stat-card__value">{{ formatPrice(stats.total_revenue) }} <small>تومان</small></span>
        </div>
        <div class="stat-card card">
          <span class="stat-card__label">سفارش‌های امروز</span>
          <span class="stat-card__value">{{ stats.orders_today }}</span>
        </div>
      </div>

      <div v-if="stats.low_stock_products.length" class="card low-stock">
        <h3>⚠️ موجودی رو به اتمام</h3>
        <ul>
          <li v-for="p in stats.low_stock_products" :key="p.id">
            {{ p.name }} — <strong>{{ p.stock }}</strong> عدد باقی‌مانده
          </li>
        </ul>
      </div>
    </template>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

export default {
  name: "AdminDashboard",
  components: { AppLoader },
  data() {
    return { stats: null, loading: true };
  },
  async created() {
    try {
      const { data } = await api.get("/admin/stats/");
      this.stats = data;
    } finally {
      this.loading = false;
    }
  },
  methods: {
    formatPrice(v) {
      return Number(v).toLocaleString("fa-IR");
    },
  },
};
</script>

<style scoped>
.admin-dashboard h1 {
  font-size: 1.4rem;
  margin-bottom: 22px;
}
.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 16px;
  margin-bottom: 26px;
}
.stat-card {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.stat-card__label {
  font-size: 0.8rem;
  color: var(--color-text-muted);
}
.stat-card__value {
  font-size: 1.5rem;
  font-weight: 800;
}
.stat-card--accent {
  border-color: var(--color-accent);
  background: #fdf6ea;
}
.low-stock {
  padding: 20px;
}
.low-stock h3 {
  font-size: 0.95rem;
  margin-bottom: 12px;
}
.low-stock ul {
  margin: 0;
  padding-inline-start: 18px;
  font-size: 0.87rem;
  color: var(--color-text-muted);
  display: flex;
  flex-direction: column;
  gap: 6px;
}
</style>
