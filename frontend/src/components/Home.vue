<template>
  <div>
    <div>
      <div class="user-info">
        <div class="avatar-container">
          <v-avatar :size="30" color="grey lighten-4">
            <img src="https://vuetifyjs.com/apple-touch-icon-180x180.png" alt="avatar" />
          </v-avatar>
        </div>
        <div class="full-name">{{userProfile.full_name}}</div>
      </div>
      <div>
        <v-tabs v-model="currentItem" fixed-tabs>
          <v-tab v-for="tab in tabs" :key="tab.id" :to="'/Home/'+tab.path">{{ tab.name }}</v-tab>
        </v-tabs>
        <v-content class="tab-content">
          <router-view />
        </v-content>
      </div>
    </div>
        <v-card-actions class="grey darken-3 footer">           
          <div class="right-footer">&copy;2019 — 
          <strong>Codex Soft</strong>
          </div>
          <div class="faq-footer" @click="dialog = true">FAQ</div>
        </v-card-actions>
    <FAQModal :visible="dialog" :onClose="() => dialog = false" />
  </div>
</template>

<script>
import * as authService from "../services/auth.service";
import Profile from "@/components/Profile/Profile.vue";
import AbsencesTable from "@/components/AbsencesTable.vue";
import FAQModal from "@/components/FAQModal.vue";

export default {
  components: {
    FAQModal
  },
  data: () => ({
    userProfile: {},
    currentItem: "",
    dialog: false,
    tabs: [
      {
        name: "Profile",
        path: "Profile",
        id: 1
      },
      {
        name: "Absences",
        path: "Absences",
        id: 2
      },
      {
        name: "Projects",
        path: "Projects",
        id: 3
      },
      {
        name: "Assessment",
        path: "Assessment",
        id: 4
      }
    ]
  }),
  created() {
    this.getUserProfile();
  },
  methods: {
    //make action
    getUserProfile() {
      authService
        .getUserById(this.$store.state.user.logedUserId)
        .then(data => {
          this.$store.dispatch("user/setUser", data);
          this.userProfile = data;
        })
        .catch(error => {
          console.log(error, "error");
        });
    }
  }
};
</script>

<style>
.user-info {
  margin: 40px;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
}
.full-name {
  font-size: 20px;
}
.avatar-container {
  margin-bottom: 20px;
}
.v-tabs__bar.theme--light {
  background: none;
  border-bottom: 1px solid grey;
}
.tab-content {
  padding: 0 !important;
}
.footer {
  width: 100%;
  display: flex;
  justify-content: space-between;
  position: fixed;
  bottom: 0;
}
.faq-footer {
  cursor: pointer
}
 .faq-footer:hover {
   text-decoration: underline;
 }


</style>
