import api from "@/services/api";

function loadCart() {
  try {
    const raw = localStorage.getItem("kaavan_cart");
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function persist(items) {
  localStorage.setItem("kaavan_cart", JSON.stringify(items));
}

function sameLine(a, productId, variantId) {
  return a.product_id === productId && (a.variant_id || null) === (variantId || null);
}

export default {
  namespaced: true,
  state: () => ({
    // هر آیتم: { product_id, variant_id, quantity, name, image, price, variant_label }
    items: loadCart(),
    validated: null, // نتیجه آخرین اعتبارسنجی سمت سرور (قیمت/موجودی واقعی)
    validating: false,
  }),
  getters: {
    itemCount: (state) => state.items.reduce((sum, i) => sum + i.quantity, 0),
    localSubtotal: (state) => state.items.reduce((sum, i) => sum + i.price * i.quantity, 0),
    isEmpty: (state) => state.items.length === 0,
  },
  mutations: {
    ADD_ITEM(state, item) {
      const existing = state.items.find((i) => sameLine(i, item.product_id, item.variant_id));
      if (existing) {
        existing.quantity += item.quantity;
      } else {
        state.items.push(item);
      }
      persist(state.items);
    },
    SET_QUANTITY(state, { product_id, variant_id, quantity }) {
      const existing = state.items.find((i) => sameLine(i, product_id, variant_id));
      if (existing) {
        existing.quantity = quantity;
        if (existing.quantity <= 0) {
          state.items = state.items.filter((i) => i !== existing);
        }
      }
      persist(state.items);
    },
    REMOVE_ITEM(state, { product_id, variant_id }) {
      state.items = state.items.filter((i) => !sameLine(i, product_id, variant_id));
      persist(state.items);
    },
    CLEAR_CART(state) {
      state.items = [];
      persist(state.items);
    },
    SET_VALIDATED(state, payload) {
      state.validated = payload;
    },
    SET_VALIDATING(state, value) {
      state.validating = value;
    },
  },
  actions: {
    addItem({ commit }, item) {
      commit("ADD_ITEM", item);
    },
    setQuantity({ commit }, payload) {
      commit("SET_QUANTITY", payload);
    },
    removeItem({ commit }, payload) {
      commit("REMOVE_ITEM", payload);
    },
    clearCart({ commit }) {
      commit("CLEAR_CART");
    },
    async validateCart({ commit, state }) {
      if (state.items.length === 0) {
        commit("SET_VALIDATED", { items: [], subtotal: 0, has_issue: false });
        return;
      }
      commit("SET_VALIDATING", true);
      try {
        const { data } = await api.post("/cart/validate/", {
          items: state.items.map((i) => ({
            product_id: i.product_id,
            variant_id: i.variant_id || null,
            quantity: i.quantity,
          })),
        });
        commit("SET_VALIDATED", data);
        return data;
      } finally {
        commit("SET_VALIDATING", false);
      }
    },
  },
};
