<template>
  <div class="assessments">
    <CurrentAssessment />
  </div>
</template>


<script>
import CurrentAssessment from "@/components/Assessment/CurrentAssessment.vue";

export default {
  
  name: "currentAssessment",
  components: {
    CurrentAssessment
  },
}
</script>

<style>
  .assessments {
    padding: 40px 100px;
  }
</style>
