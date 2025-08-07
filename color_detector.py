"""
Robust Color Detector
====================
Actually works properly with proper color classification.
"""

import cv2
import numpy as np
import json
from typing import List, Tuple, Dict


class ColorDetector:
    """Actually working color detector."""
    
    def __init__(self):
        """Initialize with robust color detection."""
        self.calibrated_hsv = {
            "white": (13, 11, 212),
            "red": (178, 224, 211),
            "green": (71, 242, 154),
            "yellow": (24, 255, 229),
            "orange": (7, 246, 227),
            "blue": (110, 241, 183)
        }
        
        self.face_color_mapping = {
            'U': 'white', 'R': 'red', 'F': 'green',
            'D': 'yellow', 'L': 'orange', 'B': 'blue'
        }
        
        print("✅ Using calibrated HSV values:")
        for color, hsv in self.calibrated_hsv.items():
            print(f"  {color:>8}: HSV{hsv}")
    
    def detect_color(self, bgr_color: Tuple[int, int, int]) -> str:
        """Enhanced detection with proper red/orange separation."""
        hsv_color = self._bgr_to_hsv(bgr_color)
        h, s, v = hsv_color
        
        # Rule 1: White detection (very low saturation)
        if s < 30 and v > 150:
            return 'white'
        
        # Rule 2: Blue detection (high saturation + blue hue range)
        if s > 150 and 100 <= h <= 130:
            return 'blue'
        
        # Rule 3: Green detection
        if s > 100 and 55 <= h <= 85:
            return 'green'
        
        # Rule 4: Yellow vs Orange vs Red separation (CRITICAL!)
        if s > 150:  # High saturation colors
            if 20 <= h <= 35:  # Yellow territory
                return 'yellow'
            elif 5 <= h <= 19:  # Orange territory (narrow range)
                return 'orange'
            elif h >= 170:  # Red territory (high hue only)
                return 'red'
            elif h <= 4:  # Very low hue could be red or orange
                # Use calibrated distance to decide
                red_dist = self._hsv_distance(hsv_color, self.calibrated_hsv['red'])
                orange_dist = self._hsv_distance(hsv_color, self.calibrated_hsv['orange'])
                return 'red' if red_dist < orange_dist else 'orange'
    
        # Fallback to distance-based detection for edge cases
        min_distance = float('inf')
        closest_color = 'white'
        
        for color_name, ref_hsv in self.calibrated_hsv.items():
            distance = self._hsv_distance(hsv_color, ref_hsv)
            
            if distance < min_distance:
                min_distance = distance
                closest_color = color_name
        
        return closest_color
    
    def _bgr_to_hsv(self, bgr_color: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Convert BGR to HSV."""
        bgr_array = np.uint8([[bgr_color]])
        hsv_array = cv2.cvtColor(bgr_array, cv2.COLOR_BGR2HSV)
        return tuple(int(x) for x in hsv_array[0][0])
    
    def _hsv_distance(self, hsv1: Tuple[int, int, int], hsv2: Tuple[int, int, int]) -> float:
        """Calculate HSV distance with special handling for red/orange."""
        h1, s1, v1 = hsv1
        h2, s2, v2 = hsv2
        
        # Handle hue wraparound (0-179)
        hue_diff = min(abs(h1 - h2), 180 - abs(h1 - h2))
        sat_diff = abs(s1 - s2)
        val_diff = abs(v1 - v2)
        
        # White detection: saturation is most important
        if s1 < 50 or s2 < 50:
            return hue_diff * 1.0 + sat_diff * 3.0 + val_diff * 0.5
        
        # Red/Orange separation: value becomes more important
        if (h1 >= 160 or h1 <= 30) and (h2 >= 160 or h2 <= 30):
            return hue_diff * 1.5 + sat_diff * 0.5 + val_diff * 1.0
        
        # Normal distance for other colors
        return hue_diff * 2.0 + sat_diff * 0.8 + val_diff * 0.3
    
    def calibrate_from_centers(self, face_data: Dict) -> bool:
        """Calibration is hardcoded."""
        print("✅ Using hardcoded calibrated HSV values")
        return True
    
    def process_face_colors(self, face_bgr_colors: List[List[Tuple[int, int, int]]]) -> List[List[str]]:
        """Convert face colors using calibrated detection."""
        result = []
        for row in face_bgr_colors:
            color_row = []
            for bgr in row:
                color = self.detect_color(bgr)
                color_row.append(color)
            result.append(color_row)
        return result
    
    def print_face_debug(self, face_name: str, face_colors: List[List[str]]):
        """Debug output."""
        print(f"  {face_name} face:")
        for i, row in enumerate(face_colors):
            print(f"    Row {i+1}: {' '.join(f'{c:8}' for c in row)}")
        
        # Count colors
        all_colors = [color for row in face_colors for color in row]
        color_counts = {}
        for color in all_colors:
            color_counts[color] = color_counts.get(color, 0) + 1
        
        print(f"    Distribution: {color_counts}")
        print(f"    Center: {face_colors[1][1]}")
    
    def visualize_cube_2d(self, cube_state):
        """Create a 2D representation of the scanned cube."""
        print("\n" + "="*60)
        print("🎲 2D CUBE VISUALIZATION - What Was Scanned")
        print("="*60)
        
        # Get face data from cube state
        faces = cube_state.faces
        
        # Color to emoji mapping for better visualization
        color_emojis = {
            'white': '⬜', 'red': '🟥', 'green': '🟩',
            'yellow': '🟨', 'orange': '🟧', 'blue': '🟦'
        }
        
        # Color to letter mapping (backup)
        color_letters = {
            'white': 'W', 'red': 'R', 'green': 'G',
            'yellow': 'Y', 'orange': 'O', 'blue': 'B'
        }
        
        def format_square(color):
            """Format a square with emoji if available."""
            return color_emojis.get(color, color_letters.get(color, '?'))
        
        # Standard cube net layout:
        #       [U]
        #   [L] [F] [R] [B]
        #       [D]
        
        print("\n    🔝 TOP (U - White)")
        print("    " + "-"*13)
        for row in faces['U']:
            line = "    | "
            for color in row:
                line += format_square(color) + " "
            line += "|"
            print(line)
        print("    " + "-"*13)
        
        print("\n🔄 MIDDLE ROW - Left to Right view")
        print("+" + "-"*13 + "+" + "-"*13 + "+" + "-"*13 + "+" + "-"*13 + "+")
        print("| 🟧 LEFT (L) | 🟩 FRONT(F) | 🟥 RIGHT(R) | 🟦 BACK (B) |")
        print("+" + "-"*13 + "+" + "-"*13 + "+" + "-"*13 + "+" + "-"*13 + "+")
        
        for row_idx in range(3):
            line = "| "
            
            # Left face (L)
            for color in faces['L'][row_idx]:
                line += format_square(color) + " "
            line += "| "
            
            # Front face (F) 
            for color in faces['F'][row_idx]:
                line += format_square(color) + " "
            line += "| "
            
            # Right face (R)
            for color in faces['R'][row_idx]:
                line += format_square(color) + " "
            line += "| "
            
            # Back face (B)
            for color in faces['B'][row_idx]:
                line += format_square(color) + " "
            line += "|"
            
            print(line)
        
        print("+" + "-"*13 + "+" + "-"*13 + "+" + "-"*13 + "+" + "-"*13 + "+")
        
        print("\n    🔻 BOTTOM (D - Yellow)")
        print("    " + "-"*13)
        for row in faces['D']:
            line = "    | "
            for color in row:
                line += format_square(color) + " "
            line += "|"
            print(line)
        print("    " + "-"*13)
        
        # Show centers for validation
        print("\n🎯 CENTER SQUARES ANALYSIS:")
        centers = {
            'U': faces['U'][1][1],  # Center of U face
            'R': faces['R'][1][1],  # Center of R face
            'F': faces['F'][1][1],  # Center of F face  
            'D': faces['D'][1][1],  # Center of D face
            'L': faces['L'][1][1],  # Center of L face
            'B': faces['B'][1][1]   # Center of B face
        }
        
        expected_centers = {
            'U': 'white', 'R': 'red', 'F': 'green',
            'D': 'yellow', 'L': 'orange', 'B': 'blue'
        }
        
        for face, detected_color in centers.items():
            expected_color = expected_centers[face]
            emoji = format_square(detected_color)
            if detected_color == expected_color:
                status = "✅"
            else:
                status = "❌"
            print(f"  Face {face}: {emoji} {detected_color:>8} {status} (should be {expected_color})")
        
        # Color distribution summary
        print("\n📊 COLOR DISTRIBUTION:")
        all_colors = []
        for face_data in faces.values():
            for row in face_data:
                all_colors.extend(row)
        
        color_counts = {}
        for color in all_colors:
            color_counts[color] = color_counts.get(color, 0) + 1
        
        for color, count in color_counts.items():
            emoji = format_square(color)
            status = "✅" if count == 9 else "❌"
            print(f"  {emoji} {color:>8}: {count:2d} squares {status}")
        
        print("="*60)
        
        return centers == expected_centers
