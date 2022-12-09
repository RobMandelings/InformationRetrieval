<template>
  <div class="flex flex-row space-x-3">
    <div class="flex flex-col space-y-2 w-1/2">
      <chess-board class="w-full h-full" :state="state"></chess-board>
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
    <div class="flex flex-col w-1/2">
      <h1 class="text-2xl">Search results</h1>
      <div class="border-2 max-h-full w-full space-y-2" style="min-height: 300px; min-width: 300px">
        <!--        <chess-game-viewer v-if="testDocument" :document-data="testDocument"></chess-game-viewer>-->
        <template v-for="document in retrievedDocuments">
          <chess-game-viewer :document-data="document"></chess-game-viewer>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import {initialState, testGame, encodeState, decodeState} from "@/assets/js/StateLoader.js";
import {Chess} from 'chess.js';
import ChessBoard from "@/components/ChessBoard.vue";
import ChessGameViewer from "@/components/ChessGameViewer.vue";
import axios from 'axios';

export default {
  components: {ChessBoard, ChessGameViewer},
  data() {
    return {
      state: initialState,
      searching: false,
      retrievedDocuments: [],
      testDocument: null,
    }
  },
  created() {
    const game = new Chess();
    game.loadPgn(testGame.game);

    let boards = []

    const chessGame = new Chess();
    boards.push(decodeState(chessGame.fen()));
    for (let i = 0; i < game.history().length; i++) {
      chessGame.move(game.history()[i]);
      boards.push(decodeState(chessGame.fen()));
    }

    this.testDocument = {
      move_nr: 50,
      boards: boards,
      game: game
    }
    console.log('hi')
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

          for (let i = 0; i < history.length; i++) {
            newGame.move(history[i])
            boardStates.push(decodeState(newGame.fen()))
          }
          document['game'] = game;
          document['boards'] = boardStates;
          document['move_nr'] = document.move_nr;
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