<template>
  <div class="admin-inventory">
    <h1>انبارداری</h1>

    <div class="grid-2col">
      <!-- Adjustment form -->
      <div class="card section-card">
        <h3>ثبت اصلاح موجودی</h3>
        <div v-if="adjustError" class="form-error-box">{{ adjustError }}</div>

        <div class="field">
          <label>محصول</label>
          <input v-model="productSearch" type="text" placeholder="نام محصول را جستجو کنید..." @input="debouncedSearch" />
          <div v-if="productResults.length" class="product-results">
            <button
              v-for="p in productResults"
              :key="p.id"
              type="button"
              class="product-result-item"
              @click="selectProduct(p)"
            >
              {{ p.name }} <span class="text-muted">— موجودی فعلی: {{ p.stock != null ? p.stock : "—" }}</span>
            </button>
          </div>
          <p v-if="selectedProduct" class="selected-product">
            انتخاب‌شده: <strong>{{ selectedProduct.name }}</strong>
          </p>
        </div>

        <div class="two-col">
          <div class="field">
            <label>نوع تغییر</label>
            <select v-model="adjustForm.movement_type">
              <option value="restock">ورود کالا / خرید</option>
              <option value="adjustment_in">اصلاح دستی (افزایش)</option>
              <option value="adjustment_out">اصلاح دستی (کاهش)</option>
              <option value="return">مرجوعی</option>
            </select>
          </div>
          <div class="field">
            <label>تعداد</label>
            <input v-model.number="adjustForm.quantity" type="number" min="1" />
          </div>
        </div>

        <div class="field">
          <label>انبار (اختیاری)</label>
          <select v-model="adjustForm.warehouse">
            <option :value="null">انبار پیش‌فرض</option>
            <option v-for="w in warehouses" :key="w.id" :value="w.id">{{ w.name }}</option>
          </select>
        </div>

        <div class="field">
          <label>توضیح</label>
          <textarea v-model="adjustForm.note" rows="2" placeholder="مثلاً: خرید از تولیدکننده"></textarea>
        </div>

        <button class="btn btn-primary btn-block" :disabled="adjusting || !selectedProduct" @click="submitAdjustment">
          {{ adjusting ? "در حال ثبت..." : "ثبت تراکنش" }}
        </button>
      </div>

      <!-- Warehouses -->
      <div class="card section-card">
        <div class="section-head">
          <h3>انبارها</h3>
          <button class="btn btn-outline btn-sm" @click="warehouseFormOpen = !warehouseFormOpen">
            {{ warehouseFormOpen ? "بستن" : "+ انبار جدید" }}
          </button>
        </div>

        <div v-if="warehouseFormOpen" class="warehouse-form">
          <input v-model="warehouseForm.name" type="text" placeholder="نام انبار" />
          <input v-model="warehouseForm.address" type="text" placeholder="آدرس (اختیاری)" />
          <label class="checkbox-label"><input v-model="warehouseForm.is_default" type="checkbox" /> انبار پیش‌فرض</label>
          <button class="btn btn-primary btn-sm" :disabled="savingWarehouse" @click="saveWarehouse">ذخیره</button>
        </div>

        <ul class="warehouse-list">
          <li v-for="w in warehouses" :key="w.id">
            <span>{{ w.name }}</span>
            <span v-if="w.is_default" class="badge badge-accent">پیش‌فرض</span>
          </li>
          <li v-if="warehouses.length === 0" class="text-muted">هنوز انباری ثبت نشده.</li>
        </ul>
      </div>
    </div>

    <!-- Movements ledger -->
    <div class="card table-card">
      <div class="section-head">
        <h3>دفترکل تراکنش‌های انبار</h3>
        <input v-model="movementProductFilter" type="text" placeholder="فیلتر بر اساس نام محصول..." @input="debouncedFetchMovements" />
      </div>

      <AppLoader v-if="loadingMovements" />
      <table v-else class="admin-table">
        <thead>
          <tr>
            <th>محصول</th>
            <th>نوع</th>
            <th>تعداد</th>
            <th>انبار</th>
            <th>مرجع</th>
            <th>ثبت‌کننده</th>
            <th>تاریخ</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="m in movements" :key="m.id">
            <td>{{ m.product_name }} <span v-if="m.variant_label" class="text-muted">({{ m.variant_label }})</span></td>
            <td>
              <span class="badge" :class="m.is_increase ? 'badge-status-paid' : 'badge-status-cancelled'">
                {{ m.movement_type_display }}
              </span>
            </td>
            <td>{{ m.quantity }}</td>
            <td>{{ m.warehouse_name || "—" }}</td>
            <td class="text-muted">{{ m.reference || m.note || "—" }}</td>
            <td class="text-muted">{{ m.created_by_username || "سیستم" }}</td>
            <td class="text-muted">{{ formatDateTime(m.created_at) }}</td>
          </tr>
        </tbody>
      </table>
      <p v-if="!loadingMovements && movements.length === 0" class="text-muted empty-row">تراکنشی ثبت نشده.</p>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

const MOVEMENT_INCREASE_TYPES = ["return", "restock", "adjustment_in"];

