import Vue from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
//import firebase from "firebase";
import Vuelidate from "vuelidate";
import router from "./router";
import Vuex from "vuex";

Vue.use(Vuex);
Vue.use(router);
Vue.use(Vuelidate);
Vue.config.productionTip = false;
const store = new Vuex.Store({
	state: {
		token: "",
	},
	mutations: {
		saveToken(state, payload) {
			state.token = payload.token;
			console.log("token: " + state.token);
		},
	},
});

/*var firebaseConfig = {
	apiKey: "AIzaSyCToU_iRBu-mJTuMG__yaJvPqsBilPbkPs",
	authDomain: "issuetracker-users.firebaseapp.com",
	projectId: "issuetracker-users",
	storageBucket: "issuetracker-users.appspot.com",
	messagingSenderId: "581835223520",
	appId: "1:581835223520:web:9c4d7d9860559a1421fb85",
};*/
// Initialize Firebase
//firebase.initializeApp(firebaseConfig);

new Vue({
	mode: "history",
	vuetify,
	router,
	store: store,
	render: (h) => h(App),
}).$mount("#app");
