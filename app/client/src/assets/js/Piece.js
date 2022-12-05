class Piece {
    constructor(black) {
        this.black = black;
    }

    get name() {
        console.assert(false, "Cannot get name of piece; is abstract");
    }

    isBlack() {
        return this.black;
    }

    isWhite() {
        return !this.black;
    }
}

export class King extends Piece {
    constructor(black) {
        super(black);
    }

    get name() {
        return `${this.isBlack() ? 'Black' : 'White'} King`;
    }

    get imgPath() {
        return `/src/assets/chess_pieces/${this.isBlack() ? 'black' : 'white'}-king.png`;
    }
}

export class Queen extends Piece {
    constructor(black) {
        super(black);
    }

    get name() {
        return `${this.isBlack() ? 'Black' : 'White'} Queen`
    }

    get imgPath() {
        return `/src/assets/chess_pieces/${this.isBlack() ? 'black' : 'white'}-queen.png`
    }
}

export class Rook extends Piece {
    constructor(black) {
        super(black);
    }

    get name() {
        return `${this.isBlack() ? 'Black' : 'White'} Rook`
    }

    get imgPath() {
        return `/src/assets/chess_pieces/${this.isBlack() ? 'black' : 'white'}-rook.png`
    }
}

export class Bishop extends Piece {
    constructor(black) {
        super(black);
    }

    get name() {
        return `${this.isBlack() ? 'Black' : 'White'} Bishop`
    }

    get imgPath() {
        return `/src/assets/chess_pieces/${this.isBlack() ? 'black' : 'white'}-bishop.png`
    }
}

export class Knight extends Piece {
    constructor(black) {
        super(black);
    }

    get name() {
        return `${this.isBlack() ? 'Black' : 'White'} Knight`
    }

    get imgPath() {
        return `/src/assets/chess_pieces/${this.isBlack() ? 'black' : 'white'}-knight.png`
    }
}

export class Pawn extends Piece {
    constructor(black) {
        super(black);
    }

    get name() {
        return `${this.isBlack() ? 'Black' : 'White'} Pawn`
    }

    get imgPath() {
        return `/src/assets/chess_pieces/${this.isBlack() ? 'black' : 'white'}-pawn.png`
    }
}