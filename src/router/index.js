import Vue from "vue";
import VueRouter from "vue-router";
import store from "../store";

Vue.use(VueRouter);

const routes = [
	{
		path: "/",
		name: "Projects",
		component: () => import("../components/Projects.vue"),
		meta: {
			authRequired: true,
		},
	},
	{
		path: "/login",
		name: "Login",
		component: () => import("../components/Login.vue"),
	},

	{
		path: "/register",
		name: "Register",
		component: () => import("../components/Register.vue"),
	},
	{
		path: "/projects",
		name: "Projects",
		component: () => import("../components/Projects.vue"),
		meta: {
			authRequired: true,
		},
	},
	{
		path: "/projects/issues",
		name: "Issues",
		component: () => import("../components/Issues.vue"),
		meta: {
			authRequired: true,
		},
	},
];

const router = new VueRouter({
	routes,
});

export default router;

router.beforeEach((to, from, next) => {
	if (to.matched.some((record) => record.meta.authRequired)) {
		if (store.state.user) {
			next();
		} else {
			next({
				path: "/login",
			});
		}
	} else {
		next();
	}
});
