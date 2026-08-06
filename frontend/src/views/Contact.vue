<template>
  <div class="container contact-page">
    <div class="contact-hero">
      <span class="eyebrow">در ارتباط باشید</span>
      <h1>تماس با یاشیل آرت</h1>
      <p class="text-muted">سوالی درباره سفارش، محصولات، یا همکاری با ما دارید؟ از راه‌های زیر در دسترس‌ایم.</p>
    </div>

    <div class="contact-grid">
      <div class="card contact-card">
        <span class="contact-card__icon">☎</span>
        <h3>تلفن پشتیبانی</h3>
        <p class="text-muted">۰۲۱-۹۱۰۰۰۰۰۰</p>
        <p class="text-muted small">شنبه تا پنجشنبه، ۹ تا ۱۸</p>
      </div>
      <div class="card contact-card">
        <span class="contact-card__icon">✉️</span>
        <h3>ایمیل</h3>
        <p class="text-muted">support@yashilart.local</p>
        <p class="text-muted small">معمولاً کمتر از ۲۴ ساعت پاسخ می‌دهیم</p>
      </div>
      <div class="card contact-card">
        <span class="contact-card__icon">📍</span>
        <h3>آدرس</h3>
        <p class="text-muted">تهران، ایران</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ContactView",
};
</script>

<style scoped>
.contact-page {
  padding: 50px 20px 60px;
}
.contact-hero {
  max-width: 560px;
  margin-bottom: 40px;
}
.contact-hero h1 {
  font-size: 1.7rem;
  margin: 10px 0 12px;
}
.contact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
}
.contact-card {
  padding: 28px 22px;
  text-align: center;
}
.contact-card__icon {
  font-size: 1.8rem;
  display: block;
  margin-bottom: 12px;
}
.contact-card h3 {
  font-size: 1rem;
  margin-bottom: 8px;
}
.contact-card .small {
  font-size: 0.78rem;
  margin-top: 4px;
}
</style>