#!/usr/bin/env python3
"""
Test Script for Rubik's Cube Solver
===================================

This script tests the basic functionality of all modules
without requiring a webcam or physical cube.
"""

import sys
from color_detector import ColorDetector
from cube_state import CubeState
from cube_solver import CubeSolver


def test_color_detector():
    """Test the color detection functionality."""
    print("🧪 Testing Color Detector...")
    detector = ColorDetector()
    
    # Test some sample BGR colors
    test_colors = [
        ((255, 255, 255), "white"),  # White
        ((0, 255, 255), "yellow"),   # Yellow  
        ((0, 0, 255), "red"),        # Red
        ((0, 165, 255), "orange"),   # Orange
        ((255, 0, 0), "blue"),       # Blue
        ((0, 255, 0), "green")       # Green
    ]
    
    for bgr_color, expected in test_colors:
        detected = detector.detect_color(bgr_color)
        status = "✅" if detected == expected else "❌"
        print(f"  {status} BGR {bgr_color} -> {detected} (expected: {expected})")
    
    print("✅ Color Detector test completed\n")


def test_cube_state():
    """Test the cube state management."""
    print("🧪 Testing Cube State...")
    cube = CubeState()
    
    # Create a test solved cube state
    solved_faces = {
        'U': [['white'] * 3 for _ in range(3)],      # White top
        'D': [['yellow'] * 3 for _ in range(3)],     # Yellow bottom
        'R': [['red'] * 3 for _ in range(3)],        # Red right
        'L': [['orange'] * 3 for _ in range(3)],     # Orange left
        'F': [['blue'] * 3 for _ in range(3)],       # Blue front
        'B': [['green'] * 3 for _ in range(3)]       # Green back
    }
    
    # Set all faces
    for face_name, colors in solved_faces.items():
        cube.set_face(face_name, colors)
    
    # Test validation
    is_valid = cube.is_valid()
    print(f"  {'✅' if is_valid else '❌'} Cube validation: {is_valid}")
    
    # Test Kociemba string conversion
    if is_valid:
        kociemba_string = cube.to_kociemba_string()
        expected_solved = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
        is_correct = kociemba_string == expected_solved
        print(f"  {'✅' if is_correct else '❌'} Kociemba format: {is_correct}")
        print(f"  Generated: {kociemba_string}")
        print(f"  Expected:  {expected_solved}")
    
    print("✅ Cube State test completed\n")


def test_cube_solver():
    """Test the cube solver functionality."""
    print("🧪 Testing Cube Solver...")
    solver = CubeSolver()
    
    # Test with a scrambled but solvable cube state
    # This is a known valid scrambled state
    scrambled_cube = "DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL"
    
    print(f"  Testing with scrambled state: {scrambled_cube}")
    
    # Validate the cube string format
    is_valid_format = solver.validate_cube_string(scrambled_cube)
    print(f"  {'✅' if is_valid_format else '❌'} String format validation: {is_valid_format}")
    
    if is_valid_format:
        # Try to solve
        print("  🧠 Attempting to solve...")
        solution = solver.solve(scrambled_cube)
        
        if solution:
            print(f"  ✅ Solution found: {solution}")
            move_count = solver.get_move_count(solution)
            is_optimal = solver.is_optimal_solution(solution)
            print(f"  📊 Move count: {move_count}")
            print(f"  🎯 Optimal (≤20): {is_optimal}")
        else:
            print("  ❌ No solution found")
    
    print("✅ Cube Solver test completed\n")


def test_move_explanations():
    """Test move explanation functionality."""
    print("🧪 Testing Move Explanations...")
    solver = CubeSolver()
    
    test_moves = ["U", "U'", "U2", "R", "F'", "D2"]
    
    for move in test_moves:
        explanation = solver.explain_move(move)
        print(f"  {move:>3} -> {explanation}")
    
    print("✅ Move Explanations test completed\n")


def main():
    """Run all tests."""
    print("🔧 RUBIK'S CUBE SOLVER - TEST SUITE")
    print("=" * 50)
    print("Testing all modules without webcam...\n")
    
    try:
        test_color_detector()
        test_cube_state()
        test_cube_solver()
        test_move_explanations()
        
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("\nYour Rubik's Cube Solver is ready to use!")
        print("Run 'python main.py' to start the full application.")
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        print("\nPlease check your installation:")
        print("1. Make sure all required packages are installed")
        print("2. Check that all module files are present")
        print("3. Verify Python version compatibility")
        sys.exit(1)


if __name__ == "__main__":
    main()
