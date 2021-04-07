<template>
  <v-app id="inspire">
    <v-navigation-drawer app>
      <v-sheet class="pa-4">
        <div class="headline">trackerofbugs</div>
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
    </v-navigation-drawer>

    <v-main>
      <v-container class="py-0 px-0" fluid> <router-view /></v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  data: () => ({
    links: [
      ["mdi-folder-multiple", "Projects", "/projects"],
      ["mdi-calendar-check", "Tasks", "/tasks"],
      ["mdi-chart-timeline", "Timeline", "/timeline"],
    ],
  }),
  methods: {},
};
</script>
