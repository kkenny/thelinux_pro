var default_status_color;
var games = [];
var boards = [];
var current_board;
var board_move_idx = []; /* Move index */
var board_end = []; /* User solved the position */
var board_fen = [];
var board_mov = [];
var board_res = [];
var board_lang = 'en';
var button_prev_move = [];
var button_next_move = [];
var button_flip_board = [];
var display_turn = [];

function removeGreySquares(i) {
    $('#chess_board_' + i + ' .square-55d63').css('background', '');
};

function greySquare(i, square) {
  var squareEl = $('#chess_board_' + i + ' .square-' + square);

  var background = '#a9a9a9';
  if (squareEl.hasClass('black-3c85d') === true) {
    background = '#696969';
  }

  squareEl.css('background', background);
};

// do not pick up pieces if the game is over
// only pick up pieces for the side to move
function onDragStart(i, source, piece, position, orientation) {
  var game = games[i];

  if (game.game_over() === true ||
      (game.turn() === 'w' && piece.search(/^b/) !== -1) ||
      (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
    return false;
  }
};

function onDrop(i, source, target) {
  var game  = games[i];
  var moves = board_mov[i];
  var mvidx = board_move_idx[i];
  removeGreySquares(i);

  if (!moves[mvidx]) {
    return 'snapback';
  } else if (!board_end[i] && (moves[mvidx].from != source || moves[mvidx].to != target)) {
    $('#chess_status_' + i).css('color', 'red');
    if (board_lang == 'tr') {
      $('#chess_status_' + i).text('Hatalı hamle!');
    } else {
      $('#chess_status_' + i).text('Bad move!');
    }
    return 'snapback';
  }

  // see if the move is legal
  var move = game.move({
    from: source,
    to: target,
    promotion: 'q' // FIXME: always promote to a queen for example simplicity
  });

  // illegal move
  if (move === null) return 'snapback';

  mvidx += 1;
  if (moves[mvidx]) {
    game.move(moves[mvidx]);
    mvidx += 1;
  }

  if (!board_end[i] && !moves[mvidx]) {
    board_end[i] = true;
    $('#chess_status_' + i).css('color', '#ffb3b3');
    if (board_lang == 'tr') {
      $('#chess_status_' + i).text('Çözdün, tebrikler!');
    } else {
      $('#chess_status_' + i).text('Solved, congrats!');
    }
  } else {
    $('#chess_status_' + i).css('color', '#00e600');
    if (board_lang == 'tr') {
      $('#chess_status_' + i).text('Doğru hamle!');
    } else {
      $('#chess_status_' + i).text('Good move!');
    }
  }

  board_move_idx[i] = mvidx;
  updateStatus(game, display_turn[i]);
};

function onMouseoverSquare(i, square, piece) {
  var game = games[i];

  // get list of possible moves for this square
  var moves = game.moves({
    square: square,
    verbose: true
  });

  // exit if there are no moves available for this square
  if (moves.length === 0) return;

  // highlight the square they moused over
  greySquare(i, square);

  // highlight the possible squares for this piece
  for (var i = 0; i < moves.length; i++) {
    greySquare(i, moves[i].to);
  }
};

function onMouseoutSquare(i, square, piece) {
  removeGreySquares(i);
};

// update the board position after the piece snap
// for castling, en passant, pawn promotion
function onSnapEnd(i) {
  boards[i].position(games[i].fen());
};

function updateStatus(game, display_turn) {
  if (game.turn() === 'w') {
    display_turn.css('color', 'white');
  } else {
    display_turn.css('color', 'black');
  }
};

function parse_moves(moves) {
  return $.map(moves.split(" "), function (uci_move) {
    var chess_move = {from: uci_move.slice(0,2), to: uci_move.slice(2,4)}
    var p = uci_move.slice(4,5);
    if (p != "") {
      chess_move.promotion = p;
    }

    return chess_move;
  });
}

$(function() {
  var board_config;
  default_status_color = $('#chess_status_0').css('color');

  for (i = 0; i < board_fen.length; i++) {
    board_config = {
      idx: i,
      draggable: true,
      dropOffBoard: 'snapback', /* default */
      showNotation: false,
      pieceTheme: '/images/chesspieces/alpha/{piece}.png',
      onDragStart: function(source, piece, position, orientation) {
        return onDragStart(this.idx, source, piece, position, orientation);
      },
      onDrop: function(source, target) {
        return onDrop(this.idx, source, target);
      },
      onMouseoutSquare: function (square, piece) {
        return onMouseoutSquare(this.idx, square, piece);
      },
      onMouseoverSquare: function(square, piece) {
        return onMouseoverSquare(this.idx, square, piece);
      },
      onSnapEnd: function () {
        return onSnapEnd(this.idx);
      }
    };

    board_move_idx[i]    = 0;
    board_end[i]         = false;

    button_flip_board[i] = $("a#flipboard_" + i);
    button_prev_move[i]  = $("a#prev_move_" + i);
    button_next_move[i]  = $("a#next_move_" + i);
    display_turn[i]      = $("i#display_turn_" + i);

    button_flip_board[i].on('click', function () {
      var idx = this.id.slice(-1);

      boards[idx].flip();
      return false;
    });
    button_prev_move[i].on('click', function () {
      var idx = this.id.slice(-1);

      if (board_move_idx[idx] > 0) {
        if (board_end[idx]) {
          board_move_idx[idx] -= 1;
        } else {
          $('#chess_status_' + idx).text('');
          board_move_idx[idx] -= 2;
          games[idx].undo(); boards[idx].position(games[idx].fen(), true);
        }
        games[idx].undo(); boards[idx].position(games[idx].fen(), true);
      }
      updateStatus(games[idx], display_turn[idx]);
      return false;
    });
    button_next_move[i].on('click', function () {
      var idx = this.id.slice(-1);

      if (board_end[idx] && board_mov[idx][board_move_idx[idx]]) {
        games[idx].move(board_mov[idx][board_move_idx[idx]]);
        boards[idx].position(games[idx].fen(), true);
        board_move_idx[idx] += 1;
      }
      updateStatus(games[idx], display_turn[idx]);
      return false;
    });

    games[i] = new Chess();
    games[i].load(board_fen[i]);
    if (games[i].turn() === 'w') {
      board_config.orientation = 'white';
      // $('#chess_task_' + i).text('Etüt: Beyaz oynar.');
    } else {
      board_config.orientation = 'black';
      // $('#chess_task_' + i).text('Etüt: Beyaz oynar.');
    }
    board_config.position = games[i].fen();
    boards[i] = new ChessBoard('chess_board_' + i, board_config);

    $(window).resize(boards[i].resize);
    updateStatus(games[i], display_turn[i]);
  //  notation_checkbox.on('click', function () {
  //    cboard_config.showNotation = !cboard_config.showNotation;
  //    cboard.showNotation = cboard_config.showNotation;
  //    /* HACK: resize redraws board -> toggles notation */
  //    cboard.resize();
  //    return false;
  //  });
  }
});
