import Vue from "vue";
import VueRouter from "vue-router";
import firebase from "firebase";
//import Dashboard from "../components/Dashboard.vue";
//import Login from ".../components/Login.vue";
//import Register from ".../components/Register.vue";

Vue.use(VueRouter);

const routes = [
	{
		path: "/",
		name: "Login",
		component: () =>
			import(/* webpackChunkName: "about" */ "../components/Login.vue"),
	},
	{
		path: "/dashboard",
		name: "Dashboard",
		// route level code-splitting
		// this generates a separate chunk (about.[hash].js) for this route
		// which is lazy-loaded when the route is visited.
		component: () =>
			import(/* webpackChunkName: "dashboard" */ "../components/Dashboard.vue"),
		meta: {
			authRequired: true,
		},
	},
	{
		path: "/register",
		name: "Register",
		// route level code-splitting
		// this generates a separate chunk (about.[hash].js) for this route
		// which is lazy-loaded when the route is visited.
		component: () =>
			import(/* webpackChunkName: "about" */ "../components/Register.vue"),
	},
];

const router = new VueRouter({
	routes,
});

export default router;

router.beforeEach((to, from, next) => {
	if (to.matched.some((record) => record.meta.authRequired)) {
		if (firebase.auth().currentUser) {
			next();
		} else {
			alert("You must be logged in to see this page");
			next({
				path: "/",
			});
		}
	} else {
		next();
	}
});
