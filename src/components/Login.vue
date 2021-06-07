<template>
  <v-app id="btrac">
    <v-form>
      <v-container>
        <v-card elevation="12" max-width="500" class="mx-auto mt-16">
          <v-card-title>
            <v-layout align-center justify-space-between>
              <h2 class="mb-4 ml-2 mt-2 text-decoration-overline">trvcker</h2>
              <h4 class="mb-4 ml-2 mt-2 font-weight-thin">login</h4>
              <v-flex> </v-flex>
            </v-layout>
          </v-card-title>
          <v-col>
            <v-col class="mx-auto" cols="12" sm="10">
              <v-text-field
                v-model="email"
                :error-messages="emailErrors"
                label="E-mail"
                required
                @input="$v.email.$touch()"
                @blur="$v.email.$touch()"
              ></v-text-field>
            </v-col>
            <v-col class="mx-auto" cols="12" sm="10">
              <v-text-field
                class="mb-6"
                type="password"
                :error-messages="passwordErrors"
                v-model="password"
                label="Password"
                required
                @input="$v.password.$touch()"
                @blur="$v.password.$touch()"
              ></v-text-field>
              <v-btn color="primary" class="mr-4" @click="submit">
                login
                <v-icon right dark> mdi-login </v-icon>
              </v-btn>

              <v-btn depressed @click="toRegister"> register </v-btn>
            </v-col>
          </v-col>
          <!-- experimenting with drag and drop
          <v-expansion-panels>
            <draggable v-model="items" class="row">
              <v-expansion-panel v-for="item in items" :key="item.id">
                <v-expansion-panel-header>
                  {{ item.title }}
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
                  do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                  Ut enim ad minim veniam, quis nostrud exercitation ullamco
                  laboris nisi ut aliquip ex ea commodo consequat.
                </v-expansion-panel-content>
              </v-expansion-panel>
            </draggable>
          </v-expansion-panels>
           -->
        </v-card>
      </v-container>
    </v-form>
  </v-app>
</template>

<script>
import { validationMixin } from "vuelidate";
import { required, email } from "vuelidate/lib/validators";
import axios from "axios";
import { mapMutations } from "vuex";
//import draggable from "vuedraggable";

export default {
  mixins: [validationMixin],
  //components: {
  //draggable,

  //},
  validations: {
    email: { required, email },
    password: { required },
  },

  data: () => ({
    items: [
      { id: 1, title: "abc" },
      { id: 3, title: "ghi" },
      { id: 4, title: "jkl" },
      { id: 5, title: "mno" },
      { id: 2, title: "def" },
    ],
    alert: true,
    email: "",
    password: "",
  }),

  computed: {
    emailErrors() {
      const emailErrors = [];
      if (!this.$v.email.$dirty) return emailErrors;
      !this.$v.email.email &&
        emailErrors.push("Must enter a valid e-mail address");
      !this.$v.email.required && emailErrors.push("E-mail is required");
      return emailErrors;
    },
    passwordErrors() {
      const passwordErrors = [];
      if (!this.$v.password.$dirty) return passwordErrors;
      !this.$v.password.password &&
        passwordErrors.push("Must enter a valid password");
      !this.$v.password.required && passwordErrors.push("Password is required");
      return passwordErrors;
    },
  },

  methods: {
    ...mapMutations(["SET_TOKEN", "SET_USER"]),
    submit() {
      this.$v.$touch();
      this.login();
    },
    clear() {
      this.$v.$reset();
      this.name = "";
      this.email = "";
      this.select = null;
      this.checkbox = false;
    },
    async login() {
      await axios
        .post("http://127.0.0.1:1234/auth", {
          email: this.email,
          password: this.password,
        })
        .then((response) => {
          this.SET_TOKEN({
            token: response.data.token,
          });
          this.SET_USER({ email: this.email });
          this.$router.push("/projects");
        })
        .catch((error) => {
          console.log(error);
        });
    },
    toRegister() {
      this.$router.push("/register");
    },
  },
};
</script>
