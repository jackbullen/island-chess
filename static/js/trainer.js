var moves = [];
var game = new Chess(variationFEN);
var currentMove = 0;
let maxIncorrectMoveCount = 3;
var incorrectMoveCount = 0;
function onDragStart (source, piece, position, orientation) {
  // do not pick up pieces if the game is over
  if (game.game_over()) return false
  // only pick up pieces for the side to move
  if ((game.turn() === 'w' && piece.search(/^b/) !== -1) ||
      (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
    return false
  }
}
function onDrop(source, target) {
  var move = game.move({
      from: source,
      to: target,
      promotion: 'q' // always promote to a queen for example simplicity
  })
console.log(variationMoves[currentMove]);
  if (move === null) return 'snapback'

  if (move.san !== variationMoves[currentMove]) {
      
      
      // alert('Incorrect move! The correct move is ' + variationMoves[currentMove])
      incorrectMoveCount++;
      
      if (incorrectMoveCount == maxIncorrectMoveCount) {
          alert('You made too many mistakes. Training restarted!');
          incorrectMoveCount = 0;
          currentMove = 0;
          game.reset();
          board.position(game.fen());
          return 'snapback';
      }
      game.undo();
      return 'snapback'
  }


  currentMove++;
  if (currentMove === variationMoves.length) {
      alert('You reached the end of the variation!')
      currentMove--;
      return;
  }

  // board.position(game.fen());
}


var variationName = document.getElementsByName('name')[0].content;
var variationFEN = document.getElementsByName('fen')[0].content
var variationPGN = document.currentScript.getAttribute('pgn');
var joinedPGN = variationPGN.split(/\d+\./).slice(1);

var variationMoves = [];
var ind = 0;
for (var i = 0; i < joinedPGN.length; i++) {
  if (joinedPGN[i] == "") {
    continue;
  }
  if (joinedPGN[i].split(" ").length < 3){
    variationMoves[ind] = joinedPGN[i].split(" ")[1];
    break;
  }
  else {
    variationMoves[ind] = joinedPGN[i].split(" ")[1];
    variationMoves[ind+1] = joinedPGN[i].split(" ")[2];
  }
  ind+=2;
}  

var board = Chessboard('board', {
    draggable: true,
    position: variationFEN,
    onDrop: onDrop,
    onDragStart: onDragStart
  })
  
  