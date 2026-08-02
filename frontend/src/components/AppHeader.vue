<template>
  <header class="site-header">
    <div class="container header-inner">
      <router-link to="/" class="brand">
        <span class="brand__mark">🎨</span>
        <span class="brand__name">یاشیل آرت</span>
      </router-link>

      <nav class="main-nav">
        <router-link to="/" exact>خانه</router-link>
        <router-link to="/products">محصولات</router-link>
        <router-link v-if="multivendorEnabled" to="/stores">فروشگاه‌ها</router-link>
        <router-link v-if="isAuthenticated" to="/my-orders">سفارش‌های من</router-link>
        <router-link v-if="isApprovedVendor" to="/vendor">پنل فروشنده</router-link>
        <router-link v-if="isAdmin" to="/admin">پنل ادمین</router-link>
      </nav>

      <div class="header-actions">
        <router-link to="/cart" class="cart-link" aria-label="سبد خرید">
          <span class="cart-icon">🛒</span>
          <span v-if="itemCount" class="cart-badge">{{ itemCount }}</span>
        </router-link>

        <div v-if="isAuthenticated" class="user-menu">
          <button class="user-menu__trigger" @click="menuOpen = !menuOpen">
            {{ userLabel }}
          </button>
          <div v-if="menuOpen" class="user-menu__dropdown" @click="menuOpen = false">
            <router-link to="/my-orders">سفارش‌های من</router-link>
            <router-link v-if="isApprovedVendor" to="/vendor">پنل فروشنده</router-link>
            <router-link v-else-if="multivendorEnabled && !isVendor" to="/become-vendor">فروشنده شوید</router-link>
            <router-link v-else-if="isVendor" to="/become-vendor">وضعیت درخواست فروشندگی</router-link>
            <button class="logout-btn" @click="logout">خروج</button>
          </div>
        </div>
        <router-link v-else to="/login" class="btn btn-primary btn-sm">ورود</router-link>
      </div>
    </div>
  </header>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "AppHeader",
  data() {
    return { menuOpen: false };
  },
  computed: {
    ...mapGetters("auth", ["isAuthenticated", "isAdmin", "currentUser"]),
    ...mapGetters("cart", ["itemCount"]),
    ...mapGetters("platform", ["multivendorEnabled"]),
    ...mapGetters("vendor", ["isVendor", "isApprovedVendor"]),
    userLabel() {
      return this.currentUser
        ? this.currentUser.first_name || this.currentUser.username
        : "";
    },
  },
  methods: {
    logout() {
      this.$store.dispatch("auth/logout");
      this.$store.dispatch("notify", { message: "با موفقیت خارج شدید." });
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
.site-header {
  position: sticky;
  top: 0;
  z-index: 40;
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
}
.header-inner {
  height: var(--header-height);
  display: flex;
  align-items: center;
  gap: 28px;
}
.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 900;
  font-size: 1.3rem;
  color: var(--color-primary);
}
.brand__mark {
  font-size: 1.3rem;
}
.main-nav {
  display: flex;
  gap: 22px;
  flex: 1;
}
.main-nav a {
  font-weight: 600;
  color: var(--color-text-muted);
  font-size: 0.92rem;
  padding: 6px 0;
  border-bottom: 2px solid transparent;
}
.main-nav a.router-link-active,
.main-nav a.router-link-exact-active {
  color: var(--color-primary);
  border-bottom-color: var(--color-accent);
}
.header-actions {
  display: flex;
  align-items: center;
  gap: 14px;
}
.cart-link {
  position: relative;
  font-size: 1.25rem;
  display: flex;
}
.cart-badge {
  position: absolute;
  top: -6px;
  left: -8px;
  background: var(--color-accent);
  color: var(--color-primary-dark);
  font-size: 0.68rem;
  font-weight: 800;
  border-radius: 50%;
  min-width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 3px;
}
.user-menu {
  position: relative;
}
.user-menu__trigger {
  background: var(--color-sand);
  border: none;
  border-radius: 20px;
  padding: 7px 16px;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--color-primary-dark);
}
.user-menu__dropdown {
  position: absolute;
  top: 42px;
  left: 0;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-md);
  min-width: 150px;
  display: flex;
  flex-direction: column;
  padding: 6px;
}
.user-menu__dropdown a,
.user-menu__dropdown button {
  text-align: right;
  background: none;
  border: none;
  padding: 9px 12px;
  border-radius: var(--radius-sm);
  font-size: 0.88rem;
  color: var(--color-text);
}
.user-menu__dropdown a:hover,
.user-menu__dropdown button:hover {
  background: var(--color-bg);
}
.logout-btn {
  color: var(--color-danger) !important;
}

@media (max-width: 720px) {
  .main-nav {
    display: none;
  }
}
</style>