import os

def remove_duplicates(input_file, output_file):
    # Read all configs from the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split the content into individual configs
    configs = content.split('`\n')

    # Remove duplicates while preserving order
    unique_configs = []
    seen = set()
    for config in configs:
        config = config.strip()
        if config and config not in seen:
            unique_configs.append(config)
            seen.add(config)

    # Write unique configs to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        for config in unique_configs:
            f.write(f"{config}`\n")

    print(f"Removed {len(configs) - len(unique_configs)} duplicate configs.")
    print(f"Saved {len(unique_configs)} unique configs to {output_file}")

if __name__ == '__main__':
    input_file = 'config.txt'
    output_file = 'config.txt'

    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
    else:
        remove_duplicates(input_file, output_file)
        # Replace the original file with the unique configs
        os.replace(output_file, input_file)
