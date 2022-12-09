<template>
  <div class="flex flex-row space-x-3">
    <div class="flex flex-col w-1/2">
      <h1 class="text-2xl">Query</h1>
      <div class="flex flex-col border-2 w-full h-full p-1">
        <chess-board class="w-full h-full mb-2" :state="state"></chess-board>
        <div class="flex flex-row justify-between">
          <div class="flex flex-row space-x-1">
            <button class="btn-secondary">Load
              FEN...
            </button>
            <button class="btn-secondary">Load
              PGN...
            </button>
          </div>
          <button @click.prevent.stop="submitSearch"
                  class="btn-primary"
                  :disabled="searching"
          >
            Search
          </button>
        </div>
      </div>
    </div>
    <div class="flex flex-col w-1/2">
      <h1 class="text-2xl">Search results</h1>
      <div style="height: 619px">
        <div class="border-2 h-full w-full overflow-auto">
          <div class="space-y-2">
            <!--            <chess-game-viewer v-if="testDocument" :document-data="testDocument"></chess-game-viewer>-->
            <template v-for="document in retrievedDocuments">
              <chess-game-viewer :document-data="document"></chess-game-viewer>
            </template>
          </div>
        </div>
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