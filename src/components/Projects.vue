<template>
  <div>
    <v-card>
      <v-toolbar flat>
        <v-toolbar-title>Projects</v-toolbar-title>
        <v-divider class="mx-8" inset vertical></v-divider>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        <v-dialog v-model="dialog" max-width="500px">
          <template v-slot:activator="{ on, attrs }">
            <v-btn large color="primary" dark class="" v-bind="attrs" v-on="on">
              <v-icon class="mr-2">mdi-plus</v-icon>Add Project
            </v-btn>
          </template>
          <v-card class="pa-4">
            <v-card-title>
              <span class="headline">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
              <v-container class="my-4">
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
        </v-dialog>
        <v-dialog v-model="dialogDelete" max-width="500px">
          <v-card class="pa-4">
            <v-card-title class="headline">Delete</v-card-title>
            <v-card-text
              >Are you sure you want to delete this project?</v-card-text
            >
            <v-card-actions>
              <v-spacer></v-spacer>

              <v-btn class="mx-4" color="primary " text @click="closeDelete"
                >Cancel</v-btn
              >
              <v-btn
                class="mx-4"
                color="primary "
                text
                @click="deleteItemConfirm"
                >Delete</v-btn
              >
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </v-card>
    <v-expansion-panels flat focusable class="pa-6 my-2 mx-2" elevation="0">
      <draggable shaped v-model="projects" class="row">
        <v-expansion-panel flat v-for="project in projects" :key="project.id">
          <v-expansion-panel-header>
            {{ project.title }}
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <div class="py-4">Some sort of a project description.</div>
            <v-btn
              large
              color="primary"
              class="my-2"
              @click="openProject(project.id)"
              ><v-icon left> mdi-format-list-checks </v-icon>Open</v-btn
            >
            <v-btn
              icon
              class="my-2 mx-2 float-right"
              @click="deleteItem(project)"
              ><v-icon> mdi-delete </v-icon></v-btn
            >
            <v-btn
              icon
              class="my-2 mx-2 float-right"
              @click="editProject(project)"
              ><v-icon> mdi-pencil </v-icon></v-btn
            >
          </v-expansion-panel-content>
        </v-expansion-panel>
      </draggable>
    </v-expansion-panels>
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
            this.getProjects();
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
        this.SET_PROJECT_ID(this.editedIndex);
      }
      this.close();
    },
    openProject(id) {
      console.log("project id at project open - ", id);
      this.SET_PROJECT_ID(id);
      this.$router.push("/projects/issues");
    },
  },
};
</script>
