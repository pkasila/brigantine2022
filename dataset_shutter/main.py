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


def get_pos(elem):
    x = elem.location['x']
    y = elem.location['y']
    w = elem.size['width']
    h = root.size['height']
    width = x + w
    height = y + h

    return {
        "x": x,
        "y": y,
        "width": width,
        "height": height
    }


def multiply_pos(pos, factor):
    return {
        "x": pos["x"] * factor,
        "y": pos["y"] * factor,
        "width": pos["width"] * factor,
        "height": pos["height"] * factor
    }


for idx in range(0, dataset['total']):
    driver.execute_script('dispatchEvent(new Event("renderNewFormula"))')
    formula = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "formula")))

    driver.save_screenshot(f'{args.out}/{idx}.png')

    root_pos = get_pos(root)
    formula_pos = get_pos(formula)

    im = Image.open(f'{args.out}/{idx}.png')
    im = im.crop((int(root_pos["x"]) * 2,
                  int(root_pos["y"]) * 2,
                  int(root_pos["width"]) * 2,
                  int(root_pos["height"]) * 2))
    im.save(f'{args.out}/{idx}.png')

    formula_pos["width"] = formula_pos["width"] - root_pos["x"]
    formula_pos["height"] = formula_pos["height"] - root_pos["y"]
    formula_pos["x"] -= root_pos["x"]
    formula_pos["y"] -= root_pos["y"]

    root_pos["width"] = root_pos["width"] - root_pos["x"]
    root_pos["height"] = root_pos["height"] - root_pos["y"]
    root_pos["x"] = 0
    root_pos["y"] = 0

    new_dataset.append({
        "file": f'{idx}.png',
        "text": multiply_pos(root_pos, 2),
        "formula": multiply_pos(formula_pos, 2)
    })
    print(f"{idx}.png")

with open(f'{args.out}/dataset.json', 'wb') as f:
    f.write(json.dumps(new_dataset, indent=2).encode('utf8'))

driver.quit()
