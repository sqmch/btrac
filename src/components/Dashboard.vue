<template>
  <v-app id="inspire">
    <v-navigation-drawer v-model="drawer" app>
      <v-sheet class="pa-4">
        <div>trackerofbugs</div>
      </v-sheet>

      <v-divider></v-divider>

      <v-list>
        <v-list-item v-for="[icon, text] in links" :key="icon" link>
          <v-list-item-icon>
            <v-icon>{{ icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ text }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-container class="py-8 px-6" fluid> </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  data: () => ({
    cards: ["Today", "Yesterday"],
    drawer: null,
    links: [
      ["mdi-folder-multiple", "Projects"],
      ["mdi-calendar-check", "Tasks"],
      ["mdi-chart-timeline", "Timeline"],
    ],
  }),
};
</script>
