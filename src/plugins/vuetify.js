import Vue from "vue";
import Vuetify from "vuetify/lib/framework";

Vue.use(Vuetify);

export default new Vuetify({
	theme: {
		dark: true,
		themes: {
			dark: {
				primary: "#8e44ad",
				secondary: "#e67e22",
				accent: "#f1c40f",
				error: "#e74c3c",
			},
		},
	},
});
