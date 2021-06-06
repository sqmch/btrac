import Vue from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import Vuelidate from "vuelidate";
import router from "./router";
import store from "./store";
import axios from "axios";

axios.defaults.baseURL = "http://localhost:1234";
axios.interceptors.response.use(
	function(response) {
		return response;
	},
	function(error) {
		//alert("Session expired, please login again.");
		router.push({ name: "Login" });
		return Promise.reject(error);
	}
);

Vue.use(router);
Vue.use(Vuelidate);
Vue.config.productionTip = false;

new Vue({
	mode: "history",
	vuetify,
	router,
	store,
	render: (h) => h(App),
}).$mount("#app");
