from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import math
import time

def get_canvas_info(driver, canvas):
    # Get canvas position and size using JavaScript
    rect = driver.execute_script("""
        var rect = arguments[0].getBoundingClientRect();
        return {
            'x': rect.x,
            'y': rect.y,
            'width': rect.width,
            'height': rect.height
        };
    """, canvas)
    
    return rect

def draw_circle(driver, canvas, canvas_info, num_points=100):
    actions = ActionChains(driver)
    
    # Calculate circle parameters
    center_x = canvas_info['width'] / 2
    center_y = canvas_info['height'] / 2
    radius = min(canvas_info['width'], canvas_info['height']) / 3
    
    # Calculate all points of the circle first
    points = []
    for i in range(num_points + 1):
        angle = 2 * math.pi * i / num_points
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        points.append((x, y))
    
    # Move to the first point
    first_point = points[0]
    actions.move_to_element(canvas)
    actions.move_by_offset(first_point[0] - canvas_info['width']/2, 
                         first_point[1] - canvas_info['height']/2)
    actions.click_and_hold()
    
    # Keep track of current position
    current_x = first_point[0]
    current_y = first_point[1]
    
    # Draw the circle by moving through each point continuously
    for x, y in points[1:]:
        # Calculate the relative movement from current position
        delta_x = x - current_x
        delta_y = y - current_y
        actions.move_by_offset(delta_x, delta_y)
        
        # Update current position
        current_x = x
        current_y = y
    
    actions.release()
    actions.perform()

def main():
    # Setup Chrome driver
    driver = webdriver.Chrome()
    driver.get("https://yage.ai/genai/pi.html")
    time.sleep(2)  # Wait for page to load
    
    # Get canvas element
    canvas = driver.find_element(By.ID, "drawingCanvas")
    
    # Get canvas information
    canvas_info = get_canvas_info(driver, canvas)
    print(f"Canvas info: {canvas_info}")
    
    # Draw circle
    draw_circle(driver, canvas, canvas_info)
    
    # Click calculate button
    calculate_btn = driver.find_element(By.ID, "calculateBtn")
    calculate_btn.click()
    
    # Wait for result and print it
    time.sleep(1)
    result = driver.find_element(By.ID, "result").text
    print(result)
    
    # Keep browser open for a few seconds to see the result
    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    main()