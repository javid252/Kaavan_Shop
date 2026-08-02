<template>
  <div class="container become-vendor-page">
    <div v-if="!multivendorEnabled" class="empty-state">
      <div class="icon">🚧</div>
      <p>در حال حاضر امکان ثبت‌نام فروشنده در این سایت فعال نیست.</p>
      <router-link to="/" class="btn btn-outline">بازگشت به خانه</router-link>
    </div>

    <div v-else-if="vendorStatus" class="card status-card fade-in">
      <template v-if="vendorStatus === 'pending'">
        <div class="icon">⏳</div>
        <h1>درخواست شما در انتظار بررسی است</h1>
        <p class="text-muted">فروشگاه «{{ profile.store_name }}» ثبت شد و به‌محض تایید ادمین، به پنل فروشندگی دسترسی خواهید داشت.</p>
      </template>
      <template v-else-if="vendorStatus === 'approved'">
        <div class="icon">✅</div>
        <h1>فروشگاه شما تایید شده است</h1>
        <p class="text-muted">می‌توانید از همین‌جا وارد پنل فروشندگی خود شوید.</p>
        <router-link to="/vendor" class="btn btn-primary">ورود به پنل فروشنده</router-link>
      </template>
      <template v-else-if="vendorStatus === 'rejected'">
        <div class="icon">❌</div>
        <h1>درخواست شما رد شده است</h1>
        <p class="text-muted">برای اطلاعات بیشتر با پشتیبانی تماس بگیرید.</p>
      </template>
      <template v-else>
        <div class="icon">⛔</div>
        <h1>حساب فروشندگی شما معلق شده است</h1>
        <p class="text-muted">برای اطلاعات بیشتر با پشتیبانی تماس بگیرید.</p>
      </template>
    </div>

    <form v-else class="card apply-card fade-in" @submit.prevent="submit">
      <h1>ثبت‌نام به‌عنوان فروشنده</h1>
      <p class="text-muted intro">اطلاعات فروشگاه خود را وارد کنید؛ بعد از تایید ادمین، به پنل فروشندگی دسترسی خواهید داشت.</p>

      <div v-if="errorMessage" class="form-error-box">{{ errorMessage }}</div>

      <div class="field">
        <label>نام فروشگاه</label>
        <input v-model="form.store_name" type="text" required />
      </div>
      <div class="field">
        <label>توضیحات فروشگاه</label>
        <textarea v-model="form.description" rows="4" placeholder="چه محصولاتی می‌فروشید؟"></textarea>
      </div>

      <button type="submit" class="btn btn-primary btn-block" :disabled="submitting">
        {{ submitting ? "در حال ارسال..." : "ارسال درخواست" }}
      </button>
    </form>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "BecomeVendorView",
  data() {
    return {
      form: { store_name: "", description: "" },
      submitting: false,
      errorMessage: "",
    };
  },
  computed: {
    ...mapGetters("platform", ["multivendorEnabled"]),
    ...mapGetters("vendor", ["vendorStatus", "profile"]),
  },
  async created() {
    if (!this.$store.state.vendor.checked) {
      await this.$store.dispatch("vendor/fetchMe");
    }
  },
  methods: {
    async submit() {
      this.submitting = true;
      this.errorMessage = "";
      try {
        await this.$store.dispatch("vendor/apply", this.form);
        this.$store.dispatch("notify", { message: "درخواست فروشندگی شما ثبت شد." });
      } catch (e) {
        this.errorMessage = "ثبت درخواست ناموفق بود. لطفاً دوباره تلاش کنید.";
      } finally {
        this.submitting = false;
      }
    },
  },
};
</script>

<style scoped>
.become-vendor-page {
  padding: 50px 20px;
  display: flex;
  justify-content: center;
}
.apply-card,
.status-card {
  max-width: 460px;
  width: 100%;
  padding: 36px 32px;
  text-align: center;
}
.apply-card {
  text-align: right;
}
.apply-card h1,
.status-card h1 {
  font-size: 1.25rem;
  margin-bottom: 8px;
}
.status-card .icon {
  font-size: 2.4rem;
  margin-bottom: 10px;
}
.intro {
  font-size: 0.85rem;
  margin-bottom: 20px;
  text-align: right;
}
.status-card .text-muted {
  margin-bottom: 20px;
}
</style>