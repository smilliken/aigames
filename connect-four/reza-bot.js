#!/usr/bin/env node
process.stdin.setEncoding('utf8');
var fs = require('fs');

var board = [
  [null,null,null,null,null,null,null],
  [null,null,null,null,null,null,null],
  [null,null,null,null,null,null,null],
  [null,null,null,null,null,null,null],
  [null,null,null,null,null,null,null],
  [null,null,null,null,null,null,null]
];

var playMove = function(move) {
  console.log(move);
  setBoard(0, move);
};

var receiveMove = function(move) {
  setBoard(1, move);
};

var setBoard = function(player, move) {
  var movePlayed = false;
  for (var n = 5 ; n > -1 ; n--) {
    if (board[n][+move] === null) {
      board[n][+move] = player;
      break;
    }
  }
};

function getRandomInt() {
  return Math.floor(Math.random() * (6 - 0 + 1) + 0);
}

var calculateMove = function() {
  var newMove = -1;
  
  while (true) {
    newMove = getRandomInt();
    if (board[0][newMove] === null) {
      break;
    }
  }
  
  return newMove;
};

process.stdin.on('data', function(move) {
  move = move.trim();
  
  if (move === 'go!') {
    playMove('3');
  }
  else {
    receiveMove(move);
    
    //play next move based on their move
    var nextPlay = calculateMove();
    playMove(nextPlay);
  }
});
