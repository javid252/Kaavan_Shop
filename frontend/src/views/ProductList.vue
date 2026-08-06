<template>
  <div class="container product-list-page">
    <aside class="filters card">
      <h3>فیلترها</h3>

      <div class="filter-group">
        <label>جستجو</label>
        <input v-model="filters.search" type="text" placeholder="نام محصول..." @input="debouncedFetch" />
      </div>

      <div class="filter-group">
        <label>دسته‌بندی</label>
        <div class="filter-options">
          <button class="filter-chip" :class="{ active: !filters.category }" @click="setCategory('')">همه</button>
          <button
            v-for="cat in categories"
            :key="cat.id"
            class="filter-chip"
            :class="{ active: filters.category === cat.slug }"
            @click="setCategory(cat.slug)"
          >
            {{ cat.icon }} {{ cat.name }}
          </button>
        </div>
      </div>

      <div class="filter-group">
        <label>محدوده قیمت (تومان)</label>
        <div class="price-inputs">
          <input v-model.number="filters.min_price" type="number" placeholder="از" @change="fetchProducts" />
          <input v-model.number="filters.max_price" type="number" placeholder="تا" @change="fetchProducts" />
        </div>
      </div>

      <div class="filter-group">
        <label>مرتب‌سازی</label>
        <select v-model="filters.ordering" @change="fetchProducts">
          <option value="-created_at">جدیدترین</option>
          <option value="-sales_count">پرفروش‌ترین</option>
          <option value="price">ارزان‌ترین</option>
          <option value="-price">گران‌ترین</option>
        </select>
      </div>

      <div class="filter-group">
        <label class="checkbox-label">
          <input type="checkbox" v-model="filters.has_discount" true-value="true" false-value="" @change="fetchProducts" />
          فقط محصولات تخفیف‌دار
        </label>
      </div>
    </aside>

    <section class="results">
      <div class="results-header">
        <h2>محصولات</h2>
        <span class="text-muted" v-if="!loading">{{ count }} محصول</span>
      </div>

      <AppLoader v-if="loading" />
      <div v-else-if="products.length === 0" class="empty-state">
        <div class="icon">🔎</div>
        <p>محصولی با این فیلترها پیدا نشد.</p>
      </div>
      <div v-else class="product-grid">
        <ProductCard v-for="p in products" :key="p.id" :product="p" />
      </div>

      <div v-if="totalPages > 1" class="pagination">
        <button class="btn btn-outline btn-sm" :disabled="page <= 1" @click="goPage(page - 1)">قبلی</button>
        <span class="text-muted">صفحه {{ page }} از {{ totalPages }}</span>
        <button class="btn btn-outline btn-sm" :disabled="page >= totalPages" @click="goPage(page + 1)">بعدی</button>
      </div>
    </section>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";
import ProductCard from "@/components/ProductCard.vue";

export default {
  name: "ProductListView",
  components: { ProductCard, AppLoader },
  data() {
    return {
      products: [],
      count: 0,
      page: 1,
      loading: true,
      debounceTimer: null,
      filters: {
        search: this.$route.query.search || "",
        category: this.$route.query.category || "",
        min_price: null,
        max_price: null,
        ordering: this.$route.query.ordering || "-created_at",
        is_featured: this.$route.query.featured ? true : undefined,
        has_discount: this.$route.query.has_discount ? true : undefined,
      },
    };
  },
  computed: {
    categories() {
      return this.$store.state.products.categories;
    },
    totalPages() {
      return Math.max(Math.ceil(this.count / 12), 1);
    },
  },
  created() {
    this.$store.dispatch("products/fetchCategories");
    this.fetchProducts();
  },
  watch: {
    "$route.query"(newQuery, oldQuery) {
      if (JSON.stringify(newQuery) === JSON.stringify(oldQuery)) return;
      this.filters.search = newQuery.search || "";
      this.filters.category = newQuery.category || "";
      this.filters.ordering = newQuery.ordering || "-created_at";
      this.filters.is_featured = newQuery.featured ? true : undefined;
      this.filters.has_discount = newQuery.has_discount ? true : undefined;
      this.page = 1;
      this.fetchProducts();
    },
  },
  methods: {
    setCategory(slug) {
      this.filters.category = slug;
      this.fetchProducts();
    },
    debouncedFetch() {
      clearTimeout(this.debounceTimer);
      this.debounceTimer = setTimeout(() => this.fetchProducts(), 400);
    },
    goPage(p) {
      this.page = p;
      this.fetchProducts();
    },
    async fetchProducts() {
      this.loading = true;
      try {
        const params = { page: this.page, ...this.filters };
        Object.keys(params).forEach((k) => (params[k] === "" || params[k] == null) && delete params[k]);
        const { data } = await api.get("/products/", { params });
        this.products = data.results || data;
        this.count = data.count ?? this.products.length;
      } catch (e) {
        this.$store.dispatch("notify", { message: "بارگذاری محصولات ناموفق بود.", type: "error" });
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.product-list-page {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 30px;
  padding: 36px 20px 60px;
}
.filters {
  padding: 20px;
  align-self: start;
  position: sticky;
  top: calc(var(--header-height) + 20px);
}
.filters h3 {
  font-size: 1rem;
  margin-bottom: 16px;
}
.filter-group {
  margin-bottom: 20px;
}
.filter-group label {
  display: block;
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--color-text-muted);
  margin-bottom: 8px;
}
.filter-group input,
.filter-group select {
  width: 100%;
  padding: 9px 12px;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: inherit;
  font-size: 0.87rem;
}
.filter-options {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.filter-chip {
  text-align: right;
  background: none;
  border: none;
  padding: 6px 8px;
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
  color: var(--color-text-muted);
}
.filter-chip.active,
.filter-chip:hover {
  background: var(--color-sand);
  color: var(--color-primary-dark);
  font-weight: 700;
}
.price-inputs {
  display: flex;
  gap: 8px;
}
.checkbox-label {
  display: flex !important;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem !important;
  font-weight: 600 !important;
  color: var(--color-text) !important;
  cursor: pointer;
}
.results-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 22px;
}
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
  gap: 20px;
}
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-top: 34px;
}

@media (max-width: 860px) {
  .product-list-page {
    grid-template-columns: 1fr;
  }
  .filters {
    position: static;
  }
}
</style>