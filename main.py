#!/usr/bin/env python3
"""
Rubik's Cube Solver
===================

Complete application for scanning and solving Rubik's cubes using computer vision
and the Kociemba algorithm.
"""

from cube_scanner import CubeScanner
from color_detector import ColorDetector
from cube_state import CubeState
from cube_solver import CubeSolver


def main():
    """Main application function."""
    print("🎲 RUBIK'S CUBE SOLVER")
    print("=" * 30)
    print("Welcome to the AI-powered Rubik's Cube Solver!")
    print("Make sure your webcam is connected and working.")
    print()
    
    # Initialize components
    scanner = CubeScanner()
    detector = ColorDetector()
    cube_state = CubeState()
    solver = CubeSolver()
    
    try:
        # Step 1: Scan the cube
        print("📹 Step 1: Scanning cube faces...")
        face_data = scanner.scan_all_faces()
        
        if not face_data:
            print("❌ Failed to scan cube. Please try again.")
            return
        
        # Step 2: Detect colors and build cube state
        print("\n🎨 Step 2: Detecting colors...")
        
        # Calibrate color detection
        detector.calibrate_from_centers(face_data)
        
        # IMPORTANT: Update cube state with the correct color mapping
        cube_state.update_color_mapping(detector.face_color_mapping)

        # Process each face - CRITICAL: Match scanner sequence exactly
        face_names = ['U', 'R', 'F', 'D', 'L', 'B']  # Same order as scanner
        
        for i, face_name in enumerate(face_names):
            # Get the scanned data in the same order as face_names
            face_key = f"face_{i+1}"  # Scanner stores as "face_1", "face_2", etc.
            
            if face_key not in face_data:
                print(f"❌ Missing data for {face_name} (key: {face_key})")
                return
            
            face_bgr_colors = face_data[face_key]
            
            # Convert BGR to color names
            face_colors = detector.process_face_colors(face_bgr_colors)
            
            # Set face in cube state
            success = cube_state.set_face(face_name, face_colors)
            if not success:
                print(f"❌ Failed to set colors for face {face_name}")
                return
            
            # Debug output
            detector.print_face_debug(face_name, face_colors)
        
        # DEBUG: Show detailed string generation
        print("\n🔍 DETAILED STRING GENERATION:")
        debug_string = cube_state.debug_string_generation()
        print(debug_string)
        
        # STEP 2.5: VISUALIZE THE SCANNED CUBE
        print("\n📱 Step 2.5: Visualizing scanned cube...")
        centers_valid = detector.visualize_cube_2d(cube_state)

        if not centers_valid:
            print("\n⚠️  WARNING: Center squares don't match expected positions!")
            print("💡 This usually means:")
            print("   • Cube was held in wrong orientation during scanning")
            print("   • Faces were scanned in wrong sequence")
            print("   • Color detection needs recalibration")
            
            response = input("\n🔄 Continue anyway? (y/N): ")
            if response.lower() != 'y':
                print("📹 Try scanning again with correct orientation")
                return

        # Step 3: Validate cube state
        print("\n🔍 Step 3: Validating cube state...")
        
        if not cube_state.validate():
            print("❌ Invalid cube state detected. Please try scanning again.")
            print("Make sure all faces are scanned correctly.")
            return
        
        print("✅ Cube state is valid!")
        
        # Debug: Show the cube string with face analysis
        print(f"\n🔤 Cube string analysis:")
        print(cube_state.get_cube_string_debug())
        
        # Step 4: Solve the cube
        print("\n🧠 Step 4: Computing optimal solution...")
        
        solution = solver.solve_cube(cube_state)
        
        if solution is None:
            print("❌ Failed to find a solution. The cube might be in an invalid state.")
            print("💡 TIP: Try re-scanning the cube, especially the center squares")
            return
        
        # Step 5: Present the solution
        print("\n🎉 Step 5: Solution ready!")
        
        if not solution:  # Empty list means already solved
            print("🎉 Congratulations! Your cube is already solved!")
            print("✨ No moves needed - you're done!")
            
            # Show solved cube summary
            solver.print_solution_summary(solution)
            
        else:
            # Show solution for scrambled cube
            print(f"🎉 Solution found: {solver.format_solution_compact(solution)}")
            print(f"📊 Move count: {len(solution)}")
            
            # Print detailed solution
            solver.print_solution_summary(solution)
            print()
            solver.explain_solution(solution)
        
        print(f"\n📝 QUICK REFERENCE:")
        if solution:
            print(f"🔄 Solution: {solver.format_solution_compact(solution)}")
            print(f"📊 Total moves: {len(solution)}")
        else:
            print(f"✅ Cube is already solved - no moves needed!")
        
        print("\n🎯 TIPS:")
        print("• Hold the cube with WHITE on top and GREEN facing you")
        print("• Clockwise means turning like a clock face")
        print("• Take your time - accuracy is more important than speed")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please try again or check your setup.")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up
        scanner.release_camera()
        print("\n👋 Thank you for using Rubik's Cube Solver!")


if __name__ == "__main__":
    main()
