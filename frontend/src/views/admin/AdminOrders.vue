<template>
  <div class="admin-orders">
    <h1>سفارش‌ها</h1>

    <div class="card table-card">
      <AppLoader v-if="loading" />
      <table v-else class="admin-table">
        <thead>
          <tr>
            <th>شماره</th>
            <th>مشتری</th>
            <th>گیرنده</th>
            <th>تعداد اقلام</th>
            <th>مبلغ کل</th>
            <th>تاریخ</th>
            <th>وضعیت</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in orders" :key="order.id">
            <td>#{{ order.id }}</td>
            <td>{{ order.user_display }}</td>
            <td>{{ order.full_name }}<br /><span class="text-muted">{{ order.phone_number }}</span></td>
            <td>{{ order.items.length }}</td>
            <td>{{ formatPrice(order.total_price) }}</td>
            <td>{{ formatDate(order.created_at) }}</td>
            <td>
              <select
                class="status-select"
                :value="order.status"
                @change="updateStatus(order, $event.target.value)"
              >
                <option v-for="s in statuses" :key="s.value" :value="s.value">{{ s.label }}</option>
              </select>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-if="!loading && orders.length === 0" class="text-muted empty-row">سفارشی ثبت نشده است.</p>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

const STATUSES = [
  { value: "pending", label: "در حال بررسی" },
  { value: "paid", label: "پرداخت شده" },
  { value: "shipped", label: "ارسال شده" },
  { value: "delivered", label: "تحویل شده" },
  { value: "cancelled", label: "لغو شده" },
];

export default {
  name: "AdminOrders",
  components: { AppLoader },
  data() {
    return { orders: [], loading: true, statuses: STATUSES };
  },
  created() {
    this.fetchOrders();
  },
  methods: {
    formatPrice(v) {
      return Number(v).toLocaleString("fa-IR");
    },
    formatDate(v) {
      return new Date(v).toLocaleDateString("fa-IR");
    },
    async fetchOrders() {
      this.loading = true;
      try {
        const { data } = await api.get("/admin/orders/", { params: { page_size: 100 } });
        this.orders = data.results || data;
      } finally {
        this.loading = false;
      }
    },
    async updateStatus(order, status) {
      try {
        await api.patch(`/admin/orders/${order.id}/`, { status });
        order.status = status;
        this.$store.dispatch("notify", { message: `وضعیت سفارش #${order.id} به‌روزرسانی شد.` });
      } catch (e) {
        this.$store.dispatch("notify", { message: "به‌روزرسانی وضعیت ناموفق بود.", type: "error" });
      }
    },
  },
};
</script>

<style scoped>
.admin-orders h1 {
  font-size: 1.4rem;
  margin-bottom: 20px;
}
.table-card {
  padding: 18px;
  overflow-x: auto;
}
.admin-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
  min-width: 720px;
}
.admin-table th {
  text-align: right;
  color: var(--color-text-muted);
  font-weight: 700;
  padding: 10px 12px;
  border-bottom: 1.5px solid var(--color-border);
  font-size: 0.78rem;
}
.admin-table td {
  padding: 12px;
  border-bottom: 1px solid var(--color-border);
  vertical-align: top;
}
.status-select {
  padding: 6px 10px;
  border-radius: var(--radius-sm);
  border: 1.5px solid var(--color-border);
  font-family: inherit;
  font-size: 0.82rem;
}
.empty-row {
  text-align: center;
  padding: 30px;
}
</style>
