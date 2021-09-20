<template>
  <v-app id="inspire">
    <v-navigation-drawer app prominent>
      <v-sheet class="pa-4">
        <div class="headline text-decoration-overline">trvcker</div>
      </v-sheet>

      <v-divider></v-divider>

      <v-list>
        <v-list-item v-for="[icon, text, path] in links" :key="icon" link>
          <v-list-item-icon>
            <v-icon>{{ icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <router-link
              style="text-decoration: none; color: inherit; display: block"
              :to="{ path: path }"
            >
              <v-list-item-title>{{ text }}</v-list-item-title>
            </router-link>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <template v-slot:append>
        <div class="text-center"></div>

        <div class="h3 mx-4 text-center">
          {{ $store.state.user }}
        </div>
        <div class="pa-2">
          <v-btn block @click="logout"> Logout </v-btn>
        </div>
      </template>
    </v-navigation-drawer>

    <v-main>
      <v-container class="py-0 px-0" fluid> <router-view /></v-container>
    </v-main>
    <v-footer padless>
      <v-col class="text-center" cols="12">
        <v-icon size="24px" @click="darkMode">mdi-lightbulb</v-icon>

        <v-icon size="24px" @click="ghub">mdi-github</v-icon>

        <!-- {{ new Date().getFullYear() }} — <strong>trackerofbugs</strong>-->
      </v-col>
    </v-footer>
  </v-app>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  data: () => ({
    links: [["mdi-folder-multiple", "Projects", "/projects"]],
    user: null,
  }),
  methods: {
    ...mapGetters(["getUser"]),

    logout() {
      this.$store.commit("REMOVE_TOKEN");
      this.$store.commit("REMOVE_USER");
      this.$router.push("/login");
      this.user = "";
    },
    ghub() {
      window.open("https://github.com/sqmch/trvcker", "_blank");
    },
    darkMode() {
      this.$vuetify.theme.dark = !this.$vuetify.theme.dark;
    },
  },
};
</script>
