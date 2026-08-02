<template>
  <div class="vendor-dashboard">
    <h1>داشبورد فروشگاه</h1>

    <AppLoader v-if="loading" />
    <template v-else>
      <div class="stat-grid">
        <div class="stat-card card">
          <span class="stat-card__label">تعداد محصولات من</span>
          <span class="stat-card__value">{{ productCount }}</span>
        </div>
        <div class="stat-card card">
          <span class="stat-card__label">محصولات فعال</span>
          <span class="stat-card__value">{{ activeCount }}</span>
        </div>
        <div class="stat-card card stat-card--accent">
          <span class="stat-card__label">وضعیت فروشگاه</span>
          <span class="stat-card__value status-value">{{ statusLabel }}</span>
        </div>
      </div>

      <div class="card quick-actions">
        <h3>شروع سریع</h3>
        <div class="quick-actions__buttons">
          <router-link to="/vendor/products/new" class="btn btn-primary btn-sm">+ افزودن محصول جدید</router-link>
          <router-link to="/vendor/products" class="btn btn-outline btn-sm">مدیریت محصولات</router-link>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

const LABELS = { pending: "در انتظار تایید", approved: "تاییدشده", rejected: "رد شده", suspended: "معلق" };

export default {
  name: "VendorDashboard",
  components: { AppLoader },
  data() {
    return { loading: true, productCount: 0, activeCount: 0 };
  },
  computed: {
    ...mapGetters("vendor", ["vendorStatus"]),
    statusLabel() {
      return LABELS[this.vendorStatus] || this.vendorStatus;
    },
  },
  async created() {
    try {
      const { data } = await api.get("/products/", { params: { mine: 1, page_size: 1 } });
      this.productCount = data.count ?? 0;
      const { data: activeData } = await api.get("/products/", { params: { mine: 1, page_size: 1, is_active: true } });
      this.activeCount = activeData.count ?? 0;
    } finally {
      this.loading = false;
    }
  },
};
</script>

<style scoped>
.vendor-dashboard h1 {
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
.status-value {
  font-size: 1.1rem;
}
.stat-card--accent {
  border-color: var(--color-accent);
  background: #fdf6ea;
}
.quick-actions {
  padding: 20px;
}
.quick-actions h3 {
  font-size: 0.95rem;
  margin-bottom: 14px;
}
.quick-actions__buttons {
  display: flex;
  gap: 12px;
}
</style>