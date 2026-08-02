<template>
  <div class="toast-stack">
    <transition-group name="toast-fade" tag="div">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="toast"
        :class="`toast--${toast.type}`"
        @click="remove(toast.id)"
      >
        {{ toast.message }}
      </div>
    </transition-group>
  </div>
</template>

<script>
export default {
  name: "ToastStack",
  computed: {
    toasts() {
      return this.$store.state.toasts;
    },
  },
  watch: {
    toasts(list) {
      list.forEach((t) => {
        if (!t._scheduled) {
          t._scheduled = true;
          setTimeout(() => this.remove(t.id), 3200);
        }
      });
    },
  },
  methods: {
    remove(id) {
      this.$store.commit("REMOVE_TOAST", id);
    },
  },
};
</script>

<style scoped>
.toast-stack {
  position: fixed;
  bottom: 20px;
  left: 20px;
  z-index: 100;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.toast {
  background: var(--color-primary-dark);
  color: #fff;
  padding: 12px 18px;
  border-radius: var(--radius-sm);
  font-size: 0.88rem;
  box-shadow: var(--shadow-md);
  cursor: pointer;
  max-width: 320px;
}
.toast--error {
  background: var(--color-danger);
}
.toast-fade-enter-active,
.toast-fade-leave-active {
  transition: all 0.25s ease;
}
.toast-fade-enter,
.toast-fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
