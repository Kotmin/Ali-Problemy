#!/usr/bin/env python3

import argparse
from manager import OwnerPetManager



def main():
    parser = argparse.ArgumentParser(
        description='Generate kto_ma_co.txt file.')
    parser.add_argument('--kto', type=str, help='Who has something')
    parser.add_argument('--co', type=str, help='What does someone have')

    args = parser.parse_args()
    manager = OwnerPetManager()

    try:
        result = manager.save_new_owner_pet_data(owner=args.kto, pet=args.co)
        print("Saved:", result)
    except ValueError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
