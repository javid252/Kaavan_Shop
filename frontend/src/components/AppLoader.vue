<template>
  <div class="loader" :style="{ padding: padding }">
    <span class="loader__dot" />
    <span class="loader__dot" />
    <span class="loader__dot" />
  </div>
</template>

<script>
export default {
  name: "AppLoader",
  props: {
    padding: { type: String, default: "40px 0" },
  },
};
</script>

<style scoped>
.loader {
  display: flex;
  justify-content: center;
  gap: 6px;
}
.loader__dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-accent);
  animation: loaderBounce 1s infinite ease-in-out;
}
.loader__dot:nth-child(2) {
  animation-delay: 0.15s;
}
.loader__dot:nth-child(3) {
  animation-delay: 0.3s;
}
@keyframes loaderBounce {
  0%,
  80%,
  100% {
    transform: scale(0.6);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}
</style>
