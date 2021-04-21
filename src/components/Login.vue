<template>
  <v-app id="btrac">
    <v-form>
      <v-container>
        <v-card elevation="12" max-width="500" class="mx-auto mt-16">
          <v-card-title>
            <v-layout align-center justify-space-between>
              <h2 class="mb-4 ml-2 mt-2">trackerofbugs</h2>

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
              ></v-text-field>
            </v-col>
            <v-col class="mx-auto" cols="12" sm="10">
              <v-text-field
                class="mb-6"
                type="password"
                v-model="password"
                label="Password"
                required
              ></v-text-field>
              <v-btn color="primary" class="mr-4" @click="submit">
                login
                <v-icon right dark> mdi-lock </v-icon>
              </v-btn>

              <v-btn depressed @click="reg"> register </v-btn>
            </v-col>
          </v-col>
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

export default {
  mixins: [validationMixin],

  validations: {
    email: { required, email },
    //password: { required, password },
  },

  data: () => ({
    email: "",
    password: "",
  }),

  computed: {
    emailErrors() {
      const errors = [];
      if (!this.$v.email.$dirty) return errors;
      !this.$v.email.email && errors.push("Must enter a valid e-mail address");
      !this.$v.email.required && errors.push("E-mail is required");
      return errors;
    } /*
    passwordErrors() {
      const errors = [];
      if (!this.$v.password.$dirty) return errors;
      !this.$v.password.password && errors.push("Must enter a valid password");
      !this.$v.password.required && errors.push("Password is required");
      return errors;
    },*/,
  },

  methods: {
    ...mapMutations(["SET_TOKEN", "SET_USER"]),
    submit() {
      //this.$v.$touch();
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
          console.log(this.$store.state.user);
          alert("Successfully logged in");
          this.$router.push("/issues");
        })
        .catch((error) => {
          console.log(error);
        });
    },
    reg() {
      this.$router.push("/register");
    },
  },
};
</script>
