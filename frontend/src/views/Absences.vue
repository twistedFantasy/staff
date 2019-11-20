<template>
  <div class="absences">
    <AbsencesTable />
  </div>
</template>


<script>
import AbsencesTable from "@/components/Absence/AbsencesTable.vue";

export default {
  name: "absencesTable",
  components: {
    AbsencesTable
  },
}
</script>

<style>
  .absences {
    padding: 40px 100px;
  }
</style>
