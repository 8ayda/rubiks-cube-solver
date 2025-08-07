"""
Cube Scanner Module
==================

Handles webcam input and cube face detection using computer vision.
Provides real-time guidance for proper cube scanning sequence.
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional
import time


class CubeScanner:
    """Handles webcam scanning of Rubik's cube faces with real-time guidance."""
    
    def __init__(self, camera_index: int = 0):
        """Initialize the cube scanner."""
        self.camera_index = camera_index
        self.cap = None
        self.grid_size = 3
        
        # Scanning guidance
        self.face_sequence = [
            {
                'name': 'U',
                'color': 'WHITE',
                'position': 'Top',
                'instruction': 'Hold cube with WHITE on top, GREEN facing you.\nShow the WHITE face to camera.',
                'tips': 'Keep cube steady. Make sure all 9 squares are visible.'
            },
            {
                'name': 'R', 
                'color': 'RED',
                'position': 'Right',
                'instruction': 'Keep WHITE on top, rotate cube LEFT 90°.\nNow RED face is facing you - show to camera.',
                'tips': 'White should still be on top. Red face now faces camera.'
            },
            {
                'name': 'F',
                'color': 'GREEN', 
                'position': 'Front',
                'instruction': 'Keep WHITE on top, rotate cube LEFT 90° again.\nNow GREEN face is facing you - show to camera.',
                'tips': 'White still on top. Green face now faces camera.'
            },
            {
                'name': 'D',
                'color': 'YELLOW',
                'position': 'Bottom', 
                'instruction': 'Flip cube upside down (YELLOW now on top).\nKeep GREEN still facing you - show YELLOW to camera.',
                'tips': 'Yellow on top now. Green should still face you.'
            },
            {
                'name': 'L',
                'color': 'ORANGE',
                'position': 'Left',
                'instruction': 'Keep YELLOW on top, rotate cube RIGHT 90°.\nNow ORANGE face is facing you - show to camera.',
                'tips': 'Yellow still on top. Orange face now faces camera.'
            },
            {
                'name': 'B',
                'color': 'BLUE',
                'position': 'Back',
                'instruction': 'Keep YELLOW on top, rotate cube RIGHT 90° again.\nNow BLUE face is facing you - show to camera.',
                'tips': 'Yellow still on top. Blue face now faces camera.'
            }
        ]
        
        self.current_face_index = 0
        self.scanned_faces = {}
    
    def initialize_camera(self) -> bool:
        """Initialize the camera."""
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                print("❌ Could not open camera")
                return False
            
            # Set camera properties for better quality
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            print("✅ Camera initialized successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize camera: {e}")
            return False
    
    def release_camera(self):
        """Release the camera."""
        if self.cap:
            self.cap.release()
            cv2.destroyAllWindows()
            print("📹 Camera released.")
    
    def draw_grid(self, frame: np.ndarray) -> np.ndarray:
        """Draw a 3x3 grid overlay on the frame."""
        h, w = frame.shape[:2]
        
        # Calculate grid dimensions (centered square)
        size = min(h, w) - 100  # Leave margin
        start_x = (w - size) // 2
        start_y = (h - size) // 2
        
        cell_size = size // 3
        
        # Draw grid lines
        color = (0, 255, 0)  # Green
        thickness = 2
        
        # Vertical lines
        for i in range(4):
            x = start_x + i * cell_size
            cv2.line(frame, (x, start_y), (x, start_y + size), color, thickness)
        
        # Horizontal lines  
        for i in range(4):
            y = start_y + i * cell_size
            cv2.line(frame, (start_x, y), (start_x + size, y), color, thickness)
        
        return frame, (start_x, start_y, cell_size)
    
    def draw_instructions(self, frame: np.ndarray, face_info: dict) -> np.ndarray:
        """Draw scanning instructions on the frame."""
        h, w = frame.shape[:2]
        
        # Semi-transparent overlay for text background
        overlay = frame.copy()
        
        # Top instruction panel
        cv2.rectangle(overlay, (0, 0), (w, 120), (0, 0, 0), -1)
        
        # Bottom tips panel
        cv2.rectangle(overlay, (0, h-80), (w, h), (0, 0, 0), -1)
        
        # Blend overlay
        frame = cv2.addWeighted(frame, 0.7, overlay, 0.3, 0)
        
        # Current face info
        face_title = f"Face {self.current_face_index + 1}/6: {face_info['name']} ({face_info['color']} - {face_info['position']})"
        cv2.putText(frame, face_title, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        # Instructions (multi-line)
        instruction_lines = face_info['instruction'].split('\n')
        for i, line in enumerate(instruction_lines):
            cv2.putText(frame, line, (10, 50 + i*25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Tips at bottom
        cv2.putText(frame, f"Tips: {face_info['tips']}", (10, h-50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # Controls
        cv2.putText(frame, "SPACE: Capture Face | ESC: Exit | R: Reset", (10, h-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        # Progress indicator
        progress_text = f"Progress: {len(self.scanned_faces)}/6 faces completed"
        cv2.putText(frame, progress_text, (w-300, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return frame
    
    def extract_colors(self, frame: np.ndarray, grid_info: tuple) -> List[List[Tuple[int, int, int]]]:
        """Extract colors from the 3x3 grid."""
        start_x, start_y, cell_size = grid_info
        colors = []
        
        for row in range(3):
            color_row = []
            for col in range(3):
                # Calculate center of each cell
                center_x = start_x + col * cell_size + cell_size // 2
                center_y = start_y + row * cell_size + cell_size // 2
                
                # Sample a small area around the center
                sample_size = 20
                x1 = max(0, center_x - sample_size)
                x2 = min(frame.shape[1], center_x + sample_size)
                y1 = max(0, center_y - sample_size)
                y2 = min(frame.shape[0], center_y + sample_size)
                
                # Extract color sample
                sample = frame[y1:y2, x1:x2]
                if sample.size > 0:
                    # Get average color (BGR format)
                    avg_color = tuple(map(int, np.mean(sample.reshape(-1, 3), axis=0)))
                    color_row.append(avg_color)
                else:
                    color_row.append((0, 0, 0))
            
            colors.append(color_row)
        
        return colors
    
    def scan_face(self, face_info: dict) -> Optional[List[List[Tuple[int, int, int]]]]:
        """Scan a single face with guided instructions."""
        print(f"\n📹 Scanning {face_info['name']} face ({face_info['color']})...")
        print(f"💡 {face_info['instruction']}")
        print("Press SPACE to capture when ready, ESC to exit")
        
        if not self.cap:
            if not self.initialize_camera():
                return None
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("❌ Failed to read from camera")
                return None
            
            # Mirror the image for better user experience
            frame = cv2.flip(frame, 1)
            
            # Draw grid overlay
            frame_with_grid, grid_info = self.draw_grid(frame)
            
            # Draw instructions
            frame_with_instructions = self.draw_instructions(frame_with_grid, face_info)
            
            # Show the frame
            cv2.imshow('Rubik\'s Cube Scanner - Follow Instructions', frame_with_instructions)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord(' '):  # Space to capture
                # Extract colors
                colors = self.extract_colors(frame, grid_info)
                print(f"✅ {face_info['name']} face captured!")
                
                # Show preview of captured colors
                self.show_color_preview(colors, face_info)
                
                return colors
                
            elif key == 27:  # ESC to exit
                print("❌ Scanning cancelled by user")
                return None
            
            elif key == ord('r'):  # R to reset
                print("🔄 Resetting scan sequence...")
                self.current_face_index = 0
                self.scanned_faces = {}
                return self.scan_all_faces()
    
    def show_color_preview(self, colors: List[List[Tuple[int, int, int]]], face_info: dict):
        """Show a preview of captured colors."""
        print(f"📊 Captured colors for {face_info['name']} face:")
        for i, row in enumerate(colors):
            row_colors = [f"BGR{color}" for color in row]
            print(f"  Row {i+1}: {' | '.join(row_colors)}")
    
    def scan_all_faces(self) -> Optional[Dict[str, List[List[Tuple[int, int, int]]]]]:
        """Scan all six faces of the cube with guided instructions."""
        print("🎲 RUBIK'S CUBE SCANNER WITH GUIDED INSTRUCTIONS")
        print("=" * 60)
        print("Follow the on-screen instructions for each face")
        print("Make sure to maintain proper cube orientation!")
        print()
        
        if not self.initialize_camera():
            return None
        
        self.current_face_index = 0
        self.scanned_faces = {}
        
        # Show initial setup instructions
        self.show_setup_instructions()
        
        try:
            for i, face_info in enumerate(self.face_sequence):
                self.current_face_index = i
                
                print(f"\n{'='*50}")
                print(f"STEP {i+1}/6: Scanning {face_info['name']} face")
                print(f"{'='*50}")
                
                colors = self.scan_face(face_info)
                if colors is None:
                    return None
                
                self.scanned_faces[f"face_{i+1}"] = colors
                
                # Brief pause between faces
                if i < len(self.face_sequence) - 1:
                    print("⏳ Get ready for next face...")
                    time.sleep(1)
            
            print("\n🎉 All faces scanned successfully!")
            print(f"📊 Total faces captured: {len(self.scanned_faces)}")
            
            return self.scanned_faces
            
        except Exception as e:
            print(f"❌ Error during scanning: {e}")
            return None
    
    def show_setup_instructions(self):
        """Show initial setup instructions."""
        print("📋 SETUP INSTRUCTIONS:")
        print("1. Make sure your cube is properly scrambled")
        print("2. Have good lighting (avoid shadows)")
        print("3. Hold cube steady during each capture")
        print("4. Start with WHITE on top, GREEN facing you")
        print("5. Follow the on-screen guidance for each face")
        print("\nPress any key when ready...")
        
        # Wait for user to be ready
        if self.cap:
            while True:
                ret, frame = self.cap.read()
                if ret:
                    frame = cv2.flip(frame, 1)
                    cv2.putText(frame, "GET READY - Press any key to start", 
                              (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame, "Position: WHITE on top, GREEN facing you", 
                              (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                    cv2.imshow('Rubik\'s Cube Scanner - Setup', frame)
                    
                    if cv2.waitKey(1) != -1:  # Any key pressed
                        break
        
        print("🚀 Starting guided scan sequence...")
