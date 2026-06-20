#!/usr/bin/env python3
"""
Generate an animated GIF of a 3D resume analyzer
"""

from PIL import Image, ImageDraw, ImageFont
import math

def create_resume_analyzer_gif(filename="static/resume_analyzer_3d.gif", duration=100, frames=36):
    """
    Create an animated GIF showing a 3D rotating resume analyzer
    """
    images = []
    width, height = 400, 500
    
    # Try to load a large bold font
    try:
        title_font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 36)
    except:
        try:
            title_font = ImageFont.truetype("C:\\Windows\\Fonts\\verdana.ttf", 36)
        except:
            title_font = ImageFont.load_default()
    
    for frame in range(frames):
        # Create a new image with gradient background
        img = Image.new('RGB', (width, height), color=(247, 251, 255))
        draw = ImageDraw.Draw(img, 'RGBA')
        
        # Calculate rotation angle
        angle = (frame / frames) * 360
        rad = math.radians(angle)
        
        # Draw background gradient effect
        for y in range(height):
            ratio = y / height
            r = int(247 + (220 - 247) * ratio)
            g = int(251 + (240 - 251) * ratio)
            b = int(255 + (255 - 255) * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Calculate 3D perspective
        center_x, center_y = width // 2, height // 2
        scale = 0.7 + 0.3 * math.cos(rad)
        
        # Draw paper document with 3D effect
        paper_width = int(120 * scale)
        paper_height = int(160 * scale)
        
        # Calculate skew for 3D rotation
        x_offset = int(60 * math.sin(rad))
        
        # Draw shadow
        shadow_alpha = int(40 * scale)
        shadow_width = max(40, paper_width + 40)
        draw.ellipse(
            [center_x - shadow_width//2 + x_offset, 
             center_y + paper_height//2,
             center_x + shadow_width//2 + x_offset,
             center_y + paper_height//2 + 20],
            fill=(0, 0, 0, shadow_alpha)
        )
        
        # Draw paper
        paper_color = int(230 + 25 * math.sin(rad * 2))
        draw.rectangle(
            [center_x - paper_width//2 + x_offset, 
             center_y - paper_height//2,
             center_x + paper_width//2 + x_offset,
             center_y + paper_height//2],
            fill=(255, 255, paper_color),
            outline=(200, 200, 220),
            width=2
        )
        
        # Draw lines on paper to represent text
        line_color = int(100 + 50 * math.sin(rad + frame * 0.2))
        line_spacing = int(12 * scale)
        
        for i in range(4):
            y_pos = center_y - paper_height//2 + 20 + i * line_spacing
            line_len = int(paper_width * (0.6 - i * 0.08))
            draw.line(
                [center_x - line_len//2 + x_offset, y_pos,
                 center_x + line_len//2 + x_offset, y_pos],
                fill=(line_color, line_color + 30, line_color + 60),
                width=2
            )
        
        # Draw rotating bars (skill indicators)
        bar_x = center_x - paper_width//4 + x_offset
        bar_y = center_y + paper_height//4
        bar_alpha = int(150 + 100 * math.sin(rad + i))
        
        for i in range(3):
            bar_width = int(abs(40 * (0.3 + 0.7 * math.sin(rad + i * 1.2))))
            bar_width = max(5, bar_width)  # Ensure minimum width
            colors = [
                (79, 114, 175, bar_alpha),
                (143, 188, 230, bar_alpha),
                (199, 215, 247, bar_alpha)
            ]
            draw.rectangle(
                [bar_x, bar_y + i * 16, bar_x + bar_width, bar_y + i * 16 + 10],
                fill=colors[i]
            )
        
        # Draw rotating badge
        badge_angle = rad * 2
        badge_x = int(center_x + 80 * math.cos(badge_angle))
        badge_y = int(center_y - 100 + 40 * math.sin(badge_angle))
        badge_size = max(5, int(20 + 10 * math.sin(badge_angle * 3)))
        
        draw.ellipse(
            [badge_x - badge_size//2, badge_y - badge_size//2,
             badge_x + badge_size//2, badge_y + badge_size//2],
            fill=(58, 210, 255, 180),
            outline=(15, 96, 252, 200),
            width=2
        )
        
        # Draw checkmark in badge
        if badge_size > 15:
            draw.line(
                [badge_x - 5, badge_y, badge_x - 2, badge_y + 4, badge_x + 6, badge_y - 5],
                fill=(255, 255, 255),
                width=2
            )
        
        # Draw title with highlight
        title_alpha = int(100 + 155 * math.sin(rad * 0.5 + 1))
        title_text = "Resume Analyzer"
        
        # Draw highlight box behind title (larger to fit bigger text)
        highlight_width = 280
        highlight_height = 50
        highlight_alpha = int(100 + 50 * math.sin(rad * 0.5 + 1))
        draw.rectangle(
            [width // 2 - highlight_width // 2, 10,
             width // 2 + highlight_width // 2, 60],
            fill=(143, 188, 230, highlight_alpha),
            outline=(79, 114, 175, 200),
            width=2
        )
        
        # Draw bold text multiple times with offsets for bold effect
        for offset_x in [-1, 0, 1]:
            for offset_y in [-1, 0, 1]:
                if offset_x != 0 or offset_y != 0:
                    draw.text(
                        (width // 2 + offset_x, 35 + offset_y),
                        title_text,
                        fill=(100, 150, 220, 200),
                        anchor="mm",
                        font=title_font
                    )
        
        # Draw main text in white
        draw.text(
            (width // 2, 35),
            title_text,
            fill=(255, 255, 255, 255),
            anchor="mm",
            font=title_font
        )
        
        # Draw progress indicator
        progress = (frame / frames)
        progress_width = int(200 * progress)
        draw.rectangle(
            [width // 2 - 100, height - 40, width // 2 - 100 + progress_width, height - 35],
            fill=(79, 114, 175)
        )
        draw.rectangle(
            [width // 2 - 100, height - 40, width // 2 + 100, height - 35],
            outline=(79, 114, 175),
            width=1
        )
        
        images.append(img)
    
    # Save as GIF
    images[0].save(
        filename,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0,
        optimize=False
    )
    print(f"✓ GIF created: {filename}")

if __name__ == "__main__":
    create_resume_analyzer_gif()
