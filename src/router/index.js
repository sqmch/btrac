import Vue from "vue";
import VueRouter from "vue-router";
import store from "../store";

Vue.use(VueRouter);

const routes = [
	{
		path: "/",
		name: "Home",
		component: () =>
			import(/* webpackChunkName: "about" */ "../components/Login.vue"),
		meta: {
			authRequired: true,
		},
	},
	{
		path: "/login",
		name: "Login",
		component: () =>
			import(/* webpackChunkName: "about" */ "../components/Login.vue"),
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
	{
		path: "/tasks",
		name: "Tasks",
		component: () =>
			import(/* webpackChunkName: "about" */ "../components/Tasks.vue"),
		meta: {
			authRequired: true,
		},
	},
	{
		path: "/projects",
		name: "Projects",
		component: () =>
			import(/* webpackChunkName: "about" */ "../components/Projects.vue"),
		meta: {
			authRequired: true,
		},
	},
	{
		path: "/timeline",
		name: "Timeline",
		component: () =>
			import(/* webpackChunkName: "about" */ "../components/Timeline.vue"),
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
			//alert("You must be logged in to see this page");
			next({
				path: "/login",
			});
		}
	} else {
		next();
	}
});
