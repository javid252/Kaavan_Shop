import api from "@/services/api";

export default {
  namespaced: true,
  state: () => ({
    multivendorEnabled: false,
    loaded: false,
  }),
  getters: {
    multivendorEnabled: (state) => state.multivendorEnabled,
  },
  mutations: {
    SET_SETTINGS(state, { multivendor_enabled }) {
      state.multivendorEnabled = multivendor_enabled;
      state.loaded = true;
    },
  },
  actions: {
    async fetchSettings({ commit, state }) {
      if (state.loaded) return;
      try {
        const { data } = await api.get("/settings/");
        commit("SET_SETTINGS", data);
      } catch (e) {
        commit("SET_SETTINGS", { multivendor_enabled: false });
      }
    },
  },
};