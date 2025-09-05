# generate_image.py
import json
import random
import math

# --- Configuration ---
WIDTH = 800
HEIGHT = 400
BACKGROUND_COLOR = "#0D1117"
# This list of colors is essential for the colorful output
NEBULA_COLORS = ["#58A6FF", "#3FB950", "#F78166", "#A371F7"] # Blue, Green, Orange, Purple

# --- Main Generation Logic ---
def generate_universe():
    with open('contributions.json', 'r') as f:
        data = json.load(f)

    # Extract all contribution days into a single list
    all_days = []
    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    for week in weeks:
        all_days.extend(week["contributionDays"])

    svg_defs = []
    svg_elements = [f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{BACKGROUND_COLOR}"/>']
    
    # Generate a galaxy for each day with contributions
    total_days = len(all_days)
    for i, day in enumerate(all_days):
        count = day["contributionCount"]
        if count == 0:
            continue

        # --- Position the Galaxy ---
        x_pos = (i / total_days) * (WIDTH * 0.9) + (WIDTH * 0.05)
        y_pos = random.uniform(HEIGHT * 0.2, HEIGHT * 0.8)
        
        # --- Define the Galaxy's Appearance ---
        radius = 20 + math.log(count + 1) * 6
        core_opacity = 0.6 + (count / 20)
        core_opacity = min(1.0, core_opacity)
        
        # --- Create the SVG Elements ---
        unique_id = f"g{i}"
        # This line picks a random color from the list for each galaxy
        gradient_color = random.choice(NEBULA_COLORS)

        # This gradient uses the selected color
        gradient = f"""
        <radialGradient id="grad{unique_id}" cx="50%" cy="50%" r="50%">
          <stop offset="0%" style="stop-color:white; stop-opacity:{core_opacity:.2f}" />
          <stop offset="100%" style="stop-color:{gradient_color}; stop-opacity:0" />
        </radialGradient>
        """
        
        galaxy_circle = f'<circle cx="{x_pos:.2f}" cy="{y_pos:.2f}" r="{radius:.2f}" fill="url(#grad{unique_id})"/>'
        
        svg_defs.append(gradient)
        svg_elements.append(galaxy_circle)

    # --- Assemble the final SVG file ---
    svg_content = f"""
<svg width="{WIDTH}" height="{HEIGHT}" xmlns="http://www.w3.org/2000/svg">
  <defs>{''.join(svg_defs)}</defs>
  {''.join(svg_elements)}
</svg>
"""
    with open('universe.svg', 'w') as f:
        f.write(svg_content)
    
    print("Successfully generated universe.svg")

if __name__ == "__main__":
    generate_universe()
