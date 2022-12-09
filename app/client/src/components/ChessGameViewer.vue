<template>
  <div class="flex flex-col">
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
          <chess-board class="h-full w-full"
                       :highlight="this.selectedMoveNr === this.documentData.move_nr"
                       :state="this.selectedBoard"></chess-board>
        </div>
      </div>
    </div>
    <div class="h-1/3">
      <div class="flex flex-row h-full w-full gap-2 overflow-x-auto">
        <template v-for="(board, move_nr) in boards">
          <div class="flex flex-col flex-shrink-0 flex-grow-0" style="width: 150px">
            <div class="border-2 hover:border-green-600 h-full w-full">
              <chess-board
                  :highlight="move_nr === this.documentData.move_nr"
                  :state="board"
                  @click="boardClicked(move_nr)"
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
    this.selectedMoveNr = this.documentData.move_nr;
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
    },
    boardClicked(move_nr) {
      this.selectedMoveNr = move_nr;
    },
  }
}

</script>