<template>
  <div id="app-shell" :class="{ 'admin-theme': isAdminRoute }">
    <AppHeader v-if="!isAdminRoute" />
    <main class="main-content">
      <router-view />
    </main>
    <AppFooter v-if="!isAdminRoute" />
    <ToastStack />
  </div>
</template>

<script>
import AppFooter from "@/components/AppFooter.vue";
import AppHeader from "@/components/AppHeader.vue";
import ToastStack from "@/components/ToastStack.vue";

export default {
  name: "App",
  components: { AppHeader, AppFooter, ToastStack },
  computed: {
    isAdminRoute() {
      return this.$route.path.startsWith("/admin");
    },
  },
};
</script>
