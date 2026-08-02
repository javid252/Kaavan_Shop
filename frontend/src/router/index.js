import Vue from "vue";
import VueRouter from "vue-router";

import store from "@/store";

Vue.use(VueRouter);

const routes = [
  { path: "/", name: "home", component: () => import("@/views/Home.vue") },
  { path: "/products", name: "product-list", component: () => import("@/views/ProductList.vue") },
  { path: "/products/:slug", name: "product-detail", component: () => import("@/views/ProductDetail.vue") },
  { path: "/cart", name: "cart", component: () => import("@/views/Cart.vue") },
  {
    path: "/checkout",
    name: "checkout",
    component: () => import("@/views/Checkout.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/order-success/:id",
    name: "order-success",
    component: () => import("@/views/OrderSuccess.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/my-orders",
    name: "my-orders",
    component: () => import("@/views/MyOrders.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/Login.vue"),
    meta: { guestOnly: true },
  },
  {
    path: "/register",
    name: "register",
    component: () => import("@/views/Register.vue"),
    meta: { guestOnly: true },
  },
  {
    path: "/forgot-password",
    name: "forgot-password",
    component: () => import("@/views/ForgotPassword.vue"),
    meta: { guestOnly: true },
  },
  {
    path: "/reset-password/:uid/:token",
    name: "reset-password",
    component: () => import("@/views/ResetPassword.vue"),
    meta: { guestOnly: true },
  },
  {
    path: "/admin",
    component: () => import("@/views/admin/AdminLayout.vue"),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      { path: "", redirect: { name: "admin-dashboard" } },
      { path: "dashboard", name: "admin-dashboard", component: () => import("@/views/admin/AdminDashboard.vue") },
      { path: "products", name: "admin-products", component: () => import("@/views/admin/AdminProducts.vue") },
      {
        path: "products/new",
        name: "admin-product-new",
        component: () => import("@/views/admin/AdminProductForm.vue"),
      },
      {
        path: "products/:slug/edit",
        name: "admin-product-edit",
        component: () => import("@/views/admin/AdminProductForm.vue"),
      },
      { path: "orders", name: "admin-orders", component: () => import("@/views/admin/AdminOrders.vue") },
      { path: "users", name: "admin-users", component: () => import("@/views/admin/AdminUsers.vue") },
    ],
  },
  { path: "*", name: "not-found", component: () => import("@/views/NotFound.vue") },
];

const router = new VueRouter({
  mode: "history",
  routes,
  scrollBehavior() {
    return { x: 0, y: 0 };
  },
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters["auth/isAuthenticated"];
  const isAdmin = store.getters["auth/isAdmin"];

  if (to.meta.requiresAuth && !isAuthenticated) {
    return next({ name: "login", query: { redirect: to.fullPath } });
  }
  if (to.meta.requiresAdmin && !isAdmin) {
    return next({ name: "home" });
  }
  if (to.meta.guestOnly && isAuthenticated) {
    return next({ name: "home" });
  }
  next();
});

export default router;
