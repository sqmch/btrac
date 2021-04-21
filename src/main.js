import Vue from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import Vuelidate from "vuelidate";
import router from "./router";
import store from "./store";
import axios from "axios";

Vue.use(router);
Vue.use(Vuelidate);
Vue.config.productionTip = false;

const token = store.token;
if (token) {
	axios.defaults.headers.common["Authorization"] = token;
}

new Vue({
	mode: "history",
	vuetify,
	router,
	store,
	render: (h) => h(App),
}).$mount("#app");
