<template>
  <div class="flex flex-row space-x-3">
    <div class="flex flex-col space-y-2">
      <chess-board :state="state"></chess-board>
      <div class="flex flex-row justify-between">
        <button class="p-1 text-white bg-gray-500 hover:bg-gray-200 transition">Load FEN...</button>
        <button @click.prevent.stop="submitSearch"
                class="p-1 text-white bg-green-700 hover:bg-green-500 transition disabled:bg-red-200"
                :disabled="searching"
        >
          Search
        </button>
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
import axios from 'axios';

export default {
  components: {ChessBoard},
  data() {
    return {
      state: initialState,
      searching: false
    }
  },
  computed: {},
  methods: {
    async submitSearch() {
      this.searching = true;
      const stateEncoding = 'hi';
      try {
        const result = await axios(
            {
              method: 'get',
              url: `http://127.0.0.1:5000/api/search/${stateEncoding}`,
              timeout: 2000
            });

        console.log(`result is: ${result.data.msg}`)
      } catch (e) {
        console.log(e);
      }
      // TODO show results
      this.searching = false;
    }
  }
}
</script>