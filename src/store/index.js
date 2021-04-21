import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";
import auth from "./modules/auth";

Vue.use(Vuex);

export default new Vuex.Store({
	state: {},
	getters: { isAuthenticated: (state) => !!state.token },
	mutations: {
		SAVE_TOKEN(state, payload) {
			state.token = payload.token;
		},
		REMOVE_TOKEN(state) {
			state.token = null;
		},
		SET_USER(state, payload) {
			state.user = payload.email;
		},
		REMOVE_USER(state) {
			state.user = "";
		},
	},
	plugins: [createPersistedState()],
	modules: auth,
});
