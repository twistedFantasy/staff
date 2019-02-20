<template>
  <div>
    <div class="user-info">
      <div class="avatar-container">
        <v-avatar
          :size="30"
          color="grey lighten-4"
        >
          <img src="https://vuetifyjs.com/apple-touch-icon-180x180.png" alt="avatar">
        </v-avatar>
      </div>
      <div class="full-name">{{userProfile.full_name}}</div>
    </div>
    <div>
      <v-tabs
        v-model="currentItem"
        fixed-tabs
      >
        <v-tab
          v-for="tab in tabs"
          :key="tab.id"
          :href="'#tab-' + tab.name"
        >
          {{ tab.name }}
        </v-tab>
      </v-tabs>
      <v-tabs-items v-model="currentItem">
        <v-tab-item
          v-for="tab in tabs"
          :key="tab.id"
          :value="'tab-' + tab.name"
        >
          <v-card flat>
            <div v-if="tab.name === 'Profile'"><Profile/></div>
            <div v-if="tab.name === 'Absences'"><AbsencesTable/></div>
          </v-card>
        </v-tab-item>
      </v-tabs-items>
    </div>
  </div>
</template>

<script>
  import * as authService from '../services/auth.service'
  import Profile from "@/components/Profile.vue";
  import AbsencesTable from "@/components/AbsencesTable.vue";

  export default {
     components: {
      Profile,
      AbsencesTable,
    },
    data: () => ({
      userProfile: {},
      currentItem: 'Profile',
      tabs: [
        {
          name: 'Profile',
          id: 1,
        },
        {
          name: 'Absences',
          id: 2,
        },
        {
          name: 'Projects',
           id: 3,
        },
        {
          name: 'Key skills',
           id: 4,
        },
         {
          name: 'Assessment',
           id: 5,
        },
      ],
    }),
    created () {
      this.getUserProfile();
    },
    methods: {
      getUserProfile() {
        authService.getUserById(this.$store.state.user.logedUserId).then(
          data => {
              this.$store.dispatch('user/setUser', data)
               this.userProfile = data;
          },
          error => {
            console.log(error, 'error')
          }
        );
      },
    },
  }
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
  .v-tabs__bar.theme--light{
    background: none;
    border-bottom: 1px solid grey;
  }

</style>
