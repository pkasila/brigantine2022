import json

from selenium import webdriver
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse

# Parse arguments
parser = argparse.ArgumentParser("dataset_shutter")
parser.add_argument("http", help="URL at which renderer is working", type=str)
parser.add_argument("out", help="Output directory for dataset", type=str)
parser.add_argument("dataset", help="Path to dataset", type=str)
args = parser.parse_args()

dataset = json.load(open(args.dataset, 'rb'))

driver = webdriver.Safari()

driver.get(args.http)

root = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "root")))

new_dataset = []

for idx in range(0, dataset['total']):
    driver.execute_script('dispatchEvent(new Event("renderNewFormula"))')
    formula = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "formula")))

    driver.save_screenshot(f'{args.out}/{idx}.png')

    location = root.location
    size = root.size

    x = location['x']
    y = location['y']
    w = size['width']
    h = size['height']
    width = x + w
    height = y + h

    root_pos = {
        "x": x,
        "y": y,
        "width": width,
        "height": height
    }

    location = formula.location
    size = formula.size

    x = location['x'] - root_pos['x']
    y = location['y'] - root_pos['y']
    w = size['width']
    h = size['height']
    width = x + w
    height = y + h

    formula_pos = {
        "x": x,
        "y": y,
        "width": width,
        "height": height
    }

    im = Image.open(f'{args.out}/{idx}.png')
    im = im.crop((int(x) * 2, int(y) * 2, int(width) * 2, int(height) * 2))
    im.save(f'{args.out}/{idx}.png')

    new_dataset.append({
        "file": f'{idx}.png',
        "text": root_pos,
        "formula": formula_pos
    })
    print(f"{idx}.png")

with open(f'{args.out}/dataset.json', 'wb') as f:
    f.write(json.dumps(new_dataset, indent=2).encode('utf8'))

driver.close()
driver.quit()
