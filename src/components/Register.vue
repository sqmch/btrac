<template>
  <v-app id="btrac">
    <v-form>
      <v-container>
        <v-card elevation="12" max-width="500" class="mx-auto mt-16">
          <v-card-title>
            <v-layout align-center justify-space-between>
              <h2 class="mb-4 ml-2 mt-2 text-decoration-overline">trvcker</h2>
              <h4 class="mb-4 ml-2 mt-2 font-weight-thin">register</h4>

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
              <v-text-field
                class="mb-6"
                type="password"
                :error-messages="repasswordErrors"
                v-model="repassword"
                label="Re-type password"
                required
              ></v-text-field>
              <v-btn color="primary" class="mr-4" @click="submit">
                register
                <v-icon right dark> mdi-account-plus </v-icon>
              </v-btn>

              <v-btn depressed @click="toLogin"> login </v-btn>
            </v-col>
          </v-col>
        </v-card>
      </v-container>
    </v-form>
  </v-app>
</template>


<script>
import { validationMixin } from "vuelidate";
import { required, email, minLength } from "vuelidate/lib/validators";
import axios from "axios";

export default {
  mixins: [validationMixin],

  validations: {
    email: { required, email },
    password: { required, minLength: minLength(6) },
  },

  data: () => ({
    email: "",
    password: "",
    repassword: "",
    type: null,

    elapse: null,
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
      !this.$v.password.required && passwordErrors.push("Password is required");
      return passwordErrors;
    },
    repasswordErrors() {
      const repasswordErrors = [];
      if (this.password !== this.repassword) {
        repasswordErrors.push("Passwords don't match");
      }

      return repasswordErrors;
    },
  },

  methods: {
    submit() {
      this.$v.$touch();
      this.register();
    },
    toLogin() {
      this.$router.push("/login");
    },
    register() {
      if (
        this.email.length > 5 &&
        this.password.length > 6 &&
        this.repassword === this.password
      ) {
        alert("Registered!");
        axios
          .post("http://127.0.0.1:1234/register", {
            email: this.email,
            password: this.password,
          })
          .then(() => {
            //this.toLogin();
          })
          .catch((error) => {
            console.log(error);
          })
          .then(() => {
            this.toLogin();
          });
      }
    },
    showAlert(type) {
      this.type = type;

      let timer = this.showAlert.timer;
      if (timer) {
        clearTimeout(timer);
      }
      this.showAlert.timer = setTimeout(() => {
        this.type = null;
      }, 3000);

      this.elapse = 1;
      let t = this.showAlert.t;
      if (t) {
        clearInterval(t);
      }

      this.showAlert.t = setInterval(() => {
        if (this.elapse === 3) {
          this.elapse = 0;
          clearInterval(this.showAlert.t);
        } else {
          this.elapse++;
        }
      }, 1000);
    },
  },
};
</script>
