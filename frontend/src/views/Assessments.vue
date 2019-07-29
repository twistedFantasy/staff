<template>
  <div class="assessments">
    <Assessments />
  </div>
</template>


<script>
import Assessments from "@/components/AssessmentsTable.vue";

export default {
  
  name: "projects",
  components: {
    Assessments
  },
}
</script>

<style>
  .assessments {
    padding: 40px 100px;
  }
</style>
