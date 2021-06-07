import Vue from "vue";
import Vuetify from "vuetify/lib/framework";

Vue.use(Vuetify);

export default new Vuetify({
	theme: {
		dark: true,
		themes: {
			dark: {
				primary: "#65499c",
				secondary: "#c7a4ff",
				accent: "#f1c40f",
				error: "#e74c3c",
			},
		},
	},
});
