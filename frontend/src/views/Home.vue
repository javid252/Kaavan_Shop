<template>
  <div class="home">
    <HeroSlider />
    <CategoryGrid
      :categories="categories"
    />
    <RouteDivider />
    <section class="container featured-section">
      <div class="section-heading">
        <div>
          <span class="eyebrow">پیشنهاد یاشیل آرت</span>
          <h2>محصولات ویژه</h2>
        </div>
        <router-link to="/products" class="see-all">مشاهده همه ←</router-link>
      </div>

      <AppLoader v-if="loading" />
      <div v-else class="product-grid">
        <ProductCard v-for="p in featured" :key="p.id" :product="p" />
      </div>
    </section>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";
import ProductCard from "@/components/ProductCard.vue";
import RouteDivider from "@/components/RouteDivider.vue";
import HeroSlider from "@/components/HeroSlider.vue";
import CategoryGrid from "@/components/CategoryGrid.vue";

export default {
  name: "HomeView",
  components: {
    ProductCard,
    RouteDivider,
    AppLoader,
    HeroSlider,
    CategoryGrid
  },
  data() {
    return { featured: [], loading: true };
  },
  computed: {
    categories() {
      return this.$store.state.products.categories;
    },
  },
  async created() {
    this.$store.dispatch("products/fetchCategories");
    try {
      const { data } = await api.get("/products/", { params: { is_featured: true } });
      this.featured = data.results || data;
    } catch (e) {
      this.$store.dispatch("notify", { message: "بارگذاری محصولات ویژه ناموفق بود.", type: "error" });
    } finally {
      this.loading = false;
    }
  },
};
</script>

<style scoped>
.hero {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  color: #fff;
}
.hero-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 40px;
  padding: 64px 20px;
}
.hero-copy {
  max-width: 560px;
}
.hero-copy .eyebrow {
  color: var(--color-accent);
}
.hero-copy .eyebrow::before {
  background: var(--color-accent);
}
.hero-copy h1 {
  font-size: 2.4rem;
  color: #fff;
  margin: 14px 0 16px;
  line-height: 1.35;
}
.hero-copy .text-muted {
  color: rgba(255, 255, 255, 0.75);
  font-size: 1rem;
}
.hero-actions {
  display: flex;
  gap: 12px;
  margin-top: 26px;
}
.hero-art__circle {
  width: 220px;
  height: 220px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
  border: 1px dashed rgba(255, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 5rem;
}

.categories-section {
  padding: 56px 20px 10px;
}
.categories-section h2 {
  font-size: 1.5rem;
  margin: 6px 0 26px;
}
.category-route {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
}
.category-stop {
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 30px;
  padding: 10px 20px;
  font-weight: 700;
  font-size: 0.9rem;
  transition: border-color 0.15s ease, transform 0.15s ease;
}
.category-stop:hover {
  border-color: var(--color-accent);
  transform: translateY(-2px);
}
.category-stop__icon {
  font-size: 1.1rem;
}

.featured-section {
  padding: 40px 20px 60px;
}
.section-heading {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: 24px;
}
.section-heading h2 {
  font-size: 1.5rem;
  margin-top: 6px;
}
.see-all {
  font-weight: 700;
  color: var(--color-primary);
  font-size: 0.88rem;
}
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}

@media (max-width: 780px) {
  .hero-inner {
    flex-direction: column;
    text-align: center;
  }
  .hero-copy {
    max-width: 100%;
  }
  .hero-actions {
    justify-content: center;
  }
}
</style>
