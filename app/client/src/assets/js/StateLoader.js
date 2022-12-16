import * as piece from './Piece.js'

export const initialState = {
    '0,0': new piece.Rook(true),
    '0,1': new piece.Knight(true),
    '0,2': new piece.Bishop(true),
    '0,3': new piece.King(true),
    '0,4': new piece.Queen(true),
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
    '7,3': new piece.Queen(false),
    '7,4': new piece.King(false),
    '7,5': new piece.Bishop(false),
    '7,6': new piece.Knight(false),
    '7,7': new piece.Rook(false),
}

export const testGame = {
    'game': "[Event \"Rated Bullet game\"]\n" +
        "[Site \"https://lichess.org/rklpc7mk\"]\n" +
        "[White \"Naitero_Nagasaki\"]\n" +
        "[Black \"800\"]\n" +
        "[Result \"0-1\"]\n" +
        "[UTCDate \"2012.12.31\"]\n" +
        "[UTCTime \"23:04:57\"]\n" +
        "[WhiteElo \"1824\"]\n" +
        "[BlackElo \"1973\"]\n" +
        "[WhiteRatingDiff \"-6\"]\n" +
        "[BlackRatingDiff \"+8\"]\n" +
        "[ECO \"B12\"]\n" +
        "[Opening \"Caro-Kann Defense: Goldman Variation\"]\n" +
        "[TimeControl \"60+1\"]\n" +
        "[Termination \"Normal\"]\n" +
        "\n" +
        "1. e4 c6 2. Nc3 d5 3. Qf3 dxe4 4. Nxe4 Nd7 5. Bc4 Ngf6 6. Nxf6+ Nxf6 7. Qg3 Bf5 8. d3 Bg6 9. Ne2 e6 10. Bf4 Nh5 11. Qf3 Nxf4 12. Nxf4 Be7 13. Bxe6 fxe6 14. Nxe6 Qa5+ 15. c3 Qe5+ 16. Qe3 Qxe3+ 17. fxe3 Kd7 18. Nf4 Bd6 19. Nxg6 hxg6 20. h3 Bg3+ 21. Kd2 Raf8 22. Rhf1 Ke7 23. d4 Rxf1 24. Rxf1 Rf8 25. Rxf8 Kxf8 26. e4 Ke7 27. Ke3 g5 28. Kf3 Be1 29. Kg4 Bd2 30. Kf5 Bc1 31. Kg6 Kf8 32. e5 Bxb2 33. Kxg5 Bxc3 34. h4 Bxd4 35. h5 Bxe5 36. g4 Bb2 37. Kf5 Kf7 38. g5 Bc1 39. g6+ Ke7 40. Ke5 b5 41. Kd4 Kd6 42. Kc3 c5 43. a3 Bg5 44. a4 bxa4 45. Kb2 Kd5 46. Ka3 Kd4 47. Kxa4 c4 0-1\n"
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

    console.assert(false, `should not be possible, encodedPiece: ${encodedPiece}`)

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
        let col = 0;
        for (let j = 0; j < row.length; j++) {
            const elem = row[j];
            if (isNaN(elem)) {

                state[`${i},${col}`] = loadPiece(row[j]);
                col++;
            } else {
                col += parseInt(elem)
            }
        }
    }

    return state
}