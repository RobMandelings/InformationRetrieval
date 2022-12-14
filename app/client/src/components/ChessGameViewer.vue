<template>
  <div class="flex flex-col space-y-3">
    <div class="h-2/3">
      <div class="flex flex-row h-full w-full">
        <div class="w-2/5">
          <!--   General game data     -->
          <h2 class="mb-2 text-lg font-semibold text-gray-900 dark:text-white">Game Data</h2>
          <div class="flex flex-col space-y-1 text-left">
            <div>Event: {{ this.event }}</div>
            <div>Players: {{ this.whiteName }} (white) vs {{ this.blackName }} (black)</div>
            <div>Datetime: {{ this.dateTime }}</div>
          </div>
        </div>
        <div class="w-3/5">
          <!--   Selected board vue     -->
          <!--          <div class="h-full w-full bg-blue-500"></div>-->
          <div class="border-4 mt-1 mr-1">
            <chess-board class="h-full w-full"
                         :highlight="this.selectedMoveNr === this.documentData.move_nr"
                         :state="this.selectedBoard"></chess-board>
          </div>
        </div>
      </div>
    </div>
    <div class="h-1/3">
      <div class="flex flex-row h-full w-full gap-2 overflow-x-auto">
        <template v-for="(board, move_nr) in boards">
          <div class="flex flex-col flex-shrink-0 flex-grow-0" style="width: 150px">
            <div :class="move_nr === this.selectedMoveNr ? 'border-green-600' : 'border-gray-800'"
                 class="border-4 focus:ring-0 hover:border-sky-600 transition h-full w-full"
                 tabindex="0"
                 ref="scroll-board"
                 @keydown.prevent.stop="keyPressedInScroll($event)"
                 @click="boardClicked(move_nr)"
            >
              <chess-board
                  :highlight="move_nr === this.documentData.move_nr"
                  :state="board"
              ></chess-board>
            </div>
            <div>Move {{ move_nr }}</div>
          </div>
        </template>
      </div>
      <!--   Board scroller   -->
    </div>
  </div>
</template>

<script>

import ChessBoard from "@/components/ChessBoard.vue";

export default {
  components: {ChessBoard},
  props: [
    'documentData'
  ],
  data() {
    return {
      selectedMoveNr: 0
    }
  },
  mounted() {
    // TODO might not be necessary anymore
    this.initializeBoard();
  },
  watch: {
    documentData() {
      this.initializeBoard();
    }
  },
  computed: {
    selectedBoard() {
      return this.boards[this.selectedMoveNr];
    },
    boards() {
      if (this.documentData) return this.documentData.boards;
      return [];
    },
    event() {
      return this.documentData.game.header().Event;
    },
    whiteName() {
      return this.documentData.game.header().White;
    },
    blackName() {
      return this.documentData.game.header().Black
    },
    dateTime() {
      return `${this.documentData.game.header().UTCDate} ${this.documentData.game.header().UTCTime}`;
    },
  },
  methods: {
    initializeBoard() {
      this.selectedMoveNr = this.documentData.move_nr;
    },
    boardClicked(move_nr) {
      this.selectedMoveNr = move_nr;
      const boardElem = this.$refs[`scroll-board`][move_nr];
      this.$nextTick(() => {
        boardElem.focus();
      })
    },
    mod(n, m) {
      return ((n % m) + m) % m;
    },
    keyPressedInScroll(event) {
      event = event || window.event;
      let charCode = event.keyCode || event.which;

      if (charCode === 65 || charCode === 37) { // a or left
        this.boardClicked(this.mod(this.selectedMoveNr - 1, this.boards.length))
      } else if (charCode === 68 || charCode === 39) {// d or right
        this.boardClicked(this.mod(this.selectedMoveNr + 1, this.boards.length))
      }
    }
  }
}

</script>