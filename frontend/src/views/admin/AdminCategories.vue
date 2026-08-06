<template>
  <div class="admin-categories">
    <div class="page-head">
      <h1>دسته‌بندی‌ها</h1>
      <button class="btn btn-primary btn-sm" @click="startCreate">+ دسته‌بندی جدید</button>
    </div>

    <div v-if="formOpen" class="card form-card">
      <h3>{{ editingId ? "ویرایش دسته‌بندی" : "دسته‌بندی جدید" }}</h3>
      <div v-if="errorMessage" class="form-error-box">{{ errorMessage }}</div>

      <div class="logo-row">
        <div class="logo-preview">
          <img v-if="imagePreview" :src="imagePreview" alt="تصویر دسته" />
          <span v-else>{{ form.icon || "📦" }}</span>
        </div>
        <div>
          <input type="file" accept="image/*" @change="onImageSelected" />
          <p class="text-muted logo-hint">اگر تصویر آپلود نکنید، همان آیکون/اموجی زیر نشان داده می‌شود.</p>
        </div>
      </div>

      <div class="two-col">
        <div class="field">
          <label>نام دسته‌بندی</label>
          <input v-model="form.name" type="text" required />
        </div>
        <div class="field">
          <label>آیکون (اموجی جایگزین، اختیاری)</label>
          <input v-model="form.icon" type="text" placeholder="مثلاً 👕" />
        </div>
      </div>

      <div class="two-col">
        <div class="field">
          <label>دسته والد (اختیاری)</label>
          <select v-model="form.parent">
            <option :value="null">بدون والد</option>
            <option v-for="c in categories.filter((c) => c.id !== editingId)" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
        </div>
        <div class="field">
          <label>ترتیب نمایش</label>
          <input v-model.number="form.order" type="number" min="0" />
        </div>
      </div>

      <div class="checkbox-row">
        <label><input v-model="form.is_active" type="checkbox" /> فعال / قابل نمایش</label>
      </div>

      <div class="form-actions">
        <button class="btn btn-outline btn-sm" @click="cancelForm">انصراف</button>
        <button class="btn btn-primary" :disabled="saving" @click="save">
          {{ saving ? "در حال ذخیره..." : "ذخیره" }}
        </button>
      </div>
    </div>

    <div class="card table-card">
      <AppLoader v-if="loading" />
      <table v-else class="admin-table">
        <thead>
          <tr>
            <th>تصویر</th>
            <th>نام</th>
            <th>والد</th>
            <th>ترتیب</th>
            <th>وضعیت</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in categories" :key="c.id">
            <td>
              <div class="row-thumb">
                <img v-if="c.image" :src="c.image" :alt="c.name" />
                <span v-else>{{ c.icon || "📦" }}</span>
              </div>
            </td>
            <td class="name-cell">{{ c.name }}</td>
            <td>{{ parentName(c.parent) }}</td>
            <td>{{ c.order }}</td>
            <td>
              <span class="badge" :class="c.is_active ? 'badge-status-paid' : 'badge-status-cancelled'">
                {{ c.is_active ? "فعال" : "غیرفعال" }}
              </span>
            </td>
            <td class="actions-cell">
              <button class="btn btn-outline btn-sm" @click="startEdit(c)">ویرایش</button>
              <button class="btn btn-danger btn-sm" @click="remove(c)">حذف</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-if="!loading && categories.length === 0" class="text-muted empty-row">هنوز دسته‌بندی‌ای ثبت نشده.</p>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

const EMPTY_FORM = { name: "", icon: "", parent: null, order: 0, is_active: true };

