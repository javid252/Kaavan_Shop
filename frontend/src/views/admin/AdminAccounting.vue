<template>
  <div class="admin-accounting">
    <h1>حسابداری</h1>

    <!-- Date range + summary -->
    <div class="card summary-card">
      <div class="date-range">
        <div class="field">
          <label>از تاریخ</label>
          <input v-model="dateFrom" type="date" @change="fetchSummary" />
        </div>
        <div class="field">
          <label>تا تاریخ</label>
          <input v-model="dateTo" type="date" @change="fetchSummary" />
        </div>
      </div>

      <AppLoader v-if="loadingSummary" />
      <div v-else class="summary-stats">
        <div class="stat stat--income">
          <span class="stat__label">کل درآمد</span>
          <span class="stat__value">{{ formatPrice(summary.total_income) }} تومان</span>
        </div>
        <div class="stat stat--expense">
          <span class="stat__label">کل هزینه</span>
          <span class="stat__value">{{ formatPrice(summary.total_expense) }} تومان</span>
        </div>
        <div class="stat stat--profit">
          <span class="stat__label">سود خالص</span>
          <span class="stat__value">{{ formatPrice(summary.net_profit) }} تومان</span>
        </div>
      </div>
    </div>

    <div class="grid-2col">
      <!-- New transaction -->
      <div class="card section-card">
        <h3>ثبت تراکنش دستی</h3>
        <div v-if="txError" class="form-error-box">{{ txError }}</div>

        <div class="two-col">
          <div class="field">
            <label>نوع</label>
            <select v-model="txForm.type">
              <option value="expense">هزینه</option>
              <option value="income">درآمد</option>
            </select>
          </div>
          <div class="field">
            <label>مبلغ (تومان)</label>
            <input v-model.number="txForm.amount" type="number" min="0" />
          </div>
        </div>

        <div class="field">
          <label>دسته</label>
          <select v-model="txForm.category">
            <option :value="null">بدون دسته</option>
            <option v-for="c in filteredCategories" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
        </div>

        <div class="field">
          <label>توضیح</label>
          <input v-model="txForm.description" type="text" placeholder="مثلاً: اجاره انبار مرداد" />
        </div>

        <div class="field">
          <label>تاریخ</label>
          <input v-model="txForm.occurred_at" type="date" />
        </div>

        <button class="btn btn-primary btn-block" :disabled="savingTx" @click="saveTransaction">
          {{ savingTx ? "در حال ثبت..." : "ثبت تراکنش" }}
        </button>
      </div>

      <!-- Categories -->
      <div class="card section-card">
        <div class="section-head">
          <h3>دسته‌های مالی</h3>
          <button class="btn btn-outline btn-sm" @click="categoryFormOpen = !categoryFormOpen">
            {{ categoryFormOpen ? "بستن" : "+ دسته جدید" }}
          </button>
        </div>

        <div v-if="categoryFormOpen" class="category-form">
          <input v-model="categoryForm.name" type="text" placeholder="نام دسته" />
          <select v-model="categoryForm.type">
            <option value="expense">هزینه</option>
            <option value="income">درآمد</option>
          </select>
          <button class="btn btn-primary btn-sm" :disabled="savingCategory" @click="saveCategory">ذخیره</button>
        </div>

        <ul class="category-list">
          <li v-for="c in categories" :key="c.id">
            <span>{{ c.name }}</span>
            <span class="badge" :class="c.type === 'income' ? 'badge-status-paid' : 'badge-status-cancelled'">
              {{ c.type === "income" ? "درآمد" : "هزینه" }}
            </span>
          </li>
          <li v-if="categories.length === 0" class="text-muted">دسته‌ای ثبت نشده.</li>
        </ul>
      </div>
    </div>

    <!-- Transactions ledger -->
    <div class="card table-card">
      <h3>تراکنش‌ها</h3>
      <AppLoader v-if="loadingTx" />
      <table v-else class="admin-table">
        <thead>
          <tr>
            <th>نوع</th>
            <th>مبلغ</th>
            <th>دسته</th>
            <th>توضیح</th>
            <th>سفارش مرتبط</th>
            <th>خودکار</th>
            <th>تاریخ</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in transactions" :key="t.id">
            <td>
              <span class="badge" :class="t.type === 'income' ? 'badge-status-paid' : 'badge-status-cancelled'">
                {{ t.type === "income" ? "درآمد" : "هزینه" }}
              </span>
            </td>
            <td>{{ formatPrice(t.amount) }}</td>
            <td>{{ t.category_name || "—" }}</td>
            <td class="text-muted">{{ t.description || "—" }}</td>
            <td class="text-muted">{{ t.related_order ? `#${t.related_order}` : "—" }}</td>
            <td>{{ t.is_automatic ? "بله" : "خیر" }}</td>
            <td class="text-muted">{{ formatDate(t.occurred_at) }}</td>
          </tr>
        </tbody>
      </table>
      <p v-if="!loadingTx && transactions.length === 0" class="text-muted empty-row">تراکنشی ثبت نشده.</p>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

