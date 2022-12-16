<template>
  <div>
    <v-dialog
        v-model="fenDialog"
        width="700"
    >
      <v-card>
        <v-card-title class="text-h5 grey lighten-2">
          Load FEN
        </v-card-title>

        <v-card-text class="space-y-3 text-left">
          <v-text-field
              label="FEN Encoding"
              :rules="rules"
              hide-details="auto"
              v-model="fenEncodingInput"
          ></v-text-field>
          <div class="space-y-2 overflow-auto" style="max-height: 300px">
            <template v-for="fen in exampleFenStates">
              <v-btn block @click="fenEncodingInput = fen; submitLoadFEN()">
                {{ fen }}
              </v-btn>
            </template>
          </div>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
              color="primary"
              text
              @click="submitLoadFEN();"
          >
            Load
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <div class="flex flex-row space-x-3">
      <div class="flex flex-col w-1/2">
        <h1 class="text-2xl">Query</h1>
        <div class="flex flex-col border-2 w-full h-full p-1">
          <chess-board class="w-full h-full mb-2" :state="state"></chess-board>
          <div class="flex flex-row justify-between">
            <div class="flex flex-row space-x-1">
              <button @click="fenDialog = true" class="btn-secondary">Load
                FEN...
              </button>
            </div>
            <button @click.prevent.stop="submitSearch"
                    class="btn-primary disabled:opacity-50"
                    :disabled="searching"
            >
              <span v-if="searching" role="status">
                <svg class="inline mr-2 w-5 h-5 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
                     viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path
                      d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                      fill="currentColor"/>
                  <path
                      d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                      fill="currentFill"/>
                </svg>
                <span class="sr-only">Loading...</span>
              </span>
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
              <template v-for="document in retrievedDocuments">
                <chess-game-viewer :document-data="document"></chess-game-viewer>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="flex flex-col items-center">
      <div class="flex flex-row">
        <v-checkbox
            hide-details
            v-model="selectedMethods"
            label="Board"
            value="board"
        ></v-checkbox>
        <v-checkbox
            hide-details
            v-model="selectedMethods"
            label="Reachability"
            value="reachability"
        ></v-checkbox>
        <v-checkbox
            hide-details
            v-model="selectedMethods"
            label="Attack"
            value="attack"
        ></v-checkbox>
        <v-checkbox
            hide-details
            v-model="selectedMethods"
            label="Defense"
            value="defense"
        ></v-checkbox>
        <v-checkbox
            hide-details
            v-model="selectedMethods"
            label="Ray Attack"
            value="ray_attack"
        ></v-checkbox>
        <v-checkbox
            hide-details
            v-model="selectedMethods"
            label="Check"
            value="check"
        ></v-checkbox>
      </div>
      <div class="w-full">
        <v-text-field
            label="Filter queries"
            hide-details="auto"

            v-model="filterQueries"
        ></v-text-field>
      </div>
    </div>
  </div>
</template>

<script>
import {decodeState, encodeState, initialState} from "@/assets/js/StateLoader.js";
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
      fenDialog: false,
      selectedMethods: [],
      exampleFenStates: [
        'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR',
        'rnbqkbnr/pp2pppp/2p5/8/4p3/2N2Q2/PPPP1PPP/R1B1KBNR',
        'r2qkb1r/pp3ppp/2p1p1b1/8/2B2n2/3P1Q2/PPP1NPPP/R3K2R',
        '8/pp2k1p1/2p3K1/6p1/3PP3/2P4P/PP4P1/2b5',
        'r2qk1r1/pbpp1pbp/1p2p2p/8/2n1P3/2PPQ2N/PP3PPP/RN2K2R',
        '1r2k1r1/p1p2p2/3pp2p/1P4p1/b1P5/Q5P1/P2R1P1P/5RK1',
        'r2q1rk1/2p3pp/p1Pp4/4pPn1/2P1P3/2N5/P5PP/2RQ1RK1',
        'r2qr1k1/pppbbpp1/3p3p/3Q4/2B1P2B/8/PPP2PPP/2KRR3',
        'r3k2r/pp2b1pp/2p1N1b1/8/8/2PPP3/PP4PP/R3K2R',
        '1r2k1r1/p1p2p2/3pp2p/1P4p1/8/Q5P1/P2R1P1P/5RK1',
        'r2q1rk1/2p4p/p1Pp2p1/4pPn1/2P1P3/2N5/P5PP/2RQR1K1',
        'r2qkb1r/pp3ppp/2p1p1b1/8/2B2n2/3P1Q2/PPP1NPPP/R3K2R',
        'r2qk1r1/pbpp1pbp/1pn1p2p/8/2B1P3/2PP1Q1N/PP3PPP/RN2K2R',

        // Check
        'r2qkb1r/pp3ppp/1pQ1p1b1/8/2B2n2/3P4/PPP1NPPP/R3K2R'
      ],
      fenEncodingInput: '',
      filterQueries: '',
    }
  },
  created() {
    const game = new Chess();

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
              url: `http://127.0.0.1:5000/api/search?state=${encodeURIComponent(stateEncoding)}&encodingMethods=${this.selectedMethods.join(',')}&filterQueries=${this.filterQueries}`
            });

        const documents = result.data.results;
        documents.forEach(document => {
          const game = new Chess();
          game.loadPgn(document['game']);
          const history = game.history()
          const newGame = new Chess()

          let boardStates = []

          boardStates.push(decodeState(newGame.fen()))
          for (let i = 0; i < history.length; i++) {
            newGame.move(history[i])
            boardStates.push(decodeState(newGame.fen()))
          }
          document['game'] = game;
          document['boards'] = boardStates;
          document['move_nr'] = document.move_nr;
        });
        documents.sort((document1, document2) => document2.score - document1.score)
        this.retrievedDocuments = documents;
      } catch (e) {
        console.log(e);
      }
      this.searching = false;
    },

    submitLoadFEN() {
      this.state = decodeState(this.fenEncodingInput);
      this.fenDialog = false;
    }
  }
}
</script>