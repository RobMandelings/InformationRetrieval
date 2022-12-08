<template>
  <div class="flex flex-row space-x-3">
    <div class="flex flex-col space-y-2">
      <chess-board style="width: 500px" :state="state"></chess-board>
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
      <div class="border-2 h-full w-full space-y-2">
        <template v-for="document in retrievedDocuments">
          <div class="flex flex-col">
            <h3 class="text-lg">{{ document.game._header['Event'] }}, id: {{ document.id }}</h3>
            <chess-board style="width: 300px" :state="document.boardStates[document.move_nr - 1]"></chess-board>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import {initialState, encodeState, decodeState} from "@/assets/js/StateLoader.js";
import {Chess} from 'chess.js';
import ChessBoard from "@/components/ChessBoard.vue";
import axios from 'axios';

export default {
  components: {ChessBoard},
  data() {
    return {
      state: initialState,
      searching: false,
      retrievedDocuments: []
    }
  },
  computed: {},
  methods: {

    getState(chess) {
      return decodeState(chess.fen());
    },

    async submitSearch() {
      this.searching = true;
      const stateEncoding = encodeState(this.state);
      try {
        const result = await axios(
            {
              method: 'get',
              url: `http://127.0.0.1:5000/api/search?state=${encodeURIComponent(stateEncoding)}`
            });

        const documents = result.data.results;
        documents.forEach(document => {
          const game = new Chess();
          game.loadPgn(document['game']);
          const history = game.history()
          const newGame = new Chess()

          let boardStates = []

          for (let i = 0; i < document.move_nr; i++) {
            newGame.move(history[i])
            boardStates.push(decodeState(newGame.fen()))
          }
          document['game'] = game;
          document['boardStates'] = boardStates;
        });
        this.retrievedDocuments = documents;
      } catch (e) {
        console.log(e);
      }
      // TODO show results
      this.searching = false;
    }
  }
}
</script>