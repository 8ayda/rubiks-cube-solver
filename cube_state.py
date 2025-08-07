"""
Cube State Module
================

Represents and manages the complete state of a Rubik's cube.
Handles color detection, validation, and conversion to standard notation.
"""

from typing import List, Dict, Optional, Tuple


class CubeState:
    """Represents the complete state of a Rubik's cube."""
    
    def __init__(self):
        """Initialize empty cube state."""
        # Store face data as 3x3 grids of color names
        self.faces = {
            'U': [['', '', ''], ['', '', ''], ['', '', '']],  # Up (top)
            'R': [['', '', ''], ['', '', ''], ['', '', '']],  # Right
            'F': [['', '', ''], ['', '', ''], ['', '', '']],  # Front
            'D': [['', '', ''], ['', '', ''], ['', '', '']],  # Down (bottom)
            'L': [['', '', ''], ['', '', ''], ['', '', '']],  # Left
            'B': [['', '', ''], ['', '', ''], ['', '', '']]   # Back
        }
        
        # This will be set based on detected center colors
        self.color_to_notation = {}
        
        # Default mapping (will be overridden by actual detection)
        self._default_color_mapping = {
            'white': 'U',
            'yellow': 'D',
            'red': 'R',
            'orange': 'L',
            'green': 'F',
            'blue': 'B'
        }
    
    def update_color_mapping(self, face_color_mapping: Dict[str, str]):
        """
        Update color-to-notation mapping based on detected center colors.
        
        Args:
            face_color_mapping: Dict mapping face notation (U,R,F,D,L,B) to color names
        """
        # Reverse the mapping: color -> notation
        self.color_to_notation = {}
        for face_notation, color_name in face_color_mapping.items():
            self.color_to_notation[color_name] = face_notation
        
        print(f"🎯 Updated color mapping: {self.color_to_notation}")
    
    def set_face(self, face_name: str, colors: List[List[str]]) -> bool:
        """
        Set the colors for a specific face.
        
        Args:
            face_name: Face identifier ('U', 'R', 'F', 'D', 'L', 'B')
            colors: 3x3 grid of color names
            
        Returns:
            True if successful, False otherwise
        """
        if face_name not in self.faces:
            print(f"❌ Invalid face name: {face_name}")
            return False
        
        if len(colors) != 3 or any(len(row) != 3 for row in colors):
            print(f"❌ Invalid color grid size for face {face_name}")
            return False
        
        self.faces[face_name] = [row[:] for row in colors]  # Deep copy
        return True
    
    def get_face(self, face_name: str) -> Optional[List[List[str]]]:
        """Get the colors for a specific face."""
        return self.faces.get(face_name)
    
    def get_center_colors(self) -> Dict[str, str]:
        """Get the center color of each face."""
        centers = {}
        for face_name, face_data in self.faces.items():
            if face_data[1][1]:  # Center square at position [1][1]
                centers[face_name] = face_data[1][1]
        return centers
    
    def to_kociemba_string(self) -> str:
        """
        Convert cube state to Kociemba algorithm format.
        
        Kociemba expects facelets in this exact order:
        U1-U9, R1-R9, F1-F9, D1-D9, L1-L9, B1-B9
        
        Each face is read left-to-right, top-to-bottom:
        1 2 3
        4 5 6  
        7 8 9
        """
        if not self.color_to_notation:
            print("❌ Color mapping not set. Using default mapping.")
            self.color_to_notation = self._default_color_mapping.copy()
        
        result = ""
        
        # Process faces in Kociemba order: U, R, F, D, L, B
        face_order = ['U', 'R', 'F', 'D', 'L', 'B']
        
        for face_name in face_order:
            face_data = self.faces[face_name]  # 3x3 grid
            
            # Convert 3x3 grid to 9 characters in correct order
            # Row 0: positions 1, 2, 3
            # Row 1: positions 4, 5, 6
            # Row 2: positions 7, 8, 9
            for row_idx in range(3):
                for col_idx in range(3):
                    color_name = face_data[row_idx][col_idx]
                    
                    if color_name not in self.color_to_notation:
                        print(f"❌ Unknown color: {color_name}")
                        print(f"Available mappings: {self.color_to_notation}")
                        return ""
                    
                    notation = self.color_to_notation[color_name]
                    result += notation
        
        return result
    
    def validate(self) -> bool:
        """
        Validate the cube state.
        
        Returns:
            True if valid, False otherwise
        """
        print("🔍 Validating cube state...")
        
        # Check that all faces have data
        for face_name in ['U', 'R', 'F', 'D', 'L', 'B']:
            if not self.faces[face_name]:
                print(f"❌ Face {face_name} has no data")
                return False
            
            # Check face structure
            face_data = self.faces[face_name]
            if len(face_data) != 3 or any(len(row) != 3 for row in face_data):
                print(f"❌ Face {face_name} has invalid structure")
                return False
        
        # Count total colors
        all_colors = []
        for face_data in self.faces.values():
            for row in face_data:
                for color in row:
                    if color:  # Skip empty strings
                        all_colors.append(color)
        
        # Count occurrences of each color
        color_counts = {}
        for color in all_colors:
            color_counts[color] = color_counts.get(color, 0) + 1
        
        print(f"📊 Total color distribution: {color_counts}")
        
        # Validate color distribution
        expected_colors = 6
        expected_count_per_color = 9
        
        if len(color_counts) != expected_colors:
            print(f"❌ Expected {expected_colors} colors, found {len(color_counts)}: {list(color_counts.keys())}")
            return False
        
        for color, count in color_counts.items():
            if count != expected_count_per_color:
                print(f"❌ Color '{color}' appears {count} times (expected {expected_count_per_color})")
                return False
        
        print("✅ Cube state validation passed!")
        return True
    
    def print_state(self):
        """Print a visual representation of the cube state."""
        print("\n🎲 CUBE STATE:")
        print("=" * 40)
        
        for face_name in ['U', 'R', 'F', 'D', 'L', 'B']:
            face_data = self.faces[face_name]
            print(f"\n{face_name} Face:")
            for row in face_data:
                row_str = " | ".join(f"{color:^8}" for color in row)
                print(f"  {row_str}")
    
    def debug_string_generation(self) -> str:
        """Debug the string generation process step by step."""
        print("\n🔍 DEBUG: STRING GENERATION PROCESS")
        print("=" * 50)
        
        if not self.color_to_notation:
            print("❌ No color mapping available!")
            return ""
        
        print(f"Color mapping: {self.color_to_notation}")
        print()
        
        result = ""
        face_order = ['U', 'R', 'F', 'D', 'L', 'B']
        
        for face_idx, face_name in enumerate(face_order):
            print(f"Face {face_name} (positions {face_idx*9 + 1}-{face_idx*9 + 9}):")
            face_data = self.faces[face_name]
            
            face_string = ""
            for row_idx in range(3):
                for col_idx in range(3):
                    color_name = face_data[row_idx][col_idx]
                    notation = self.color_to_notation.get(color_name, '?')
                    face_string += notation
                    
                    position = face_idx * 9 + row_idx * 3 + col_idx + 1
                    print(f"  Position {position:2d}: {color_name:8} -> {notation}")
            
            result += face_string
            print(f"  Face string: {face_string}")
            print()
        
        print(f"Final string: {result}")
        print(f"Length: {len(result)} (should be 54)")
        
        return result

    def get_cube_string_debug(self) -> str:
        """Get cube string with debug info."""
        cube_string = self.to_kociemba_string()
        
        print(f"Cube string: {cube_string}")
        print(f"Length: {len(cube_string)}")
        
        # Character frequency analysis
        char_counts = {}
        for char in cube_string:
            char_counts[char] = char_counts.get(char, 0) + 1
        
        print("Character frequency:")
        for char in sorted(char_counts.keys()):
            status = "✅" if char_counts[char] == 9 else "❌"
            print(f"  {char}: {char_counts[char]} times {status}")
        
        return cube_string
