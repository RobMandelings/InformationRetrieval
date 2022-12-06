<template>
  <div class="flex flex-row space-x-3">
    <div class="flex flex-col space-y-2">
      <chess-board :state="state"></chess-board>
      <div class="flex flex-row justify-between">
        <button class="p-1 text-white bg-gray-500 hover:bg-gray-200 transition">Load FEN...</button>
        <button class="p-1 text-white bg-green-700 hover:bg-green-500 transition">Search</button>
      </div>
    </div>
    <div class="flex flex-col" style="min-width: 500px">
      <h1 class="text-2xl">Search results</h1>
      <div class="border-2 h-full w-full">

      </div>
    </div>
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