# Dot Zero Game

A Python implementation of **Dots and Boxes** — a combinatorial two-player game — built as a research platform for developing and evaluating AI agents. The project includes a game engine, a suite of agents ranging from random play to neural-guided MCTS, PUCT tree search, game state encoding, and move analysis utilities designed to support reinforcement learning research.

## Overview

Dots and Boxes is played on a grid of dots. Players take turns drawing edges between adjacent dots. When a player completes the fourth side of a box, they claim it and take another turn. The player with the most boxes at the end wins.

This codebase provides the full game environment consumed by the companion [`dot-zero-model`](https://github.com/MWENSR-Final-Year-Project/dot-zero-model) package, which supplies the trained neural network.

## Project Structure

```
src/
  game/
    move.py              # Move dataclass (orientation, row, col)
    board.py             # Board state: edges and box ownership
    state.py             # GameState: legal moves, apply move, scoring, terminal check
    action_encoding.py   # Encode/decode moves to flat indices for RL environments
    encoding.py          # state_to_tensor: encode GameState as a (H, W, 4) float32 array
  agents/
    base_agent.py        # Abstract Agent: shared scoring and safety logic
    random_agent.py      # Picks a random legal move
    greedy_agent.py      # Always takes the highest-scoring move available
    defensive_agent.py   # Avoids opening chains; skips scoring moves that expose chains
    heuristic_agent.py   # Falls back to the move that minimises opponent-accessible boxes
    mcts_agent.py        # Pure UCT MCTS with random rollouts (no neural guidance)
    ng_mcts_agent.py     # Neural-guided MCTS using PUCT + a DotZeroNet policy/value model
  search/
    node.py              # PUCT tree node: visit counts, policy prior, backup
    puct.py              # PUCT search: select, expand, backup, get_policy, Dirichlet noise
  analysis/
    box/
      count_edges_around_box.py   # Count filled edges around a given box
      get_adjacent_boxes.py       # List boxes adjacent to a given position
    move/
      boxes_completed_by_move.py  # How many boxes a move immediately completes
      move_creates_third_edge.py  # Whether a move gives any box its third edge
      boxes_given_to_opponent.py  # Simulate boxes the opponent can greedily take after a move
      least_accessible_move.py    # Count opponent-accessible boxes after a move
      move_opens_chain.py         # Detect whether a move creates a chain of 2-edge boxes
      scoring_move_exposes_chain.py # Check if a scoring move subsequently exposes a chain

tests/                   # pytest test suite mirroring the src layout
```

## Agents

| Agent | Strategy |
|---|---|
| `RandomAgent` | Selects uniformly at random from all legal moves |
| `GreedyAgent` | Always takes the move that completes the most boxes immediately |
| `DefensiveAgent` | Prioritises scoring moves that don't expose chains; avoids opening chains entirely |
| `HeuristicAgent` | Uses the shared base logic, then falls back to the move minimising opponent-accessible boxes |
| `MCTSAgent` | Standard UCT MCTS with random rollouts — no neural guidance, pure search baseline |
| `NGMCTSAgent` | PUCT MCTS guided by a trained `DotZeroNet` policy/value network |

All agents inherit from the abstract `Agent` base class, which implements shared logic: take the best-scoring move if one exists, otherwise prefer moves that don't give a box its third edge, then delegate to the agent's own `_fallback` strategy. `MCTSAgent` and `NGMCTSAgent` override `select_move` entirely.

## Game Representation

- **Players** are encoded as `1` and `-1`.
- **Moves** are immutable Pydantic dataclasses: `Move(orientation="H"|"V", row=int, col=int)`.
- **Board** tracks horizontal edges `(size+1, size)`, vertical edges `(size, size+1)`, and box ownership `(size, size)` as NumPy arrays.
- **Action encoding** maps every move bijectively to a flat integer index in `[0, 2n(n+1))`, enabling use with RL frameworks that require discrete action spaces.
- **State encoding** (`state_to_tensor`) produces a `(n+1, n+1, 4)` float32 array with channels for horizontal edges, vertical edges, current player's boxes, and opponent's boxes.

## Installation

Requires Python 3.12+.

```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

To use `NGMCTSAgent`, also install the `neural` optional extra (requires PyTorch):

```bash
pip install -e ".[dev,neural]"
```

## Running Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=src
```

## Linting

```bash
pylint src/
```

## Docker

The image is published to the GitHub Container Registry on every push to `main`.

```bash
docker pull ghcr.io/mwensr-final-year-project/dot-zero-game:latest
```

To build locally:

```bash
docker build -t dot-zero-game .
```

## Dependencies

- `numpy` — board representation, encoding, and random move selection
- `pydantic` — validated, frozen `Move` dataclass
- `torch` *(optional, `[neural]`)* — required only for `NGMCTSAgent` inference
- `pytest` / `pytest-cov` — testing and coverage
- `pylint` — static analysis
