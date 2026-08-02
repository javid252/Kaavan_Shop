<template>
  <div class="container stores-page">
    <h1>فروشگاه‌های یاشیل آرت</h1>
    <p class="text-muted intro">مجموعه‌ای از فروشندگان مستقلی که محصولات خودشان را در یاشیل آرت عرضه می‌کنند.</p>

    <AppLoader v-if="loading" />
    <div v-else-if="vendors.length === 0" class="empty-state">
      <div class="icon">🏪</div>
      <p>هنوز هیچ فروشگاهی فعال نشده است.</p>
    </div>
    <div v-else class="store-grid">
      <router-link v-for="v in vendors" :key="v.id" :to="`/store/${v.store_slug}`" class="store-card card">
        <div class="store-card__logo">
          <img v-if="v.logo" :src="v.logo" :alt="v.store_name" />
          <span v-else>🏪</span>
        </div>
        <h3>{{ v.store_name }}</h3>
        <p v-if="v.description" class="text-muted">{{ v.description }}</p>
      </router-link>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

export default {
  name: "VendorStoreListView",
  components: { AppLoader },
  data() {
    return { vendors: [], loading: true };
  },
  async created() {
    try {
      const { data } = await api.get("/vendors/stores/", { params: { page_size: 100 } });
      this.vendors = data.results || data;
    } finally {
      this.loading = false;
    }
  },
};
</script>

<style scoped>
.stores-page {
  padding: 36px 20px 60px;
}
.stores-page h1 {
  font-size: 1.6rem;
  margin-bottom: 8px;
}
.intro {
  margin-bottom: 30px;
  font-size: 0.9rem;
}
.store-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}
.store-card {
  padding: 22px;
  text-align: center;
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}
.store-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-3px);
}
.store-card__logo {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: var(--color-sand);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  font-size: 1.6rem;
  margin: 0 auto 14px;
}
.store-card__logo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.store-card h3 {
  font-size: 1rem;
  margin-bottom: 6px;
}
.store-card p {
  font-size: 0.82rem;
  line-height: 1.6;
}
</style>