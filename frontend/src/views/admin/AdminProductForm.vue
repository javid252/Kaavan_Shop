<template>
  <div class="admin-product-form">
    <div class="page-head">
      <h1>{{ isEdit ? "ویرایش محصول" : "محصول جدید" }}</h1>
      <router-link to="/admin/products" class="btn btn-outline btn-sm">بازگشت به لیست</router-link>
    </div>

    <AppLoader v-if="loading" />

    <form v-else class="card form-card" @submit.prevent="submit">
      <div v-if="errorMessage" class="form-error-box">{{ errorMessage }}</div>

      <div class="two-col">
        <div class="field">
          <label>نام محصول</label>
          <input v-model="form.name" type="text" required />
        </div>
        <div class="field">
          <label>دسته‌بندی</label>
          <select v-model="form.category">
            <option :value="null">بدون دسته</option>
            <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
        </div>
      </div>

      <div class="field">
        <label>توضیحات</label>
        <textarea v-model="form.description" rows="4"></textarea>
      </div>

      <div class="three-col">
        <div class="field">
          <label>قیمت (تومان)</label>
          <input v-model.number="form.price" type="number" min="0" required />
        </div>
        <div class="field">
          <label>قیمت با تخفیف (اختیاری)</label>
          <input v-model.number="form.discount_price" type="number" min="0" />
        </div>
        <div class="field">
          <label>موجودی انبار</label>
          <input v-model.number="form.stock" type="number" min="0" required />
        </div>
      </div>

      <div class="checkbox-row">
        <label><input v-model="form.is_active" type="checkbox" /> فعال / قابل نمایش</label>
        <label><input v-model="form.is_featured" type="checkbox" /> محصول ویژه</label>
      </div>

      <div class="form-actions">
        <button type="submit" class="btn btn-primary" :disabled="submitting">
          {{ submitting ? "در حال ذخیره..." : "ذخیره محصول" }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

export default {
  name: "AdminProductForm",
  components: { AppLoader },
  data() {
    return {
      loading: false,
      submitting: false,
      errorMessage: "",
      categories: [],
      form: {
        name: "", category: null, description: "", price: 0,
        discount_price: null, stock: 0, is_active: true, is_featured: false,
      },
    };
  },
  computed: {
    isEdit() {
      return !!this.$route.params.slug;
    },
  },
  async created() {
    const { data } = await api.get("/categories/");
    this.categories = data;
    if (this.isEdit) {
      this.loading = true;
      try {
        const { data: product } = await api.get(`/products/${this.$route.params.slug}/`);
        this.form = {
          name: product.name,
          category: product.category ? product.category.id : null,
          description: product.description,
          price: Number(product.price),
          discount_price: product.discount_price ? Number(product.discount_price) : null,
          stock: product.stock,
          is_active: product.is_active !== undefined ? product.is_active : true,
          is_featured: product.is_featured,
        };
      } finally {
        this.loading = false;
      }
    }
  },
  methods: {
    async submit() {
      this.submitting = true;
      this.errorMessage = "";
      try {
        if (this.isEdit) {
          await api.patch(`/products/${this.$route.params.slug}/`, this.form);
          this.$store.dispatch("notify", { message: "محصول با موفقیت به‌روزرسانی شد." });
        } else {
          await api.post("/products/", this.form);
          this.$store.dispatch("notify", { message: "محصول جدید ثبت شد." });
        }
        this.$router.push("/admin/products");
      } catch (e) {
        this.errorMessage = "ذخیره محصول ناموفق بود. مقادیر را بررسی کنید.";
      } finally {
        this.submitting = false;
      }
    },
  },
};
</script>

<style scoped>
.page-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}
.page-head h1 {
  font-size: 1.4rem;
}
.form-card {
  padding: 26px;
  max-width: 720px;
}
.two-col {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 16px;
}
.three-col {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 16px;
}
.checkbox-row {
  display: flex;
  gap: 24px;
  margin-bottom: 22px;
  font-size: 0.88rem;
}
.checkbox-row label {
  display: flex;
  align-items: center;
  gap: 6px;
}
.form-actions {
  display: flex;
  justify-content: flex-end;
}
</style>
