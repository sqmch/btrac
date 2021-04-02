import Vue from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import firebase from "firebase";
import Vuelidate from "vuelidate";
import router from "./router";

Vue.use(router);
Vue.use(Vuelidate);
Vue.config.productionTip = false;

var firebaseConfig = {
	apiKey: "AIzaSyCToU_iRBu-mJTuMG__yaJvPqsBilPbkPs",
	authDomain: "issuetracker-users.firebaseapp.com",
	projectId: "issuetracker-users",
	storageBucket: "issuetracker-users.appspot.com",
	messagingSenderId: "581835223520",
	appId: "1:581835223520:web:9c4d7d9860559a1421fb85",
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// 3. Create the router instance and pass the `routes` option
// You can pass in additional options here, but let's
// keep it simple for now.

new Vue({
	vuetify,
	router,
	render: (h) => h(App),
}).$mount("#app");
