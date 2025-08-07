#!/usr/bin/env python3
"""
Color Calibration Tool
======================

Scans a solved Rubik's cube to learn the exact HSV color values
for accurate color detection during solving.
"""

import cv2
import numpy as np
import json
from typing import Dict, List, Tuple
from cube_scanner import CubeScanner


class ColorCalibrator:
    """Calibrates colors by scanning a solved cube."""
    
    def __init__(self):
        """Initialize the color calibrator."""
        self.scanner = CubeScanner()
        self.learned_colors = {}
        
        # Standard Rubik's cube solved state - each face has uniform color
        self.solved_face_colors = {
            'U': 'white',   # Top face
            'R': 'red',     # Right face
            'F': 'green',   # Front face
            'D': 'yellow',  # Down face
            'L': 'orange',  # Left face
            'B': 'blue'     # Back face
        }
    
    def calibrate_from_solved_cube(self) -> Dict[str, Tuple[int, int, int]]:
        """
        Scan a solved cube to learn exact color values.
        Returns dictionary mapping color names to HSV values.
        """
        print("🎲 COLOR CALIBRATION MODE")
        print("=" * 50)
        print("This will scan your SOLVED Rubik's cube to learn the exact colors.")
        print("Make sure your cube is completely solved before starting!")
        print()
        print("You will scan each face. Since the cube is solved,")
        print("each face should show only ONE color on all 9 squares.")
        print("=" * 50)
        
        # Get user confirmation
        while True:
            response = input("\nIs your cube completely solved? (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                break
            elif response in ['n', 'no']:
                print("❌ Please solve your cube first and try again.")
                return {}
            else:
                print("Please enter 'y' for yes or 'n' for no.")
        
        print("\n📹 Starting calibration scan...")
        
        # Scan all faces
        face_data = self.scanner.scan_all_faces()
        
        if not face_data:
            print("❌ Failed to scan cube faces for calibration.")
            return {}
        
        # Process each face to extract color information
        learned_colors = {}
        face_names = ['U', 'R', 'F', 'D', 'L', 'B']
        
        print("\n🎨 Analyzing scanned colors...")
        
        for i, face_name in enumerate(face_names):
            if i < len(face_data):
                face_key = list(face_data.keys())[i]
                face_colors = face_data[face_key]
                
                # Since cube is solved, all squares should be the same color
                # Sample multiple squares and average them for better accuracy
                all_bgr_colors = []
                for row in face_colors:
                    for bgr_color in row:
                        all_bgr_colors.append(bgr_color)
                
                # Calculate average BGR color for this face
                avg_bgr = tuple(int(np.mean([color[i] for color in all_bgr_colors])) 
                               for i in range(3))
                
                # Convert to HSV
                avg_hsv = self._bgr_to_hsv(avg_bgr)
                
                # Store the learned color
                expected_color = self.solved_face_colors[face_name]
                learned_colors[expected_color] = avg_hsv
                
                print(f"  {face_name} face ({expected_color:^6}): BGR{avg_bgr} -> HSV{avg_hsv}")
        
        # Save calibration data
        self._save_calibration(learned_colors)
        
        print("\n✅ Color calibration complete!")
        print("🔧 These colors will now be used for cube solving.")
        
        return learned_colors
    
    def _bgr_to_hsv(self, bgr_color: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Convert BGR color to HSV."""
        bgr_array = np.uint8([[bgr_color]])
        hsv_array = cv2.cvtColor(bgr_array, cv2.COLOR_BGR2HSV)
        return tuple(int(x) for x in hsv_array[0][0])
    
    def _save_calibration(self, learned_colors: Dict[str, Tuple[int, int, int]]):
        """Save calibration data to file."""
        # Convert tuples to lists for JSON serialization
        calibration_data = {
            color: list(hsv) for color, hsv in learned_colors.items()
        }
        
        try:
            with open('color_calibration.json', 'w') as f:
                json.dump(calibration_data, f, indent=2)
            print(f"💾 Calibration saved to color_calibration.json")
        except Exception as e:
            print(f"⚠️  Could not save calibration: {e}")
    
    @staticmethod
    def load_calibration() -> Dict[str, Tuple[int, int, int]]:
        """Load calibration data from file."""
        try:
            with open('color_calibration.json', 'r') as f:
                calibration_data = json.load(f)
            
            # Convert lists back to tuples
            learned_colors = {
                color: tuple(hsv) for color, hsv in calibration_data.items()
            }
            
            print("📂 Loaded calibration from color_calibration.json")
            return learned_colors
            
        except FileNotFoundError:
            print("⚠️  No calibration file found. Run calibration first.")
            return {}
        except Exception as e:
            print(f"⚠️  Could not load calibration: {e}")
            return {}
    
    def print_calibration_summary(self, learned_colors: Dict[str, Tuple[int, int, int]]):
        """Print a summary of the learned colors."""
        print("\n📊 CALIBRATION SUMMARY:")
        print("-" * 30)
        for color, hsv in learned_colors.items():
            h, s, v = hsv
            print(f"  {color:^8}: H={h:3d}° S={s:3d} V={v:3d}")


def main():
    """Main calibration function."""
    calibrator = ColorCalibrator()
    
    try:
        learned_colors = calibrator.calibrate_from_solved_cube()
        
        if learned_colors:
            calibrator.print_calibration_summary(learned_colors)
            print("\n🎯 Calibration complete! You can now solve scrambled cubes.")
        else:
            print("❌ Calibration failed.")
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Calibration interrupted by user")
    except Exception as e:
        print(f"\n❌ An error occurred during calibration: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up
        calibrator.scanner.release_camera()


if __name__ == "__main__":
    main()