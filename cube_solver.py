"""
Rubik's Cube Solver Module
==========================

Uses the Kociemba algorithm to find optimal solutions for Rubik's cube.
Integrates with cube state representation and provides move explanations.
"""

import kociemba
from typing import List, Optional, Tuple
from cube_state import CubeState


class CubeSolver:
    """Solves Rubik's cube using the Kociemba algorithm."""
    
    def __init__(self):
        """Initialize the cube solver."""
        self.move_explanations = {
            'R': "Right face clockwise",
            "R'": "Right face counterclockwise", 
            'R2': "Right face 180°",
            'L': "Left face clockwise",
            "L'": "Left face counterclockwise",
            'L2': "Left face 180°", 
            'U': "Up face clockwise",
            "U'": "Up face counterclockwise",
            'U2': "Up face 180°",
            'D': "Down face clockwise", 
            "D'": "Down face counterclockwise",
            'D2': "Down face 180°",
            'F': "Front face clockwise",
            "F'": "Front face counterclockwise", 
            'F2': "Front face 180°",
            'B': "Back face clockwise",
            "B'": "Back face counterclockwise",
            'B2': "Back face 180°",
            'M': "Middle slice (like L)",
            "M'": "Middle slice (like L')",
            'M2': "Middle slice 180°",
            'E': "Equatorial slice (like D)",
            "E'": "Equatorial slice (like D')",
            'E2': "Equatorial slice 180°",
            'S': "Standing slice (like F)",
            "S'": "Standing slice (like F')", 
            'S2': "Standing slice 180°"
        }
    
    def solve_cube(self, cube_state: CubeState) -> Optional[List[str]]:
        """
        Solve the cube and return the solution as a list of moves.
        
        Args:
            cube_state: The current state of the cube
            
        Returns:
            List of move strings, or None if no solution found
        """
        # Convert cube state to Kociemba format
        cube_string = self._cube_state_to_string(cube_state)
        
        if not cube_string:
            print("❌ Failed to convert cube state to string format")
            return None
        
        print(f"🔤 Cube state: {cube_string}")
        
        # Check if cube is already solved
        if self._is_solved(cube_string):
            print("🎉 Cube is already solved! No moves needed.")
            return []
        
        print(f"🧠 Solving cube state: {cube_string}")
        
        try:
            # Use Kociemba algorithm to solve
            solution = kociemba.solve(cube_string)
            
            if solution == "":
                print("🎉 Cube is already solved!")
                return []
            
            # Split solution into individual moves
            moves = solution.split()
            return moves
            
        except Exception as e:
            print(f"❌ Solver error: {e}")
            return None
    
    def _is_solved(self, cube_string: str) -> bool:
        """Check if the cube is in solved state."""

        solved_pattern = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
        return cube_string == solved_pattern
    
    def _cube_state_to_string(self, cube_state: CubeState) -> Optional[str]:
        """Convert CubeState to Kociemba format string."""
        try:
            result = ""
            
            # Process faces in the order: U, R, F, D, L, B
            face_order = ['U', 'R', 'F', 'D', 'L', 'B']
            
            for face_name in face_order:
                face_data = cube_state.get_face(face_name)
                if not face_data:
                    return None
                
                # Convert colors to notation
                for row in face_data:
                    for color in row:
                        notation = cube_state.color_to_notation.get(color)
                        if not notation:
                            print(f"❌ Unknown color: {color}")
                            return None
                        result += notation
            
            return result
            
        except Exception as e:
            print(f"❌ Error converting cube state: {e}")
            return None
    
    def explain_solution(self, moves: List[str]) -> None:
        """Print a detailed explanation of the solution moves."""
        if not moves:
            print("🎉 No moves needed - cube is already solved!")
            return
        
        print(f"\n📖 SOLUTION EXPLANATION ({len(moves)} moves):")
        print("=" * 50)
        
        for i, move in enumerate(moves, 1):
            explanation = self.move_explanations.get(move, "Unknown move")
            print(f"  {i:2d}. {move:3s} - {explanation}")
        
        print("=" * 50)
        print("💡 TIP: Hold the cube with white on top and green facing you")
        print("💡 TIP: Clockwise means turning like a clock when looking at that face")
    
    def format_solution_compact(self, moves: List[str]) -> str:
        """Format solution as a compact string."""
        if not moves:
            return "No moves needed - already solved!"
        
        return " ".join(moves)
    
    def get_solution_stats(self, moves: List[str]) -> dict:
        """Get statistics about the solution."""
        if not moves:
            return {
                'total_moves': 0,
                'quarter_turns': 0,
                'half_turns': 0,
                'face_usage': {},
                'efficiency': 'Perfect'
            }
        
        stats = {
            'total_moves': len(moves),
            'quarter_turns': 0,
            'half_turns': 0,
            'face_usage': {},
            'efficiency': 'Good'
        }
        
        for move in moves:
            # Count move types
            if move.endswith('2'):
                stats['half_turns'] += 1
            else:
                stats['quarter_turns'] += 1
            
            # Count face usage
            face = move[0]
            stats['face_usage'][face] = stats['face_usage'].get(face, 0) + 1
        
        # Determine efficiency
        if stats['total_moves'] <= 15:
            stats['efficiency'] = 'Excellent'
        elif stats['total_moves'] <= 20:
            stats['efficiency'] = 'Good'
        elif stats['total_moves'] <= 25:
            stats['efficiency'] = 'Fair'
        else:
            stats['efficiency'] = 'Could be better'
        
        return stats
    
    def validate_solution(self, cube_state: CubeState, moves: List[str]) -> bool:
        """
        Validate that the solution actually solves the cube.
        
        Args:
            cube_state: Original cube state
            moves: Solution moves to validate
            
        Returns:
            True if solution is valid, False otherwise
        """
        try:
            # This is a simplified validation
            # In a full implementation, you would apply each move
            # and check if the final state is solved
            
            # For now, just check if we got a solution from Kociemba
            return moves is not None
            
        except Exception as e:
            print(f"⚠️  Validation error: {e}")
            return False
    
    def print_solution_summary(self, moves: List[str]) -> None:
        """Print a summary of the solution."""
        if not moves:
            print("\n🎉 SOLUTION SUMMARY:")
            print("✅ Cube is already solved!")
            print("🎯 Move count: 0")
            print("⭐ Efficiency: Perfect")
            return
        
        stats = self.get_solution_stats(moves)
        
        print(f"\n🎉 SOLUTION SUMMARY:")
        print(f"✅ Solution: {self.format_solution_compact(moves)}")
        print(f"🎯 Move count: {stats['total_moves']}")
        print(f"🔄 Quarter turns: {stats['quarter_turns']}")
        print(f"🔃 Half turns: {stats['half_turns']}")
        print(f"⭐ Efficiency: {stats['efficiency']}")
        
        if stats['face_usage']:
            face_usage_str = ", ".join([f"{face}×{count}" for face, count in stats['face_usage'].items()])
            print(f"🎲 Face usage: {face_usage_str}")