export default {
  name: "AdminCategories",
  components: { AppLoader },
  data() {
    return {
      categories: [],
      loading: true,
      formOpen: false,
      saving: false,
      errorMessage: "",
      editingId: null,
      form: { ...EMPTY_FORM },
      imageFile: null,
      imagePreview: null,
    };
  },
  created() {
    this.fetchCategories();
  },
  methods: {
    parentName(parentId) {
      const parent = this.categories.find((c) => c.id === parentId);
      return parent ? parent.name : "—";
    },
    async fetchCategories() {
      this.loading = true;
      try {
        const { data } = await api.get("/categories/", { params: { page_size: 100 } });
        this.categories = data.results || data;
      } finally {
        this.loading = false;
      }
    },
    startCreate() {
      this.editingId = null;
      this.form = { ...EMPTY_FORM };
      this.imageFile = null;
      this.imagePreview = null;
      this.errorMessage = "";
      this.formOpen = true;
    },
    startEdit(category) {
      this.editingId = category.id;
      this.form = {
        name: category.name,
        icon: category.icon,
        parent: category.parent,
        order: category.order,
        is_active: category.is_active,
      };
      this.imageFile = null;
      this.imagePreview = category.image;
      this.errorMessage = "";
      this.formOpen = true;
    },
    cancelForm() {
      this.formOpen = false;
    },
    onImageSelected(event) {
      const file = event.target.files[0];
      if (!file) return;
      this.imageFile = file;
      this.imagePreview = URL.createObjectURL(file);
    },
    buildFormData() {
      const formData = new FormData();
      Object.entries(this.form).forEach(([key, value]) => {
        if (value !== null && value !== undefined) formData.append(key, value);
      });
      if (this.imageFile) formData.append("image", this.imageFile);
      return formData;
    },
    async save() {
      this.saving = true;
      this.errorMessage = "";
      try {
        const formData = this.buildFormData();
        if (this.editingId) {
          const category = this.categories.find((c) => c.id === this.editingId);
          await api.patch(`/categories/${category.slug}/`, formData);
          this.$store.dispatch("notify", { message: "دسته‌بندی به‌روزرسانی شد." });
        } else {
          await api.post("/categories/", formData);
          this.$store.dispatch("notify", { message: "دسته‌بندی جدید ثبت شد." });
        }
        this.formOpen = false;
        this.$store.commit("products/SET_CATEGORIES", []);
        await this.fetchCategories();
      } catch (e) {
        this.errorMessage = "ذخیره ناموفق بود. مقادیر را بررسی کنید.";
      } finally {
        this.saving = false;
      }
    },
    async remove(category) {
      if (!confirm(`دسته‌بندی «${category.name}» حذف شود؟`)) return;
      try {
        await api.delete(`/categories/${category.slug}/`);
        this.$store.dispatch("notify", { message: "دسته‌بندی حذف شد." });
        this.$store.commit("products/SET_CATEGORIES", []);
        this.fetchCategories();
      } catch (e) {
        this.$store.dispatch("notify", { message: "حذف ناموفق بود.", type: "error" });
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
  padding: 24px;
  margin-bottom: 20px;
  max-width: 640px;
}
.form-card h3 {
  font-size: 1rem;
  margin-bottom: 16px;
}
.logo-row {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
  padding-bottom: 18px;
  border-bottom: 1px dashed var(--color-border);
}
.logo-preview {
  width: 64px;
  height: 64px;
  border-radius: var(--radius);
  background: var(--color-sand);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  font-size: 1.7rem;
  flex-shrink: 0;
}
.logo-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.logo-hint {
  font-size: 0.78rem;
  margin-top: 6px;
}
.two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
.checkbox-row {
  margin-bottom: 20px;
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
  gap: 10px;
}
.table-card {
  padding: 18px;
}
.admin-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.87rem;
}
.admin-table th {
  text-align: right;
  color: var(--color-text-muted);
  font-weight: 700;
  padding: 10px 12px;
  border-bottom: 1.5px solid var(--color-border);
  font-size: 0.8rem;
}
.admin-table td {
  padding: 10px 12px;
  border-bottom: 1px solid var(--color-border);
  vertical-align: middle;
}
.row-thumb {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: var(--color-sand);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  font-size: 1.1rem;
}
.row-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.name-cell {
  font-weight: 700;
}
.actions-cell {
  display: flex;
  gap: 8px;
}
.empty-row {
  text-align: center;
  padding: 30px;
}
</style>