import api from "@/services/api";

export default {
  namespaced: true,
  state: () => ({
    profile: null,
    checked: false,
  }),
  getters: {
    isVendor: (state) => !!state.profile,
    isApprovedVendor: (state) => !!(state.profile && state.profile.status === "approved"),
    vendorStatus: (state) => (state.profile ? state.profile.status : null),
    profile: (state) => state.profile,
  },
  mutations: {
    SET_PROFILE(state, profile) {
      state.profile = profile;
      state.checked = true;
    },
    CLEAR(state) {
      state.profile = null;
      state.checked = false;
    },
  },
  actions: {
    async fetchMe({ commit }) {
      try {
        const { data } = await api.get("/vendors/me/");
        commit("SET_PROFILE", data);
      } catch (e) {
        commit("SET_PROFILE", null);
      }
    },
    async apply({ dispatch }, payload) {
      await api.post("/vendors/apply/", payload);
      await dispatch("fetchMe");
    },
    async updateProfile({ dispatch }, formData) {
      await api.patch("/vendors/me/", formData);
      await dispatch("fetchMe");
    },
    clear({ commit }) {
      commit("CLEAR");
    },
  },
};