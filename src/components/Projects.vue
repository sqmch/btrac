<template>
  <div>
    <v-card>
      <v-data-table
        :search="search"
        item-key="title"
        :loading="projectsLoading"
        loading-text="Loading... Please wait"
        :headers="headers"
        :items="projects"
        @click:row="handleRowClick"
        sort-by="title"
      >
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Projects</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-spacer></v-spacer>
            <v-spacer></v-spacer>
            <v-spacer></v-spacer>
            <v-spacer></v-spacer>
            <v-spacer></v-spacer>

            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Search"
              single-line
              hide-details
            ></v-text-field>
            <v-divider class="mx-4" inset vertical></v-divider>
            <v-dialog v-model="dialog" max-width="500px">
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  color="primary"
                  dark
                  class="mb-2"
                  v-bind="attrs"
                  v-on="on"
                >
                  Add Project
                </v-btn>
              </template>
              <draggable v-model="projects" class="row">
                <v-card>
                  <v-card-title>
                    <span class="headline">{{ formTitle }}</span>
                  </v-card-title>

                  <v-card-text>
                    <v-container>
                      <v-text-field
                        v-model="editedItem.title"
                        label="Title"
                      ></v-text-field>
                    </v-container>
                  </v-card-text>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="primary " text @click="close"> Cancel </v-btn>
                    <v-btn color="primary " text @click="save"> Save </v-btn>
                  </v-card-actions>
                </v-card>
              </draggable>
            </v-dialog>
            <v-dialog v-model="dialogDelete" max-width="500px">
              <v-card>
                <v-card-title class="headline"
                  >Are you sure you want to delete this project?</v-card-title
                >
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="primary " text @click="closeDelete"
                    >Cancel</v-btn
                  >
                  <v-btn color="primary " text @click="deleteItemConfirm"
                    >OK</v-btn
                  >
                  <v-spacer></v-spacer>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-toolbar>
        </template>
        <template v-slot:[`item.actions`]="{ item }">
          <v-icon small class="mr-2" @click.stop="editProject(item)">
            mdi-pencil
          </v-icon>
          <v-icon small @click.stop="deleteItem(item)"> mdi-delete </v-icon>
        </template>
      </v-data-table>
      <v-spacer></v-spacer>
    </v-card>
    <v-card class="d-flex pa-6 my-2 mx-2" outlined tile>
      <v-expansion-panels transition="slide-x-transition" focusable multiple>
        <draggable v-model="projects" class="row">
          <v-expansion-panel v-for="project in projects" :key="project.id">
            <v-expansion-panel-header>
              {{ project.title }}
            </v-expansion-panel-header>
            <v-expansion-panel-content
              ><div class="py-4">Some sort of a project description.</div>
              <v-btn
                color="primary"
                class="my-2"
                @click="openProject(project.id)"
                ><v-icon left> mdi-format-list-checks </v-icon>Open</v-btn
              >
              <v-btn text class="my-2 mx-2"
                ><v-icon left> mdi-delete </v-icon>Delete</v-btn
              >
            </v-expansion-panel-content>
          </v-expansion-panel>
        </draggable>
      </v-expansion-panels></v-card
    >
  </div>
</template>
<script>
import axios from "axios";
import draggable from "vuedraggable";

import { mapMutations } from "vuex";
export default {
  components: {
    draggable,
  },
  data: () => ({
    items: [
      { id: 1, title: "abc" },
      { id: 3, title: "ghi" },
      { id: 4, title: "jkl" },
      { id: 5, title: "mno" },
      { id: 2, title: "def" },
    ],
    search: "",
    projectsLoading: false,
    dialog: false,
    dialogDelete: false,
    headers: [
      {
        text: "Title",
        align: "start",
        value: "title",
      },
      { text: "Edit / Delete", value: "actions", sortable: false },
    ],
    projects: [],
    editedIndex: -1,
    editedItem: {
      title: "",
    },
    defaultItem: {
      title: "",
    },
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "Add Project" : "Edit Project";
    },
  },

  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
  },

  created() {
    this.getProjects();
  },

  methods: {
    ...mapMutations(["SET_PROJECT_ID"]),
    getProjects() {
      this.projectsLoading = true;
      axios
        .get("/projects", {
          headers: { Authorization: "Bearer " + this.$store.state.token },
        })
        .then((response) => {
          this.projects = response.data.Projects;
          this.projectsLoading = false;
        })
        .catch((e) => {
          console.log(e);
        });
    },
    addProject() {
      axios
        .post("/projects", this.editedItem, {
          headers: { Authorization: "Bearer " + this.$store.state.token },
        })
        .then(
          (response) => {
            console.log(response);
          },
          (error) => {
            console.log(error);
          }
        );
    },
    putProject() {
      axios({
        method: "put",
        url: `/projects/${this.editedItem.id}`,
        headers: { Authorization: "Bearer " + this.$store.state.token },
        data: this.editedItem,
      }).catch((e) => {
        console.log(e);
      });
    },

    editProject(item) {
      this.editedIndex = this.projects.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    deleteItem(item) {
      this.editedIndex = this.projects.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      this.projects.splice(this.editedIndex, 1);
      axios
        .delete(`/projects/${this.editedItem.id}`, {
          headers: { Authorization: "Bearer " + this.$store.state.token },
        })
        .catch((e) => {
          console.log(e);
        });
      this.closeDelete();
    },

    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.projects[this.editedIndex], this.editedItem);
        this.putProject();
      } else {
        this.projects.push(this.editedItem);
        this.addProject();
      }
      this.close();
    },
    handleRowClick(row) {
      this.SET_PROJECT_ID(row.id);
      this.$router.push("/projects/issues");
    },
    openProject(id) {
      this.SET_PROJECT_ID(id);
      this.$router.push("/projects/issues");
    },
  },
};
</script>
