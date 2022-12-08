<template>
  <div class="w-full">
    <div class="grid grid-cols-8 grid-rows-8 gap-0 w-full">
      <template v-for="(i, row) in 8" :key="row">
        <div class="text-xl" v-for="(j, col) in 8" :key="col">
          <div :class="getBackgroundForPosition(row, col)" style="aspect-ratio: 1/1">
            <div v-if="getPiece(row,col)">
              <img class="h-full"
                   :src="getPiece(row,col).imgPath" :alt="getPiece(row,col).name"/>
            </div>
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

  },
  props: ['state'],
  computed: {},
  methods: {
    getPiece(row, col) {
      return this.state[`${row},${col}`];
    },
    getBackgroundForPosition(row, column) {
      let black = row % 2 !== 0;
      if ((row * 8 + column) % 2 !== 0) black = !black;

      if (black) return 'bg-amber-50';
      else return 'bg-amber-800';

    }
  }
}

</script>