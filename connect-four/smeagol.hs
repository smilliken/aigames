import Data.Array
import Data.Function (on)
import Data.List (intercalate, group, groupBy, maximumBy, sortBy, tails)
import Data.Maybe (fromJust, fromMaybe)
import System.IO (hFlush, hPutStrLn, stderr, stdout)

rowCount = 6
colCount = 7
winStreak = 4
type Col = Int
type Row = Int
type Cell = (Row, Col)
data CellOwner = Us | Nobody | Them deriving (Eq, Ord, Show)
type Move = (Col, CellOwner)
type Moves = [Move]
type Board = Array Cell CellOwner
data GameState = GameState Moves Board deriving (Eq)
instance Show GameState where
    show (GameState moves board) =
        "\n" `intercalate` [" " `intercalate`
            [showCell $ board ! (r, c) | c <- [0..(colCount - 1)]]
                | r <- reverse [0..(rowCount - 1)]]

main :: IO a
main = gameLoop $ GameState [] emptyBoard

gameLoop :: GameState -> IO a
gameLoop gamestate = do
    theirMove <- receiveMove
    let gamestate' = (
          if theirMove == Nothing
              then gamestate
              else updateGameState gamestate (fromJust theirMove))
        ourMove = (nextMove gamestate', Us)
        gamestate'' = updateGameState gamestate' ourMove
    sendMove ourMove
--    debug $ gamestate''
--    debug . winner $ gamestate''
--    let (GameState moves _) = gamestate'' in debug $ moves
    let (GameState _ board) = gamestate'' in debug $ score board Us
    gameLoop $ gamestate''

sendMove :: Move -> IO ()
sendMove (col, _) = do
    putStrLn $ show col
    hFlush stdout

receiveMove :: IO (Maybe Move)
receiveMove = do
    input <- getLine
    let move = parse input
    return $ (if move == Nothing
                 then Nothing
                 else let Just m = move in Just (m, Them))

parse :: String -> Maybe Col
parse input
    | parsed == [] = Nothing
    | otherwise = let [(val, _)] = parsed in
                  if val >= 0 && val < colCount
                     then Just (val :: Col)
                     else Nothing
    where parsed = reads input :: [(Int, String)]

debug :: Show a => a -> IO ()
debug msg = do
    hPutStrLn stderr (show msg)
    hFlush stderr

showCell :: CellOwner -> String
showCell Us = "0"
showCell Them = "1"
showCell Nobody = "."

emptyBoard :: Board
emptyBoard = listArray ((0, 0), (rowCount - 1, colCount - 1)) $ repeat Nobody

cellIsEmpty :: Board -> Cell -> Bool
cellIsEmpty board cell = board ! cell == Nobody

nextEmptyCell :: Board -> Col -> Maybe Cell
nextEmptyCell board col = ret rows
  where rows = filter (\ r -> cellIsEmpty board (r, col)) $ [0..rowCount - 1]
        ret [] = Nothing
        ret (row:_) = Just (row, col)

updateBoard :: Board -> Move -> Board
updateBoard board (col, owner) =
    if cell == Nothing
       then board
       else let Just cell' = cell in board // [(cell', owner)]
    where cell = nextEmptyCell board col

updateGameState :: GameState -> Move -> GameState
updateGameState (GameState moves board) move =
    GameState (move : moves) (updateBoard board move)

updateGameStates :: GameState -> [Move] -> GameState
updateGameStates gamestate moves = foldl updateGameState gamestate moves

isColOpen :: Board -> Col -> Bool
isColOpen board col =
    any (cellIsEmpty board) . map (\ r -> (r, col)) $ [0..rowCount - 1]

legalCols :: Board -> [Col]
legalCols board = filter (isColOpen board) $ [0..colCount - 1]

isLegal :: Board -> Col -> Bool
isLegal board col = col `elem` (legalCols board)

isOurs :: Move -> Bool
isOurs (_, Us) = True
isOurs _ = False

isTheirs :: Move -> Bool
isTheirs (_, Them) = True
isTheirs _ = False

maybeHead :: [a] -> Maybe a
maybeHead (x:_) = Just x
maybeHead _ = Nothing

headDefault :: a -> [a] -> a
headDefault d xs = fromMaybe d . maybeHead $ xs

