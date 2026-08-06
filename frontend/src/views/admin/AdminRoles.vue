<template>
  <div class="admin-roles">
    <div class="page-head">
      <h1>نقش‌ها و دسترسی‌ها</h1>
      <button class="btn btn-primary btn-sm" @click="startCreate">+ نقش جدید</button>
    </div>

    <p class="text-muted intro">
      هر نقش مجموعه‌ای از دسترسی‌هاست. یک نقش بسازید (مثلاً «حسابدار» یا «انباردار»)، پرمیشن‌های لازم را تیک بزنید،
      و بعد از صفحه «کاربران» آن نقش را به هرکسی که خواستید نسبت دهید.
    </p>

    <div v-if="formOpen" class="card form-card">
      <h3>{{ editingId ? "ویرایش نقش" : "نقش جدید" }}</h3>
      <div v-if="errorMessage" class="form-error-box">{{ errorMessage }}</div>

      <div class="field">
        <label>نام نقش</label>
        <input v-model="form.name" type="text" placeholder="مثلاً حسابدار" required />
      </div>

      <div class="field">
        <label>دسترسی‌ها</label>
        <div class="perm-groups">
          <div v-for="(perms, app) in permissionCatalogue" :key="app" class="perm-group">
            <div class="perm-group__head">
              <label>
                <input
                  type="checkbox"
                  :checked="isAppFullySelected(perms)"
                  @change="toggleApp(perms, $event.target.checked)"
                />
                <strong>{{ appLabel(app) }}</strong>
              </label>
            </div>
            <div class="perm-group__items">
              <label v-for="perm in perms" :key="perm.id" class="perm-item">
                <input type="checkbox" :value="perm.id" v-model="form.permission_ids" />
                {{ perm.name }}
              </label>
            </div>
          </div>
        </div>
      </div>

      <div class="form-actions">
        <button class="btn btn-outline btn-sm" @click="cancelForm">انصراف</button>
        <button class="btn btn-primary" :disabled="saving" @click="save">
          {{ saving ? "در حال ذخیره..." : "ذخیره نقش" }}
        </button>
      </div>
    </div>

    <div class="card table-card">
      <AppLoader v-if="loading" />
      <table v-else class="admin-table">
        <thead>
          <tr>
            <th>نام نقش</th>
            <th>تعداد دسترسی‌ها</th>
            <th>تعداد کاربران</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="role in roles" :key="role.id">
            <td class="name-cell">{{ role.name }}</td>
            <td>{{ role.permissions.length }}</td>
            <td>{{ role.user_count }}</td>
            <td class="actions-cell">
              <button class="btn btn-outline btn-sm" @click="startEdit(role)">ویرایش</button>
              <button class="btn btn-danger btn-sm" @click="remove(role)">حذف</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-if="!loading && roles.length === 0" class="text-muted empty-row">هنوز نقشی ساخته نشده.</p>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

const APP_LABELS = {
  accounts: "کاربران",
  products: "محصولات",
  cart: "سبد خرید",
  orders: "سفارش‌ها",
  dashboard: "داشبورد",
  vendors: "فروشندگان",
  access: "دسترسی‌ها",
  inventory: "انبارداری",
  accounting: "حسابداری",
};

export default {
  name: "AdminRoles",
  components: { AppLoader },
  data() {
    return {
      roles: [],
      permissionCatalogue: {},
      loading: true,
      formOpen: false,
      saving: false,
      errorMessage: "",
      editingId: null,
      form: { name: "", permission_ids: [] },
    };
  },
  async created() {
    try {
      const [rolesRes, permsRes] = await Promise.all([
        api.get("/admin/roles/"),
        api.get("/admin/permissions/"),
      ]);
      this.roles = rolesRes.data.results || rolesRes.data;
      this.permissionCatalogue = permsRes.data;
    } catch (e) {
      this.errorMessage = "بارگذاری نقش‌ها ناموفق بود.";
    } finally {
      this.loading = false;
    }
  },
  methods: {
    appLabel(app) {
      return APP_LABELS[app] || app;
    },
    isAppFullySelected(perms) {
      return perms.every((p) => this.form.permission_ids.includes(p.id));
    },
    toggleApp(perms, checked) {
      const ids = perms.map((p) => p.id);
      if (checked) {
        this.form.permission_ids = [...new Set([...this.form.permission_ids, ...ids])];
      } else {
        this.form.permission_ids = this.form.permission_ids.filter((id) => !ids.includes(id));
      }
    },
    startCreate() {
      this.editingId = null;
      this.form = { name: "", permission_ids: [] };
      this.errorMessage = "";
      this.formOpen = true;
    },
    startEdit(role) {
      this.editingId = role.id;
      this.form = { name: role.name, permission_ids: role.permissions.map((p) => p.id) };
      this.errorMessage = "";
      this.formOpen = true;
    },
    cancelForm() {
      this.formOpen = false;
    },
    async save() {
      this.saving = true;
      this.errorMessage = "";
      try {
        if (this.editingId) {
          const { data } = await api.patch(`/admin/roles/${this.editingId}/`, this.form);
          const idx = this.roles.findIndex((r) => r.id === this.editingId);
          this.roles.splice(idx, 1, data);
          this.$store.dispatch("notify", { message: "نقش به‌روزرسانی شد." });
        } else {
          const { data } = await api.post("/admin/roles/", this.form);
          this.roles.push(data);
          this.$store.dispatch("notify", { message: "نقش جدید ساخته شد." });
        }
        this.formOpen = false;
      } catch (e) {
        this.errorMessage = "ذخیره نقش ناموفق بود.";
      } finally {
        this.saving = false;
      }
    },
    async remove(role) {
      if (!confirm(`نقش «${role.name}» حذف شود؟ کاربرانی که این نقش را دارند، دسترسی‌های آن را از دست می‌دهند.`)) return;
      try {
        await api.delete(`/admin/roles/${role.id}/`);
        this.roles = this.roles.filter((r) => r.id !== role.id);
        this.$store.dispatch("notify", { message: "نقش حذف شد." });
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
  margin-bottom: 14px;
}
.page-head h1 {
  font-size: 1.4rem;
}
.intro {
  font-size: 0.85rem;
  max-width: 640px;
  margin-bottom: 20px;
  line-height: 1.8;
}
.form-card {
  padding: 24px;
  margin-bottom: 20px;
  max-width: 720px;
}
.form-card h3 {
  font-size: 1rem;
  margin-bottom: 16px;
}
.perm-groups {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 420px;
  overflow-y: auto;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 12px;
}
.perm-group {
  border-bottom: 1px dashed var(--color-border);
  padding-bottom: 10px;
}
.perm-group:last-child {
  border-bottom: none;
  padding-bottom: 0;
}
.perm-group__head label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.88rem;
  margin-bottom: 8px;
}
.perm-group__items {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 6px;
  padding-right: 22px;
}
.perm-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8rem;
  color: var(--color-text-muted);
}
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 16px;
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
  padding: 12px;
  border-bottom: 1px solid var(--color-border);
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