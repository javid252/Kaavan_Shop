import api from "@/services/api";

export default {
  namespaced: true,

  state: () => ({
    categories: [],
  }),

  getters: {
    categories: (state) => state.categories,
  },

  mutations: {
    SET_CATEGORIES(state, categories) {
      state.categories = categories;
    },
  },

  actions: {
    async fetchCategories({ commit, state }) {
      if (state.categories.length) return state.categories;
      const { data } = await api.get("/categories/");
      const categories = data.results || data; // اندپوینت صفحه‌بندی‌شده است
      commit("SET_CATEGORIES", categories);
      return categories;
    },
  },
};