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
    <div class="text-center">
      <v-dialog
          v-model="pgnDialog"
          width="700"
      >
        <v-card>
          <v-card-title class="text-h5 grey lighten-2">
            Load PGN
          </v-card-title>

          <v-card-text class="space-y-3 text-left">
            <v-file-input v-model="pgnFile" clearable label="File input"></v-file-input>
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
    </div>
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
              <button @click="pgnDialog = true" class="btn-secondary">Load
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
    <div class="flex flex-col items-center">
      <div class="flex flex-row">
        <v-checkbox
            hide-details
            v-model="selectedMetrics"
            label="Reachability"
            value="Reachability"
        ></v-checkbox>
        <v-checkbox
            hide-details
            v-model="selectedMetrics"
            label="Attack"
            value="Attack"
        ></v-checkbox>
        <v-checkbox
            hide-details
            v-model="selectedMetrics"
            label="Defense"
            value="Defense"
        ></v-checkbox>
        <v-checkbox
            hide-details
            v-model="selectedMetrics"
            label="Ray Attack"
            value="RayAttack"
        ></v-checkbox>
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
      pgnFile: null,
      fenDialog: false,
      pgnDialog: false,
      selectedMetrics: [],
      exampleFenStates: [
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
        'r2qk1r1/pbpp1pbp/1pn1p2p/8/2B1P3/2PP1Q1N/PP3PPP/RN2K2R'
      ],
      fenEncodingInput: ''
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
              url: `http://127.0.0.1:5000/api/search?state=${encodeURIComponent(stateEncoding)}&metrics=${this.selectedMetrics.join(',')}`
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
        this.retrievedDocuments = documents;
      } catch (e) {
        console.log(e);
      }
      // TODO show results
      this.searching = false;
    },

    submitLoadFEN() {
      this.state = decodeState(this.fenEncodingInput);
      this.fenDialog = false;
    }
  }
}
</script>