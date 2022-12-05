<template>
  <div class="home">
    <chess-board :state="state"></chess-board>
  </div>
</template>

<script>
import {initialState} from "@/assets/js/StateLoader.js";
import ChessBoard from "@/components/ChessBoard.vue";

export default {
  components: {ChessBoard},
  data() {
    return {
      state: initialState
    }
  },
  computed: {},
  methods: {}
}
</script>