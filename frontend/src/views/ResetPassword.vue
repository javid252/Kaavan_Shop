<template>
  <div class="auth-page">
    <form class="auth-card card fade-in" @submit.prevent="submit">
      <router-link to="/" class="auth-brand">🎨 یاشیل آرت</router-link>
      <h1>تعیین رمز عبور جدید</h1>

      <div v-if="errorMessage" class="form-error-box">{{ errorMessage }}</div>
      <div v-if="done" class="form-success-box">
        رمز عبور شما با موفقیت تغییر کرد. اکنون می‌توانید وارد شوید.
      </div>

      <template v-if="!done">
        <div class="field">
          <label>رمز عبور جدید</label>
          <input v-model="password" type="password" required autofocus />
        </div>
        <div class="field">
          <label>تکرار رمز عبور جدید</label>
          <input v-model="passwordConfirm" type="password" required />
        </div>
        <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
          {{ loading ? "در حال ثبت..." : "تغییر رمز عبور" }}
        </button>
      </template>
      <router-link v-else to="/login" class="btn btn-primary btn-block">ورود</router-link>
    </form>
  </div>
</template>

<script>
export default {
  name: "ResetPasswordView",
  data() {
    return { password: "", passwordConfirm: "", loading: false, errorMessage: "", done: false };
  },
  methods: {
    async submit() {
      if (this.password !== this.passwordConfirm) {
        this.errorMessage = "رمزهای عبور یکسان نیستند.";
        return;
      }
      this.loading = true;
      this.errorMessage = "";
      try {
        await this.$store.dispatch("auth/confirmPasswordReset", {
          uid: this.$route.params.uid,
          token: this.$route.params.token,
          new_password: this.password,
        });
        this.done = true;
      } catch (e) {
        this.errorMessage = "لینک بازیابی نامعتبر یا منقضی‌شده است.";
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
  margin-bottom: 24px;
}
</style>
