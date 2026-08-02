import Vue from "vue";
import Vuex from "vuex";

import auth from "./modules/auth";
import cart from "./modules/cart";
import platform from "./modules/platform";
import products from "./modules/products";
import vendor from "./modules/vendor";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: { auth, cart, products, platform, vendor },
  state: () => ({
    toasts: [],
    toastSeq: 0,
  }),
  mutations: {
    PUSH_TOAST(state, toast) {
      state.toastSeq += 1;
      state.toasts.push({ id: state.toastSeq, ...toast });
    },
    REMOVE_TOAST(state, id) {
      state.toasts = state.toasts.filter((t) => t.id !== id);
    },
  },
  actions: {
    notify({ commit }, { message, type = "success" }) {
      commit("PUSH_TOAST", { message, type });
    },
  },
});