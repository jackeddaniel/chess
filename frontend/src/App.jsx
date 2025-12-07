import React, { useState, useEffect, useRef } from 'react';
import { Chessboard } from 'react-chessboard';
import { Chess } from 'chess.js';

function App() {
    const [game, setGame] = useState(new Chess());
    const [position, setPosition] = useState(game.fen());
    const wsRef = useRef(null);

    // WebSocket connection
    useEffect(() => {
        const ws = new WebSocket('ws://localhost:8080/ws');

        ws.onopen = () => {
            console.log('WebSocket connected');
        };

        ws.onmessage = (event) => {
            console.log('Message from server:', event.data);
        };

        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        ws.onclose = () => {
            console.log('WebSocket disconnected');
        };

        wsRef.current = ws;

        return () => {
            ws.close();
        };
    }, []);

    // Send move to WebSocket
    const sendMoveToServer = (move, currentFen) => {
        if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
            const moveData = {
                from: move.from,
                to: move.to,
                piece: move.piece,
                captured: move.captured,
                promotion: move.promotion,
                san: move.san,
                fen: currentFen,
                timestamp: new Date().toISOString()
            };

            wsRef.current.send(JSON.stringify(moveData));
            console.log('Move sent to server:', moveData);
        } else {
            console.error('WebSocket is not connected');
        }
    };

    // Handle piece drop
    function onPieceDrop({ sourceSquare, targetSquare }) {
        console.log('=== onPieceDrop called ===');
        console.log('Source:', sourceSquare);
        console.log('Target:', targetSquare);

        try {
            const move = game.move({
                from: sourceSquare,
                to: targetSquare,
                promotion: 'q'
            });

            if (move === null) {
                console.log('Illegal move');
                return false;
            }

            console.log('Move successful:', move);
            setPosition(game.fen());
            sendMoveToServer(move, game.fen());

            return true;
        } catch (error) {
            console.error('Move error:', error);
            return false;
        }
    }

    // Reset game
    const resetGame = () => {
        const newGame = new Chess();
        setGame(newGame);
        setPosition(newGame.fen());
        console.log('Game reset');
    };

    return (
        <div style={{
            padding: '20px',
            minHeight: '100vh',
            backgroundColor: '#f0f0f0'
        }}>
            <h1 style={{ textAlign: 'center', marginBottom: '20px' }}>
                My Chess Game
            </h1>

            <div style={{
                maxWidth: '600px',
                margin: '0 auto'
            }}>
                <Chessboard
                    options={{
                        position: position,
                        onPieceDrop: onPieceDrop
                    }}
                />

                <div style={{ marginTop: '20px', textAlign: 'center' }}>
                    <button
                        onClick={resetGame}
                        style={{
                            padding: '10px 20px',
                            fontSize: '16px',
                            cursor: 'pointer',
                            backgroundColor: '#4CAF50',
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px'
                        }}
                    >
                        Reset Game
                    </button>
                </div>

                <div style={{
                    marginTop: '20px',
                    padding: '10px',
                    backgroundColor: 'white',
                    borderRadius: '4px'
                }}>
                    <h3>Game Status:</h3>
                    <p>Turn: {game.turn() === 'w' ? 'White' : 'Black'}</p>
                    <p>Moves: {game.history().length}</p>
                    <p>FEN: {position}</p>
                    {game.isCheckmate() && <p style={{ color: 'red', fontWeight: 'bold' }}>Checkmate!</p>}
                    {game.isCheck() && <p style={{ color: 'orange', fontWeight: 'bold' }}>Check!</p>}
                    {game.isDraw() && <p style={{ color: 'blue', fontWeight: 'bold' }}>Draw!</p>}
                </div>

                <div style={{
                    marginTop: '20px',
                    padding: '10px',
                    backgroundColor: 'white',
                    borderRadius: '4px',
                    maxHeight: '200px',
                    overflowY: 'auto'
                }}>
                    <h3>Move History:</h3>
                    <p>{game.history().join(', ') || 'No moves yet'}</p>
                </div>
            </div>
        </div>
    );
}

export default App;
