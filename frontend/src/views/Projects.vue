<template>
  <div class="projects">
    <Projects />
  </div>
</template>


<script>
import Projects from "@/components/ProjectsTable.vue";

export default {
  
  name: "projects",
  components: {
    Projects
  },
}
</script>

<style>
  .projects {
    padding: 40px 100px;
  }
</style>
