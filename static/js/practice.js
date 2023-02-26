var path = window.location.pathname;
var pathArr = path.split('/');
var val = pathArr[pathArr.length-2];

var variation_moves = [];
var movs = [];
var currentMove = 0;
var board = null;
var game = new Chess();
var $status = $('#status');
var $fen = $('#fen');
var $pgn = $('#pgn');
var whiteSquareGrey = '#a9a9a9';
var blackSquareGrey = '#696969';

$.ajax({
  url: '/courses/get_variation_pgn/'+val,
  dataType: 'json',
  success: function(data) {
      var variation_pgn = data['pgn'];
      const game_pgn = new Chess();
      game_pgn.load_pgn(variation_pgn);
      variation_moves = game_pgn.history();
      game.load(variation_pgn);
      board.position(game.fen());
      updateStatus();
  }
});

function onDragStart (source, piece, position, orientation) {
  // do not pick up pieces if the game is over
  if (game.game_over()) return false

  // only pick up pieces for the side to move
  if ((game.turn() === 'w' && piece.search(/^b/) !== -1) ||
      (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
    return false
  }
}

  function onDrop (source, target) {
    // see if the move is legal
    var move = game.move({
      from: source,
      to: target,
      promotion: 'q' // NOTE: always promote to a queen for example simplicity
    })
  
    // illegal move
    if (move === null) {
      return 'snapback';
    }

    if (variation_moves[currentMove] != move.san) {
      board.position('start'); // reset the board to the starting position
      movs = []; // clear the variation_moves array
      currentMove = 0; // reset the currentMove index
      game.reset(); // reset the game to the starting position
      updateStatus(); // update the status to display as incorrect
      return 'snapback'
    }
  
    // move is legal
    movs.push(move);
    currentMove++;
    updateStatus();
  

  }


// update the board position after the piece snap
// for castling, en passant, pawn promotion
function onSnapEnd () {
  board.position(game.fen())
}

function removeGreySquares () {
  $('#myBoard .square-55d63').css('background', '')
}

function greySquare (square) {
  var $square = $('#myBoard .square-' + square)

  var background = whiteSquareGrey
  if ($square.hasClass('black-3c85d')) {
    background = blackSquareGrey
  }

  $square.css('background', background)
}

function onMouseoverSquare (square, piece) {
  // get list of possible moves for this square
  var moves = game.moves({
    square: square,
    verbose: true
  })

  // exit if there are no moves available for this square
  if (moves.length === 0) return

  // highlight the square they moused over
  greySquare(square)

  // highlight the possible squares for this piece
  for (var i = 0; i < moves.length; i++) {
    greySquare(moves[i].to)
  }
}
function onMouseoutSquare (square, piece) {
  removeGreySquares()
}

function updateStatus() {
  var status = '';

  var moveColor = 'White';
  if (game.turn() === 'b') {
    moveColor = 'Black';
  }

  // checkmate?
  if (game.in_checkmate() === true) {
    status = 'Game over, ' + moveColor + ' is in checkmate.';
    $('#check-indicator').text('Checkmate');
    $('#game-result').text('Checkmate');
  }

  // draw?
  else if (game.in_draw() === true) {
    status = 'Game over, drawn position';
    $('#check-indicator').text('');
    $('#game-result').text('Draw');
  }

  // game still on
  else {
    status = moveColor + ' to move';

    // check?
    if (game.in_check() === true) {
      status += ', ' + moveColor + ' is in check';
      $('#check-indicator').text('Check');
    } else {
      $('#check-indicator').text('');
    }
  }

  $('#pgn-text').text(game.pgn().replace(/\s(?=\d)/g, '\n'));
  $('#fen').text(game.fen());



}

var config = {
  draggable: true,
  position: 'start',
  onDragStart: onDragStart,
  onDrop: onDrop,
  onSnapEnd: onSnapEnd,
  onMouseoverSquare: onMouseoverSquare,
  onMouseoutSquare: onMouseoutSquare,
}
board = Chessboard('myBoard', config)

updateStatus()


$('#back-button').on('click', function() {
  if (currentMove >= 0) {
    currentMove--;
    game.undo();
    board.position(game.fen());
    updateStatus();
  }
});

$('#forward-button').on('click', function() {
  console.log(currentMove);
  
  if (currentMove < variation_moves.length - 1) {
    
    game.move(variation_moves[currentMove]);
    board.position(game.fen());
    currentMove++;
    updateStatus();
  }
});
