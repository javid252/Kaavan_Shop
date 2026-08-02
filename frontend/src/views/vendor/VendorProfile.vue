<template>
  <div class="vendor-profile">
    <h1>پروفایل فروشگاه</h1>

    <AppLoader v-if="loading" />

    <form v-else class="card form-card" @submit.prevent="save">
      <div v-if="errorMessage" class="form-error-box">{{ errorMessage }}</div>

      <div class="logo-row">
        <div class="logo-preview">
          <img v-if="logoPreview" :src="logoPreview" alt="لوگوی فروشگاه" />
          <span v-else>🏪</span>
        </div>
        <div>
          <input type="file" accept="image/*" @change="onLogoSelected" />
          <p class="text-muted logo-hint">لوگو بلافاصله بعد از انتخاب آپلود می‌شود.</p>
        </div>
      </div>

      <div class="field">
        <label>نام فروشگاه</label>
        <input v-model="form.store_name" type="text" required />
      </div>
      <div class="field">
        <label>توضیحات فروشگاه</label>
        <textarea v-model="form.description" rows="4"></textarea>
      </div>
      <div class="field">
        <label>وضعیت</label>
        <span class="badge" :class="statusClass">{{ statusLabel }}</span>
      </div>

      <button type="submit" class="btn btn-primary" :disabled="saving">
        {{ saving ? "در حال ذخیره..." : "ذخیره تغییرات" }}
      </button>
    </form>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

const LABELS = { pending: "در انتظار تایید", approved: "تاییدشده", rejected: "رد شده", suspended: "معلق" };

export default {
  name: "VendorProfile",
  components: { AppLoader },
  data() {
    return {
      loading: true,
      saving: false,
      errorMessage: "",
      form: { store_name: "", description: "" },
      logoPreview: null,
    };
  },
  computed: {
    ...mapGetters("vendor", ["profile", "vendorStatus"]),
    statusLabel() {
      return LABELS[this.vendorStatus] || this.vendorStatus;
    },
    statusClass() {
      const map = { pending: "badge-status-pending", approved: "badge-status-paid", rejected: "badge-status-cancelled", suspended: "badge-status-cancelled" };
      return map[this.vendorStatus] || "badge-muted";
    },
  },
  async created() {
    if (!this.$store.state.vendor.checked) {
      await this.$store.dispatch("vendor/fetchMe");
    }
    this.form = { store_name: this.profile.store_name, description: this.profile.description };
    this.logoPreview = this.profile.logo;
    this.loading = false;
  },
  methods: {
    async save() {
      this.saving = true;
      this.errorMessage = "";
      try {
        await this.$store.dispatch("vendor/updateProfile", this.form);
        this.$store.dispatch("notify", { message: "پروفایل فروشگاه به‌روزرسانی شد." });
      } catch (e) {
        this.errorMessage = "ذخیره ناموفق بود.";
      } finally {
        this.saving = false;
      }
    },
    async onLogoSelected(event) {
      const file = event.target.files[0];
      if (!file) return;
      this.logoPreview = URL.createObjectURL(file);
      const formData = new FormData();
      formData.append("logo", file);
      try {
        await this.$store.dispatch("vendor/updateProfile", formData);
        this.$store.dispatch("notify", { message: "لوگو به‌روزرسانی شد." });
      } catch (e) {
        this.$store.dispatch("notify", { message: "آپلود لوگو ناموفق بود.", type: "error" });
      }
    },
  },
};
</script>

<style scoped>
.vendor-profile h1 {
  font-size: 1.4rem;
  margin-bottom: 20px;
}
.form-card {
  padding: 26px;
  max-width: 560px;
}
.logo-row {
  display: flex;
  align-items: center;
  gap: 18px;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px dashed var(--color-border);
}
.logo-preview {
  width: 72px;
  height: 72px;
  border-radius: var(--radius);
  background: var(--color-sand);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  font-size: 1.8rem;
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
</style>