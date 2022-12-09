<!--         :style="{width: `${boardWidth}px`}"-->
<template>
  <div ref="chess-board">
    <div class="grid gap-0"
         style="grid-template-rows: repeat(8, minmax(0, 1fr));grid-template-columns: repeat(8,  minmax(0, 1fr));"
    >
      <template v-for="(i, row) in 8" :key="row">
        <div class="text-xl" :class="getBackgroundForPosition(row, col)" v-for="(j, col) in 8" :key="col">
          <div v-if="getPiece(row,col)">
            <img class="h-full"
                 :src="getPiece(row,col).imgPath" :alt="getPiece(row,col).name"/>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>
<script>

export default {
  name: 'ChessBoard',
  data() {
    return {
      boardWidth: 0
    }
  },
  mounted() {
    window.addEventListener('resize', this.handleResize)
    this.handleResize()
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize)
  },
  props: ['state', 'highlight'],
  computed: {},
  methods: {
    getPiece(row, col) {
      return this.state[`${row},${col}`];
    },
    getBackgroundForPosition(row, column) {
      let black = row % 2 !== 0;
      if ((row * 8 + column) % 2 !== 0) black = !black;

      if (black) return this.highlight ? 'bg-emerald-50' : 'bg-amber-50';
      else return this.highlight ? 'bg-emerald-800' : 'bg-amber-800';
    },
    handleResize() {
      if (this.$refs["chess-board"]) {
        // this.boardWidth = Math.min(this.$refs["chess-board"].offsetWidth, this.$refs["chess-board"].offsetHeight)
      }
    }
  }
}

</script>