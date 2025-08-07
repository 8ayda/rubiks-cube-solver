#!/usr/bin/env python3
"""
Cube Scanning Guide
==================
Shows the correct order and orientation for scanning cube faces.
"""

def show_scanning_guide():
    """Display the correct scanning procedure."""
    
    print("📹 CUBE SCANNING GUIDE")
    print("=" * 40)
    print("Follow this exact sequence for accurate scanning:")
    print()
    
    steps = [
        ("1️⃣ U Face (WHITE - Top)", 
         "Hold cube with WHITE on top, GREEN facing you\n" +
         "   Show the WHITE face to camera"),
        
        ("2️⃣ R Face (RED - Right)",
         "Keep WHITE on top, rotate cube LEFT 90°\n" +
         "   Now RED face is facing you - show to camera"),
        
        ("3️⃣ F Face (GREEN - Front)", 
         "Keep WHITE on top, rotate cube LEFT 90° again\n" +
         "   Now GREEN face is facing you - show to camera"),
        
        ("4️⃣ D Face (YELLOW - Bottom)",
         "Flip cube upside down (YELLOW now on top)\n" +
         "   Keep GREEN still facing you - show YELLOW to camera"),
        
        ("5️⃣ L Face (ORANGE - Left)",
         "Keep YELLOW on top, rotate cube RIGHT 90°\n" +
         "   Now ORANGE face is facing you - show to camera"),
        
        ("6️⃣ B Face (BLUE - Back)",
         "Keep YELLOW on top, rotate cube RIGHT 90° again\n" +
         "   Now BLUE face is facing you - show to camera")
    ]
    
    for step, instruction in steps:
        print(f"{step}")
        print(f"   {instruction}")
        print()
    
    print("🎯 IMPORTANT TIPS:")
    print("• Never rotate individual faces during scanning")
    print("• Only rotate the entire cube as a whole")
    print("• Keep movements smooth and deliberate")
    print("• Make sure camera sees the entire face clearly")
    print("• Don't move too fast between faces")
    print()
    
    print("❌ COMMON MISTAKES:")
    print("• Scanning faces in wrong order")
    print("• Losing track of cube orientation")
    print("• Rotating faces instead of whole cube")
    print("• Inconsistent lighting between scans")

if __name__ == "__main__":
    show_scanning_guide()