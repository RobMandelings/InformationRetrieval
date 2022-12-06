class Piece {
    constructor(black) {
        this.black = black;
    }

    get name() {
        console.assert(false, "Cannot get name of piece; is abstract");
    }

    get shortName() {
        console.assert(false, "Cannot get short name of piece; is abstract");
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

    get shortName() {
        return `${this.isBlack() ? 'k' : 'K'}`;
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

    get shortName() {
        return `${this.isBlack() ? 'q' : 'Q'}`;
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

    get shortName() {
        return `${this.isBlack() ? 'r' : 'R'}`;
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

    get shortName() {
        return `${this.isBlack() ? 'b' : 'B'}`;
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

    get shortName() {
        return `${this.isBlack() ? 'n' : 'N'}`;
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

    get shortName() {
        return `${this.isBlack() ? 'p' : 'P'}`;
    }

    get imgPath() {
        return `/src/assets/chess_pieces/${this.isBlack() ? 'black' : 'white'}-pawn.png`
    }
}