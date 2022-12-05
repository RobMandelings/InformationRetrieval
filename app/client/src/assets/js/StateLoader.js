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