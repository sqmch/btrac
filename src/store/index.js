import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";
import auth from "./modules/auth";

Vue.use(Vuex);
const state = {
	project_id: null,
};
const getters = {
	getUser: (state) => {
		return state.user
	},
};
const mutations = {
	SET_TOKEN(state, payload) {
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
	SET_PROJECT_ID(state, id) {
		state.project_id = id;
	},
};

export default new Vuex.Store({
	strict: false,
	state,
	getters,
	mutations,
	plugins: [createPersistedState()],
	modules: { auth },
});
