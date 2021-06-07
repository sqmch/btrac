import Vue from "vue";
import Vuetify from "vuetify/lib/framework";
import colors from "vuetify/lib/util/colors";

Vue.use(Vuetify);

export default new Vuetify({
	theme: {
		dark: true,
		themes: {
			dark: {
				primary: "#673ab7",
				secondary: colors.grey.darken1,
				accent: colors.shades.black,
				error: colors.red,
			},
			light: {
				primary: "#7e57c2",
			},
		},
	},
});