cellsByCharacteristic :: Ord a => (Cell -> a) -> [[Cell]]
cellsByCharacteristic chr =
    groupBy ((==) `on` chr) . sortBy (compare `on` chr) $
    range ((0, 0), (rowCount - 1, colCount - 1))

rowCells :: [[Cell]]
rowCells = cellsByCharacteristic fst

colCells :: [[Cell]]
colCells = cellsByCharacteristic snd

leftDiagCells :: [[Cell]]
leftDiagCells = cellsByCharacteristic (\ (r, c) -> r + c)

rightDiagCells :: [[Cell]]
rightDiagCells = cellsByCharacteristic (\ (r, c) -> r - c)

allSeries :: [[Cell]]
allSeries = rowCells ++ colCells ++ leftDiagCells ++ rightDiagCells

seriesWinner :: [CellOwner] -> CellOwner
seriesWinner [] = Nobody
seriesWinner cos = headDefault Nobody .
    filter (/= Nobody) .
    map head .
    filter (\ g -> length g >= winStreak) .
    group $ cos

winner :: GameState -> CellOwner
winner (GameState moves board) =
    headDefault Nobody .
    filter (/= Nobody) .
    map seriesWinner .
    map (\ cs -> [board ! c | c <- cs]) $
    allSeries

nextMoveMod :: GameState -> Col
nextMoveMod (GameState [] _) = 0
nextMoveMod (GameState [_] _) = 0
nextMoveMod (GameState moves board) =
    headDefault 0 . filter (isLegal board) . drop 1 $ mods
    where prevs = map (\ (c, _) -> c) . filter isOurs $ moves
          mods = iterate (\ c -> (c + 1) `mod` colCount) $ headDefault 0 prevs

nextMove :: GameState -> Col
nextMove (GameState [] _) = 3
nextMove (GameState [_] _) = 3
nextMove gamestate@(GameState moves board) =
    maximumBy (compare `on` (\ c ->  nextMoveSearch (gamestate `updateGameState` (c, Us)) 1)) $
    legalCols board

nextMoveSearch :: GameState -> Int -> Int
nextMoveSearch gamestate 0 = scoreGameState gamestate Us
nextMoveSearch gamestate@(GameState moves board) depth =
    --case winner gamestate of
    --    Us -> 2^31
    --    Them -> -2^31
    --    Nobody -> 
    (if co == Us then maximum else minimum) . map recur $ legalCols board
    where co = flipCellOwner . snd . headDefault (0, Nobody) $ moves
          upgs c = (gamestate `updateGameState` (c, co))
          recur c = nextMoveSearch (upgs c) (depth - 1)

scoreGameState :: GameState ->  CellOwner -> Int
scoreGameState (GameState _ board) co = score board co

score :: Board -> CellOwner -> Int
score board Nobody = 0
score board co =
    sum .
    map (\ cs -> scoreSeries co cs - scoreSeries (flipCellOwner co) cs) .
    map (\ cs -> [board ! c | c <- cs]) $ allSeries

scoreSeries :: CellOwner -> [CellOwner] -> Int
scoreSeries co cells = headScore + tailScore
    where tailScore = if length cells > 4
                         then scoreSeries co (tail cells)
                         else 0
          run = map (if co == Us then id else flipCellOwner) . take 4 $ cells
          headScore = (case run of
                  [Us, Nobody, Nobody, Nobody] -> 1
                  [Nobody, Us, Nobody, Nobody] -> 1
                  [Nobody, Nobody, Us, Nobody] -> 1
                  [Nobody, Nobody, Nobody, Us] -> 1
                  [Us, Us, Nobody, Nobody] -> 4
                  [Us, Nobody, Us, Nobody] -> 4
                  [Us, Nobody, Nobody, Us] -> 4
                  [Nobody, Us, Us, Nobody] -> 4
                  [Nobody, Us, Nobody, Us] -> 4
                  [Nobody, Nobody, Us, Us] -> 4
                  [Us, Us, Us, Nobody] -> 16
                  [Us, Us, Nobody, Us] -> 16
                  [Us, Nobody, Us, Us] -> 16
                  [Nobody, Us, Us, Us] -> 16
                  [Us, Us, Us, Us] -> 2 ^ 31
                  otherwise -> 0)

flipCellOwner :: CellOwner -> CellOwner
flipCellOwner Us = Them
flipCellOwner Them = Us
flipCellOwner Nobody = Nobody

