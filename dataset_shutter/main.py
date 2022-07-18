import json
import time

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
    width = elem.size['width']
    height = elem.size['height']

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
    driver.execute_script('window.renderNewFormula()')
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "formula_done")))
    formula = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "formula")))

    driver.save_screenshot(f'{args.out}/{idx}.png')

    root_pos = multiply_pos(get_pos(root), 2)
    formula_pos = multiply_pos(get_pos(formula), 2)

    new_dataset.append({
        "imagefilename": f'{idx}.png',
        "annotation": [
            {
                "coordinates": root_pos,
                "label": "text"
            },
            {
                "coordinates": formula_pos,
                "label": "formula"
            }
        ]
    })
    print(f"{idx}.png")

with open(f'{args.out}/dataset.json', 'wb') as f:
    f.write(json.dumps(new_dataset, indent=2).encode('utf8'))

driver.quit()
