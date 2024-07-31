#!/usr/bin/env python3

import sys
import datetime

def save_new_owner_pet_data_to_file(kto=None, co=None):
    # Get current date
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')

    # If kto or co are not provided, use input to take data
    if not kto:
        kto = input("Podaj kto: ").strip()
    if not co:
        co = input("Podaj co: ").strip()

    # Validate inputs
    if not kto or not co:
        print("Error: Both 'kto' and 'co' must be provided.")
        sys.exit(1)

    # Write to file
    with open('Kto_ma_co.txt', 'w') as file:
        file.write(f"{kto} ma {co} od {current_date}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate kto_ma_co.txt file.')
    parser.add_argument('--kto', type=str, help='Who has something')
    parser.add_argument('--co', type=str, help='What does someone have')

    args = parser.parse_args()
    save_new_owner_pet_data_to_file(kto=args.kto, co=args.co)