function todayISO() {
  return new Date().toISOString().slice(0, 10);
}

export default {
  name: "AdminAccounting",
  components: { AppLoader },
  data() {
    return {
      dateFrom: "",
      dateTo: "",
      summary: { total_income: 0, total_expense: 0, net_profit: 0 },
      loadingSummary: true,

      categories: [],
      categoryFormOpen: false,
      savingCategory: false,
      categoryForm: { name: "", type: "expense" },

      transactions: [],
      loadingTx: true,
      txForm: { type: "expense", amount: 0, category: null, description: "", occurred_at: todayISO() },
      savingTx: false,
      txError: "",
    };
  },
  computed: {
    filteredCategories() {
      return this.categories.filter((c) => c.type === this.txForm.type);
    },
  },
  created() {
    this.fetchSummary();
    this.fetchCategories();
    this.fetchTransactions();
  },
  methods: {
    formatPrice(v) {
      return Number(v).toLocaleString("fa-IR");
    },
    formatDate(v) {
      return new Date(v).toLocaleDateString("fa-IR");
    },
    async fetchSummary() {
      this.loadingSummary = true;
      try {
        const params = {};
        if (this.dateFrom) params.date_from = this.dateFrom;
        if (this.dateTo) params.date_to = this.dateTo;
        const { data } = await api.get("/admin/accounting/summary/", { params });
        this.summary = data;
      } finally {
        this.loadingSummary = false;
      }
    },
    async fetchCategories() {
      const { data } = await api.get("/admin/accounting/categories/");
      this.categories = data.results || data;
    },
    async saveCategory() {
      this.savingCategory = true;
      try {
        const { data } = await api.post("/admin/accounting/categories/", this.categoryForm);
        this.categories.push(data);
        this.categoryForm = { name: "", type: "expense" };
        this.categoryFormOpen = false;
        this.$store.dispatch("notify", { message: "دسته مالی جدید ثبت شد." });
      } catch (e) {
        this.$store.dispatch("notify", { message: "ثبت دسته ناموفق بود.", type: "error" });
      } finally {
        this.savingCategory = false;
      }
    },
    async fetchTransactions() {
      this.loadingTx = true;
      try {
        const { data } = await api.get("/admin/accounting/transactions/", { params: { page_size: 50 } });
        this.transactions = data.results || data;
      } finally {
        this.loadingTx = false;
      }
    },
    async saveTransaction() {
      this.savingTx = true;
      this.txError = "";
      try {
        await api.post("/admin/accounting/transactions/", this.txForm);
        this.$store.dispatch("notify", { message: "تراکنش ثبت شد." });
        this.txForm = { type: "expense", amount: 0, category: null, description: "", occurred_at: todayISO() };
        this.fetchTransactions();
        this.fetchSummary();
      } catch (e) {
        this.txError = "ثبت تراکنش ناموفق بود. مقادیر را بررسی کنید.";
      } finally {
        this.savingTx = false;
      }
    },
  },
};
</script>

<style scoped>
.admin-accounting h1 {
  font-size: 1.4rem;
  margin-bottom: 20px;
}
.summary-card {
  padding: 22px;
  margin-bottom: 20px;
}
.date-range {
  display: flex;
  gap: 16px;
  margin-bottom: 18px;
}
.date-range .field input {
  padding: 8px 12px;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: inherit;
}
.summary-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 14px;
}
.stat {
  padding: 16px;
  border-radius: var(--radius-sm);
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.stat__label {
  font-size: 0.8rem;
  color: var(--color-text-muted);
}
.stat__value {
  font-size: 1.15rem;
  font-weight: 800;
}
.stat--income {
  background: #e4f0ec;
}
.stat--expense {
  background: #f8e6e2;
}
.stat--profit {
  background: #fdf6ea;
}
.grid-2col {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}
.section-card {
  padding: 22px;
}
.section-card h3 {
  font-size: 1rem;
  margin-bottom: 16px;
}
.two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}
.section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}
.category-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px dashed var(--color-border);
}
.category-form input,
.category-form select {
  padding: 8px 12px;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: inherit;
  font-size: 0.85rem;
}
.category-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.category-list li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.87rem;
  padding: 8px 0;
  border-bottom: 1px solid var(--color-border);
}
.category-list li:last-child {
  border-bottom: none;
}
.table-card {
  padding: 18px;
  overflow-x: auto;
}
.table-card h3 {
  font-size: 1rem;
  margin-bottom: 14px;
}
.admin-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.84rem;
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
  padding: 10px 12px;
  border-bottom: 1px solid var(--color-border);
}
.empty-row {
  text-align: center;
  padding: 30px;
}

@media (max-width: 900px) {
  .grid-2col {
    grid-template-columns: 1fr;
  }
}
</style>