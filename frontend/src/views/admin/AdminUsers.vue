<template>
  <div class="admin-users">
    <h1>کاربران</h1>

    <div class="card table-card">
      <AppLoader v-if="loading" />
      <table v-else class="admin-table">
        <thead>
          <tr>
            <th>نام کاربری</th>
            <th>ایمیل</th>
            <th>نقش‌ها</th>
            <th>تاریخ عضویت</th>
            <th>مدیر سیستم</th>
            <th>وضعیت</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in users" :key="u.id">
            <td>{{ u.username }} <span v-if="u.first_name" class="text-muted">({{ u.first_name }} {{ u.last_name }})</span></td>
            <td>{{ u.email }}</td>
            <td class="roles-cell">
              <select multiple :value="u.groups" class="roles-select" @change="updateGroups(u, $event)">
                <option v-for="role in roles" :key="role.id" :value="role.id">{{ role.name }}</option>
              </select>
              <p class="text-muted roles-hint">با Ctrl/Cmd چند نقش انتخاب کنید</p>
            </td>
            <td>{{ formatDate(u.date_joined) }}</td>
            <td>
              <label class="switch">
                <input type="checkbox" :checked="u.is_staff" @change="toggle(u, 'is_staff', $event.target.checked)" />
                <span>{{ u.is_staff ? "بله" : "خیر" }}</span>
              </label>
            </td>
            <td>
              <label class="switch">
                <input type="checkbox" :checked="u.is_active" @change="toggle(u, 'is_active', $event.target.checked)" />
                <span>{{ u.is_active ? "فعال" : "غیرفعال" }}</span>
              </label>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-if="!loading && users.length === 0" class="text-muted empty-row">کاربری یافت نشد.</p>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

export default {
  name: "AdminUsers",
  components: { AppLoader },
  data() {
    return { users: [], roles: [], loading: true };
  },
  created() {
    this.fetchUsers();
    this.fetchRoles();
  },
  methods: {
    formatDate(v) {
      return new Date(v).toLocaleDateString("fa-IR");
    },
    async fetchUsers() {
      this.loading = true;
      try {
        const { data } = await api.get("/admin/users/", { params: { page_size: 100 } });
        this.users = data.results || data;
      } finally {
        this.loading = false;
      }
    },
    async fetchRoles() {
      try {
        const { data } = await api.get("/admin/roles/");
        this.roles = data.results || data;
      } catch (e) {
        this.roles = [];
      }
    },
    async toggle(user, field, value) {
      try {
        await api.patch(`/admin/users/${user.id}/`, { [field]: value });
        user[field] = value;
        this.$store.dispatch("notify", { message: "کاربر به‌روزرسانی شد." });
      } catch (e) {
        this.$store.dispatch("notify", { message: "به‌روزرسانی ناموفق بود.", type: "error" });
      }
    },
    async updateGroups(user, event) {
      const selectedIds = Array.from(event.target.selectedOptions).map((o) => Number(o.value));
      try {
        const { data } = await api.patch(`/admin/users/${user.id}/`, { groups: selectedIds });
        user.groups = data.groups;
        user.group_names = data.group_names;
        this.$store.dispatch("notify", { message: `نقش‌های ${user.username} به‌روزرسانی شد.` });
      } catch (e) {
        this.$store.dispatch("notify", { message: "به‌روزرسانی نقش ناموفق بود.", type: "error" });
      }
    },
  },
};
</script>

<style scoped>
.admin-users h1 {
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
  font-size: 0.87rem;
  min-width: 780px;
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
  vertical-align: top;
}
.switch {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.82rem;
  cursor: pointer;
}
.roles-cell {
  min-width: 160px;
}
.roles-select {
  width: 100%;
  min-height: 60px;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: inherit;
  font-size: 0.8rem;
  padding: 4px;
}
.roles-hint {
  font-size: 0.7rem;
  margin-top: 4px;
}
.empty-row {
  text-align: center;
  padding: 30px;
}
</style>