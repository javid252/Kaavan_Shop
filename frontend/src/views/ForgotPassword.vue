<template>
  <div class="auth-page">
    <form class="auth-card card fade-in" @submit.prevent="submit">
      <router-link to="/" class="auth-brand">🎨 یاشیل آرت</router-link>
      <h1>بازیابی رمز عبور</h1>

      <div v-if="sent" class="form-success-box">
        در صورتی که این ایمیل در سامانه ثبت شده باشد، لینک بازیابی برای شما ارسال شد.
      </div>

      <template v-else>
        <p class="text-muted intro">ایمیل خود را وارد کنید تا لینک بازیابی رمز عبور برایتان ارسال شود.</p>
        <div class="field">
          <label>ایمیل</label>
          <input v-model="email" type="email" required autofocus />
        </div>
        <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
          {{ loading ? "در حال ارسال..." : "ارسال لینک بازیابی" }}
        </button>
      </template>

      <p class="auth-switch">
        <router-link to="/login">بازگشت به ورود</router-link>
      </p>
    </form>
  </div>
</template>

<script>
export default {
  name: "ForgotPasswordView",
  data() {
    return { email: "", loading: false, sent: false };
  },
  methods: {
    async submit() {
      this.loading = true;
      try {
        await this.$store.dispatch("auth/requestPasswordReset", this.email);
        this.sent = true;
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.auth-page {
  min-height: calc(100vh - var(--header-height));
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 16px;
  background: var(--color-sand);
}
.auth-card {
  width: 100%;
  max-width: 400px;
  padding: 34px 30px;
}
.auth-brand {
  display: block;
  text-align: center;
  font-weight: 900;
  color: var(--color-primary);
  margin-bottom: 18px;
  font-size: 1.1rem;
}
.auth-card h1 {
  font-size: 1.2rem;
  text-align: center;
  margin-bottom: 16px;
}
.intro {
  font-size: 0.85rem;
  text-align: center;
  margin-bottom: 20px;
}
.auth-switch {
  text-align: center;
  font-size: 0.85rem;
  margin-top: 18px;
  color: var(--color-text-muted);
}
.auth-switch a {
  color: var(--color-primary);
  font-weight: 700;
}
</style>
