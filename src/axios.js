import axios from "axios";

axios.defaults.baseURL = "http://localhost:1234/";
axios.defaults.headers.common["Authorization"] =
	"Bearer " + this.$store.state.token;
