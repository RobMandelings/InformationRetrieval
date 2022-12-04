<template>
  <div>
    <div class="grid grid-cols-8 grid-rows-8 gap-1">
      <template v-for="row in 8">
        <div class="text-xl" v-for="column in 8">
          <div :class="getBackgroundForPosition(row, column)" style="width: 60px; aspect-ratio: 1/1"><img class="h-full" src="@/assets/chess_pieces/black-bishop.png"/></div>
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
  computed: {},
  methods: {
    getBackgroundForPosition(row, column) {
      let black;
      black = (row * 8 + column) % 2 !== 0;

      if (row % 2 === 1) black = !black;

      if (black) return 'bg-stone-600';
      else return 'bg-stone-200';

    }
  }
}

</script>