export default {
  name: "AdminInventory",
  components: { AppLoader },
  data() {
    return {
      warehouses: [],
      movements: [],
      loadingMovements: true,
      warehouseFormOpen: false,
      savingWarehouse: false,
      warehouseForm: { name: "", address: "", is_default: false },

      productSearch: "",
      productResults: [],
      selectedProduct: null,
      searchDebounce: null,
      adjustForm: { movement_type: "restock", quantity: 1, warehouse: null, note: "" },
      adjusting: false,
      adjustError: "",

      movementProductFilter: "",
      movementDebounce: null,
    };
  },
  created() {
    this.fetchWarehouses();
    this.fetchMovements();
  },
  methods: {
    formatDateTime(v) {
      return new Date(v).toLocaleString("fa-IR");
    },
    debouncedSearch() {
      clearTimeout(this.searchDebounce);
      this.searchDebounce = setTimeout(this.searchProducts, 350);
    },
    async searchProducts() {
      if (!this.productSearch.trim()) {
        this.productResults = [];
        return;
      }
      const { data } = await api.get("/products/", { params: { search: this.productSearch, page_size: 8 } });
      this.productResults = data.results || data;
    },
    selectProduct(product) {
      this.selectedProduct = product;
      this.productResults = [];
      this.productSearch = "";
    },
    async submitAdjustment() {
      this.adjusting = true;
      this.adjustError = "";
      try {
        await api.post("/admin/inventory/adjust/", {
          product: this.selectedProduct.id,
          movement_type: this.adjustForm.movement_type,
          quantity: this.adjustForm.quantity,
          warehouse: this.adjustForm.warehouse,
          note: this.adjustForm.note,
        });
        this.$store.dispatch("notify", { message: "تراکنش انبار ثبت شد." });
        this.selectedProduct = null;
        this.adjustForm = { movement_type: "restock", quantity: 1, warehouse: null, note: "" };
        this.fetchMovements();
      } catch (e) {
        this.adjustError = "ثبت تراکنش ناموفق بود. مقادیر را بررسی کنید.";
      } finally {
        this.adjusting = false;
      }
    },
    async fetchWarehouses() {
      const { data } = await api.get("/admin/inventory/warehouses/");
      this.warehouses = data.results || data;
    },
    async saveWarehouse() {
      this.savingWarehouse = true;
      try {
        const { data } = await api.post("/admin/inventory/warehouses/", this.warehouseForm);
        this.warehouses.push(data);
        this.warehouseForm = { name: "", address: "", is_default: false };
        this.warehouseFormOpen = false;
        this.$store.dispatch("notify", { message: "انبار جدید ثبت شد." });
        this.fetchWarehouses();
      } catch (e) {
        this.$store.dispatch("notify", { message: "ثبت انبار ناموفق بود.", type: "error" });
      } finally {
        this.savingWarehouse = false;
      }
    },
    debouncedFetchMovements() {
      clearTimeout(this.movementDebounce);
      this.movementDebounce = setTimeout(this.fetchMovements, 350);
    },
    async fetchMovements() {
      this.loadingMovements = true;
      try {
        const params = { page_size: 50 };
        const { data } = await api.get("/admin/inventory/movements/", { params });
        let results = data.results || data;
        if (this.movementProductFilter.trim()) {
          const q = this.movementProductFilter.trim();
          results = results.filter((m) => m.product_name && m.product_name.includes(q));
        }
        this.movements = results.map((m) => ({ ...m, is_increase: MOVEMENT_INCREASE_TYPES.includes(m.movement_type) }));
      } finally {
        this.loadingMovements = false;
      }
    },
  },
};
</script>

<style scoped>
.admin-inventory h1 {
  font-size: 1.4rem;
  margin-bottom: 20px;
}
.grid-2col {
  display: grid;
  grid-template-columns: 1.3fr 1fr;
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
.section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
  flex-wrap: wrap;
  gap: 10px;
}
.two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}
.product-results {
  margin-top: 6px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  max-height: 180px;
  overflow-y: auto;
}
.product-result-item {
  display: block;
  width: 100%;
  text-align: right;
  background: none;
  border: none;
  padding: 8px 12px;
  font-size: 0.83rem;
  border-bottom: 1px solid var(--color-border);
}
.product-result-item:last-child {
  border-bottom: none;
}
.product-result-item:hover {
  background: var(--color-bg);
}
.selected-product {
  margin-top: 8px;
  font-size: 0.85rem;
  background: var(--color-sand);
  padding: 8px 12px;
  border-radius: var(--radius-sm);
}
.warehouse-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px dashed var(--color-border);
}
.warehouse-form input[type="text"] {
  padding: 8px 12px;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: inherit;
  font-size: 0.85rem;
}
.checkbox-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.83rem;
}
.warehouse-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.warehouse-list li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.87rem;
  padding: 8px 0;
  border-bottom: 1px solid var(--color-border);
}
.warehouse-list li:last-child {
  border-bottom: none;
}
.table-card {
  padding: 18px;
  overflow-x: auto;
}
.table-card input {
  padding: 8px 12px;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: inherit;
  font-size: 0.83rem;
  width: 240px;
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