<template>
  <div class="admin-vendors">
    <h1>فروشندگان</h1>

    <div class="card table-card">
      <AppLoader v-if="loading" />
      <table v-else class="admin-table">
        <thead>
          <tr>
            <th>فروشگاه</th>
            <th>کاربر</th>
            <th>وضعیت</th>
            <th>کارمزد اختصاصی</th>
            <th>تاریخ درخواست</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="v in vendors" :key="v.id">
            <td class="vendor-name-cell">{{ v.store_name }}</td>
            <td>{{ v.username }}<br /><span class="text-muted">{{ v.email }}</span></td>
            <td>
              <span class="badge" :class="statusClass(v.status)">{{ statusLabel(v.status) }}</span>
            </td>
            <td>
              <input
                class="commission-input"
                type="number"
                min="0"
                max="100"
                step="0.5"
                :value="v.commission_percent"
                placeholder="پیش‌فرض"
                @change="updateCommission(v, $event.target.value)"
              />
            </td>
            <td>{{ formatDate(v.created_at) }}</td>
            <td class="actions-cell">
              <button v-if="v.status !== 'approved'" class="btn btn-primary btn-sm" @click="setStatus(v, 'approved')">تایید</button>
              <button v-if="v.status !== 'rejected'" class="btn btn-danger btn-sm" @click="setStatus(v, 'rejected')">رد</button>
              <button v-if="v.status === 'approved'" class="btn btn-outline btn-sm" @click="setStatus(v, 'suspended')">تعلیق</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-if="!loading && vendors.length === 0" class="text-muted empty-row">هنوز هیچ فروشنده‌ای ثبت‌نام نکرده است.</p>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

const LABELS = {
  pending: "در انتظار تایید",
  approved: "تاییدشده",
  rejected: "رد شده",
  suspended: "معلق",
};

export default {
  name: "AdminVendors",
  components: { AppLoader },
  data() {
    return { vendors: [], loading: true };
  },
  created() {
    this.fetchVendors();
  },
  methods: {
    formatDate(v) {
      return new Date(v).toLocaleDateString("fa-IR");
    },
    statusLabel(status) {
      return LABELS[status] || status;
    },
    statusClass(status) {
      const map = {
        pending: "badge-status-pending",
        approved: "badge-status-paid",
        rejected: "badge-status-cancelled",
        suspended: "badge-status-cancelled",
      };
      return map[status] || "badge-muted";
    },
    async fetchVendors() {
      this.loading = true;
      try {
        const { data } = await api.get("/admin/vendors/", { params: { page_size: 100 } });
        this.vendors = data.results || data;
      } finally {
        this.loading = false;
      }
    },
    async setStatus(vendor, status) {
      try {
        const { data } = await api.patch(`/admin/vendors/${vendor.id}/`, { status });
        Object.assign(vendor, data);
        this.$store.dispatch("notify", { message: `وضعیت «${vendor.store_name}» به‌روزرسانی شد.` });
      } catch (e) {
        this.$store.dispatch("notify", { message: "به‌روزرسانی ناموفق بود.", type: "error" });
      }
    },
    async updateCommission(vendor, value) {
      const commission_percent = value === "" ? null : Number(value);
      try {
        const { data } = await api.patch(`/admin/vendors/${vendor.id}/`, { commission_percent });
        Object.assign(vendor, data);
      } catch (e) {
        this.$store.dispatch("notify", { message: "تنظیم کارمزد ناموفق بود.", type: "error" });
      }
    },
  },
};
</script>

<style scoped>
.admin-vendors h1 {
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
  min-width: 760px;
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
  vertical-align: middle;
}
.vendor-name-cell {
  font-weight: 700;
}
.commission-input {
  width: 90px;
  padding: 6px 8px;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: inherit;
  font-size: 0.82rem;
}
.actions-cell {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}
.empty-row {
  text-align: center;
  padding: 30px;
}
</style>