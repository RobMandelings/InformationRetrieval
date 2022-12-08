import * as piece from './Piece.js'

export const initialState = {
    '0,0': new piece.Rook(true),
    '0,1': new piece.Knight(true),
    '0,2': new piece.Bishop(true),
    '0,3': new piece.Queen(true),
    '0,4': new piece.King(true),
    '0,5': new piece.Bishop(true),
    '0,6': new piece.Knight(true),
    '0,7': new piece.Rook(true),

    '1,0': new piece.Pawn(true),
    '1,1': new piece.Pawn(true),
    '1,2': new piece.Pawn(true),
    '1,3': new piece.Pawn(true),
    '1,4': new piece.Pawn(true),
    '1,5': new piece.Pawn(true),
    '1,6': new piece.Pawn(true),
    '1,7': new piece.Pawn(true),

    '6,0': new piece.Pawn(false),
    '6,1': new piece.Pawn(false),
    '6,2': new piece.Pawn(false),
    '6,3': new piece.Pawn(false),
    '6,4': new piece.Pawn(false),
    '6,5': new piece.Pawn(false),
    '6,6': new piece.Pawn(false),
    '6,7': new piece.Pawn(false),

    '7,0': new piece.Rook(false),
    '7,1': new piece.Knight(false),
    '7,2': new piece.Bishop(false),
    '7,3': new piece.King(false),
    '7,4': new piece.Queen(false),
    '7,5': new piece.Bishop(false),
    '7,6': new piece.Knight(false),
    '7,7': new piece.Rook(false),
}

export function loadPiece(encodedPiece) {

    if (encodedPiece === 'r') return new piece.Rook(true)
    if (encodedPiece === 'R') return new piece.Rook(false)

    if (encodedPiece === 'n') return new piece.Knight(true)
    if (encodedPiece === 'N') return new piece.Knight(false)

    if (encodedPiece === 'b') return new piece.Bishop(true)
    if (encodedPiece === 'B') return new piece.Bishop(false)

    if (encodedPiece === 'q') return new piece.Queen(true)
    if (encodedPiece === 'Q') return new piece.Queen(false)

    if (encodedPiece === 'k') return new piece.King(true)
    if (encodedPiece === 'K') return new piece.King(false)

    if (encodedPiece === 'p') return new piece.Pawn(true)
    if (encodedPiece === 'P') return new piece.Pawn(false)

}

/**
 * Encodes the chess state into FEN encoding
 */
export function encodeState(state) {
    let encoding = '';

    for (let row = 0; row < 8; row++) {
        let rowEncoding = '';
        let emptyCtr = 0;
        for (let col = 0; col < 8; col++) {
            const piece = state[`${row},${col}`]
            if (piece) {
                if (emptyCtr > 0) rowEncoding += `${emptyCtr}`;
                rowEncoding += piece.shortName;
                emptyCtr = 0;
            } else emptyCtr++;
        }

        if (emptyCtr > 0) rowEncoding += `${emptyCtr}`;
        encoding += `${rowEncoding}`;
        if (row < 7) encoding += '/';
    }
    return encoding;
}

export function decodeState(fen) {

    let state = {}
    const fenNoHeaders = fen.split(' ')[0];
    const rows = fenNoHeaders.split('/');

    for (let i = 0; i < 8; i++) {
        const row = rows[i];
        for (let j = 0; j < 8; j++) {

            const elem = row[j];
            if (isNaN(elem)) {
                state[`${i},${j}`] = loadPiece(row[j]);
            } else {
                j += (parseInt(elem) - 1)
            }
        }
    }

    return state
}