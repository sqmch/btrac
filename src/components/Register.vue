<template>
  <form>
    <v-text-field
      v-model="email"
      :error-messages="emailErrors"
      label="E-mail"
      required
      @input="$v.email.$touch()"
      @blur="$v.email.$touch()"
    ></v-text-field>
    <v-text-field
      v-model="password"
      :error-messages="emailErrors"
      label="Password"
      required
      @input="$v.email.$touch()"
      @blur="$v.email.$touch()"
    ></v-text-field>

    <v-btn
      class="mr-4"
      @click="submit"
    >
      submit
    </v-btn>
    <v-btn @click="clear">
      clear
    </v-btn>
  </form>
</template>

<script>
  import { validationMixin } from 'vuelidate'
  import { required, maxLength, email } from 'vuelidate/lib/validators'
  import firebase from "firebase";

  export default {
    mixins: [validationMixin],

    validations: {
      name: { required, maxLength: maxLength(10) },
      email: { required, email },
    },

    data: () => ({
      email: '',
      password: '',
    }),

    computed: {
      emailErrors () {
        const errors = []
        if (!this.$v.email.$dirty) return errors
        !this.$v.email.email && errors.push('Must be valid e-mail')
        !this.$v.email.required && errors.push('E-mail is required')
        return errors
      },
    },

    methods: {
      submit () {
        this.$v.$touch()
        this.register()
      },
      clear () {
        this.$v.$reset()
        this.password = ''
        this.email = ''

      },
      register() {
    firebase
      .auth()
      .createUserWithEmailAndPassword(this.email, this.password)
      .then(() => {
        alert('Successfully registered! Please login.');
        this.$router.push('/');
      })
      .catch(error => {
        alert(error.message);
      });
  },
    },

  }
</script>
