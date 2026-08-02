<template>
  <div class="vendor-store-page">
    <AppLoader v-if="loading" />

    <div v-else-if="!vendor" class="container empty-state">
      <div class="icon">🏪</div>
      <p>این فروشگاه پیدا نشد.</p>
      <router-link to="/stores" class="btn btn-outline">مشاهده همه فروشگاه‌ها</router-link>
    </div>

    <template v-else>
      <section class="store-hero">
        <div class="container store-hero__inner">
          <div class="store-logo">
            <img v-if="vendor.logo" :src="vendor.logo" :alt="vendor.store_name" />
            <span v-else>🏪</span>
          </div>
          <div>
            <h1>{{ vendor.store_name }}</h1>
            <p v-if="vendor.description" class="text-muted">{{ vendor.description }}</p>
          </div>
        </div>
      </section>

      <section class="container products-section">
        <div class="section-heading">
          <h2>محصولات این فروشگاه</h2>
          <span class="text-muted" v-if="!productsLoading">{{ count }} محصول</span>
        </div>

        <AppLoader v-if="productsLoading" />
        <div v-else-if="products.length === 0" class="empty-state">
          <div class="icon">📦</div>
          <p>این فروشگاه هنوز محصولی ثبت نکرده است.</p>
        </div>
        <div v-else class="product-grid">
          <ProductCard v-for="p in products" :key="p.id" :product="p" />
        </div>
      </section>
    </template>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";
import ProductCard from "@/components/ProductCard.vue";

export default {
  name: "VendorStoreView",
  components: { ProductCard, AppLoader },
  data() {
    return {
      vendor: null,
      loading: true,
      products: [],
      productsLoading: true,
      count: 0,
    };
  },
  async created() {
    try {
      const { data } = await api.get(`/vendors/stores/${this.$route.params.slug}/`);
      this.vendor = data;
    } catch (e) {
      this.vendor = null;
    } finally {
      this.loading = false;
    }

    if (this.vendor) {
      try {
        const { data } = await api.get("/products/", { params: { vendor: this.$route.params.slug, page_size: 24 } });
        this.products = data.results || data;
        this.count = data.count ?? this.products.length;
      } finally {
        this.productsLoading = false;
      }
    } else {
      this.productsLoading = false;
    }
  },
};
</script>

<style scoped>
.store-hero {
  background: var(--color-sand);
  border-bottom: 1px solid var(--color-border);
}
.store-hero__inner {
  display: flex;
  align-items: center;
  gap: 22px;
  padding: 40px 20px;
}
.store-logo {
  width: 88px;
  height: 88px;
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  font-size: 2.2rem;
  flex-shrink: 0;
}
.store-logo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.store-hero h1 {
  font-size: 1.5rem;
  margin-bottom: 6px;
}
.products-section {
  padding: 36px 20px 60px;
}
.section-heading {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 22px;
}
.section-heading h2 {
  font-size: 1.2rem;
}
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
  gap: 20px;
}
</style>