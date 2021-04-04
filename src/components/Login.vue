<template>
  <v-app id="btrac">
    <v-form>
      <v-container>
        <v-card elevation="2" max-width="500" class="mx-auto mt-12">
          <v-card-title>
            <v-layout align-center justify-space-between>
              <h2 class="mb-4 ml-2 mt-2">bugtracker</h2>

              <v-flex> </v-flex>
            </v-layout>
          </v-card-title>
          <!--<v-divider></v-divider>-->
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
                v-model="password"
                label="Password"
                required
                @input="$v.password.$touch()"
                @blur="$v.password.$touch()"
              ></v-text-field>
              <v-btn color="primary" class="mr-4" @click="submit">
                login
                <v-icon right dark> mdi-lock </v-icon>
              </v-btn>

              <v-btn depressed @click="register"> register </v-btn>
            </v-col>
          </v-col>
        </v-card>
      </v-container>
    </v-form>
  </v-app>
</template>

<script>
import { validationMixin } from "vuelidate";
import { required, maxLength, email } from "vuelidate/lib/validators";
import firebase from "firebase";

export default {
  mixins: [validationMixin],

  validations: {
    name: { required, maxLength: maxLength(10) },
    email: { required, email },
  },

  data: () => ({
    email: "",
    password: "",
  }),

  computed: {
    emailErrors() {
      const errors = [];
      if (!this.$v.email.$dirty) return errors;
      !this.$v.email.email && errors.push("Must be valid e-mail");
      !this.$v.email.required && errors.push("E-mail is required");
      return errors;
    },
  },

  methods: {
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
    login() {
      firebase
        .auth()
        .signInWithEmailAndPassword(this.email, this.password)
        .then(() => {
          alert("Successfully logged in");
          this.$router.push("/dashboard");
        })
        .catch((error) => {
          alert(error.message);
        });
    },
  },
};
</script>
