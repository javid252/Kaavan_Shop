<template>
  <div class="container not-found">
    <div class="empty-state">
      <div class="icon">🎨</div>
      <h1>۴۰۴</h1>
      <p>این مسیر در نقشه کاروان ما وجود ندارد.</p>
      <router-link to="/" class="btn btn-primary">بازگشت به خانه</router-link>
    </div>
  </div>
</template>

<script>
export default { name: "NotFoundView" };
</script>

<style scoped>
.not-found {
  min-height: 50vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
.not-found h1 {
  font-size: 2rem;
  margin: 10px 0;
}
</style>
