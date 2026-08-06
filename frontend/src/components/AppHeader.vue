<template>
  <header class="site-header">
    <!-- Top Bar -->
    <div class="top-bar">
      <div class="container top-bar-inner">
        <div class="top-right">
          <span>🚚 ارسال رایگان</span>
          <span>🎧 پشتیبانی</span>
          <span>☎ ۰۲۱-۹۱۰۰۰۰۰۰</span>
        </div>

        <div class="top-left">
          <router-link v-if="multivendorEnabled && !isVendor" to="/become-vendor">فروشنده شوید</router-link>
          <router-link v-else-if="isVendor && !isApprovedVendor" to="/become-vendor">وضعیت درخواست فروشندگی</router-link>
        </div>
      </div>
    </div>

    <!-- Main Header -->
    <div class="main-header">
      <div class="container header-inner">
        <!-- Logo -->
        <router-link to="/" class="brand">
          <span class="brand-icon">🎨</span>
          <span class="brand-name">یاشیل آرت</span>
        </router-link>

        <!-- Search -->
        <form class="search-box" @submit.prevent="submitSearch">
          <input v-model="searchQuery" type="text" placeholder="جستجو در محصولات..." />
          <button type="submit" aria-label="جستجو">🔍</button>
        </form>

        <!-- Actions -->
        <div class="header-actions">
          <!-- Cart -->
          <router-link to="/cart" class="header-action">
            🛒
            <span>سبد خرید</span>
            <b v-if="itemCount">{{ itemCount }}</b>
          </router-link>

          <!-- User -->
          <div v-if="isAuthenticated" class="user-box" @mouseleave="menuOpen = false">
            <button @click="menuOpen = !menuOpen">👤 {{ userLabel }}</button>

            <div v-if="menuOpen" class="user-dropdown" @click="menuOpen = false">
              <router-link to="/my-orders">سفارش‌های من</router-link>
              <router-link v-if="isApprovedVendor" to="/vendor">پنل فروشنده</router-link>
              <router-link v-if="isAdmin" to="/admin">پنل ادمین</router-link>
              <button @click="logout">خروج</button>
            </div>
          </div>

          <router-link v-else to="/login" class="login-btn">ورود / ثبت‌نام</router-link>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "AppHeader",
  data() {
    return {
      menuOpen: false,
      searchQuery: "",
    };
  },
  computed: {
    ...mapGetters("auth", ["isAuthenticated", "isAdmin", "currentUser"]),
    ...mapGetters("cart", ["itemCount"]),
    ...mapGetters("platform", ["multivendorEnabled"]),
    ...mapGetters("vendor", ["isVendor", "isApprovedVendor"]),
    userLabel() {
      return this.currentUser ? this.currentUser.first_name || this.currentUser.username : "";
    },
  },
  methods: {
    submitSearch() {
      const query = this.searchQuery.trim();
      if (!query) return;
      this.$router.push({ path: "/products", query: { search: query } });
    },
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
  background: var(--color-surface);
  position: sticky;
  top: 0;
  z-index: 50;
}

/* TOP BAR */
.top-bar {
  background: var(--color-primary-dark);
  color: #fff;
  font-size: 0.82rem;
}
.top-bar-inner {
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.top-right,
.top-left {
  display: flex;
  align-items: center;
  gap: 22px;
}
.top-bar a {
  color: #fff;
}

/* MAIN HEADER */
.main-header {
  border-bottom: 1px solid var(--color-border);
}
.header-inner {
  height: 78px;
  display: flex;
  align-items: center;
  gap: 18px;
}

/* BRAND */
.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.35rem;
  font-weight: 900;
  color: var(--color-primary);
  flex-shrink: 0;
}
.brand-icon {
  font-size: 1.8rem;
}

/* SEARCH */
.search-box {
  flex: 1;
  display: flex;
  height: 46px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  overflow: hidden;
}
.search-box input {
  flex: 1;
  border: none;
  padding: 0 18px;
  font-family: inherit;
  background: transparent;
}
.search-box input:focus {
  outline: none;
}
.search-box button {
  width: 55px;
  border: none;
  background: var(--color-primary);
  color: #fff;
  cursor: pointer;
}

/* ACTIONS */
.header-actions {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-shrink: 0;
}
.header-action {
  position: relative;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.85rem;
  font-weight: 700;
}
.header-action b {
  position: absolute;
  top: -10px;
  right: -8px;
  background: var(--color-accent);
  border-radius: 50%;
  font-size: 0.7rem;
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.login-btn {
  background: var(--color-primary);
  color: #fff;
  padding: 10px 16px;
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
  font-weight: 700;
}
.user-box {
  position: relative;
}
.user-box button {
  border: none;
  background: var(--color-sand);
  padding: 10px 14px;
  border-radius: 20px;
  font-family: inherit;
}
.user-dropdown {
  position: absolute;
  top: 45px;
  right: 0;
  background: white;
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-md);
  border-radius: var(--radius);
  width: 170px;
  padding: 8px;
  display: flex;
  flex-direction: column;
  z-index: 60;
}
.user-dropdown a,
.user-dropdown button {
  padding: 10px;
  border: none;
  background: none;
  text-align: right;
  font-family: inherit;
  font-size: 0.86rem;
  border-radius: var(--radius-sm);
}
.user-dropdown a:hover,
.user-dropdown button:hover {
  background: var(--color-bg);
}

@media (max-width: 900px) {
  .top-bar {
    display: none;
  }
  .header-inner {
    height: auto;
    padding: 15px 0;
    flex-wrap: wrap;
  }
  .search-box {
    order: 3;
    width: 100%;
  }
}
</style>