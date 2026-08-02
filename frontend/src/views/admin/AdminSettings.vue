<template>
  <div class="admin-settings">
    <h1>تنظیمات پلتفرم</h1>

    <AppLoader v-if="loading" />

    <div v-else class="card settings-card">
      <div class="toggle-row">
        <div>
          <h3>حالت چندفروشندگی</h3>
          <p class="text-muted">
            وقتی روشن باشد، کاربران می‌توانند درخواست فروشندگی بدهند و بعد از تایید شما،
            محصولات خودشان را مدیریت کنند. وقتی خاموش باشد، سایت دقیقاً مثل یک فروشگاه
            تک‌مالکیتی معمولی کار می‌کند و هیچ بخش فروشندگی در سایت دیده نمی‌شود.
          </p>
        </div>
        <label class="toggle-switch">
          <input type="checkbox" v-model="form.multivendor_enabled" />
          <span class="toggle-switch__slider"></span>
        </label>
      </div>

      <div v-if="form.multivendor_enabled" class="field commission-field">
        <label>درصد کارمزد پیش‌فرض پلتفرم (اختیاری)</label>
        <input v-model.number="form.default_commission_percent" type="number" min="0" max="100" step="0.5" placeholder="مثلاً 10" />
        <p class="text-muted field-hint">
          اگر برای یک فروشنده خاص در صفحه «فروشندگان» کارمزد جداگانه تنظیم نشده باشد، همین عدد استفاده می‌شود.
          فعلاً این عدد فقط ذخیره می‌شود و منطق تسویه‌حساب خودکار در فاز بعد اضافه خواهد شد.
        </p>
      </div>

      <button class="btn btn-primary" :disabled="saving" @click="save">
        {{ saving ? "در حال ذخیره..." : "ذخیره تنظیمات" }}
      </button>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

export default {
  name: "AdminSettings",
  components: { AppLoader },
  data() {
    return {
      loading: true,
      saving: false,
      form: { multivendor_enabled: false, default_commission_percent: null },
    };
  },
  async created() {
    try {
      const { data } = await api.get("/admin/settings/");
      this.form = data;
    } finally {
      this.loading = false;
    }
  },
  methods: {
    async save() {
      this.saving = true;
      try {
        const { data } = await api.patch("/admin/settings/", this.form);
        this.form = data;
        this.$store.commit("platform/SET_SETTINGS", { multivendor_enabled: data.multivendor_enabled });
        this.$store.dispatch("notify", { message: "تنظیمات ذخیره شد." });
      } catch (e) {
        this.$store.dispatch("notify", { message: "ذخیره تنظیمات ناموفق بود.", type: "error" });
      } finally {
        this.saving = false;
      }
    },
  },
};
</script>

<style scoped>
.admin-settings h1 {
  font-size: 1.4rem;
  margin-bottom: 20px;
}
.settings-card {
  padding: 26px;
  max-width: 620px;
}
.toggle-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 22px;
}
.toggle-row h3 {
  font-size: 0.95rem;
  margin-bottom: 8px;
}
.toggle-row p {
  font-size: 0.83rem;
  line-height: 1.7;
}
.toggle-switch {
  position: relative;
  display: inline-block;
  width: 46px;
  height: 26px;
  flex-shrink: 0;
}
.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}
.toggle-switch__slider {
  position: absolute;
  cursor: pointer;
  inset: 0;
  background: var(--color-border);
  border-radius: 30px;
  transition: 0.2s;
}
.toggle-switch__slider::before {
  content: "";
  position: absolute;
  width: 20px;
  height: 20px;
  right: 3px;
  top: 3px;
  background: #fff;
  border-radius: 50%;
  transition: 0.2s;
}
.toggle-switch input:checked + .toggle-switch__slider {
  background: var(--color-primary);
}
.toggle-switch input:checked + .toggle-switch__slider::before {
  transform: translateX(-20px);
}
.commission-field {
  border-top: 1px dashed var(--color-border);
  padding-top: 20px;
  margin-bottom: 22px;
}
.field-hint {
  font-size: 0.78rem;
  margin-top: 6px;
}
</style>