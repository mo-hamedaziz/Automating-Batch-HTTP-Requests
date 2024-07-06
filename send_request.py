import json
import requests
import argparse
from tabulate import tabulate
from tqdm import tqdm

def main():
    parser = argparse.ArgumentParser(description="Process REST API endpoints.")
    parser.add_argument("--base-url", dest="base_url", type=str, help="Base URL for the API endpoints")
    parser.add_argument("--targets", dest="targets_file", type=str, help="Path to the targets.json file")
    parser.add_argument("--export", dest="export_file", type=str, default=None,
                        help="Export results to a JSON file")
    args = parser.parse_args()

    base_url = args.base_url

    # Load endpoints from targets.json
    with open(args.targets_file, "r") as f:
        endpoints = json.load(f)

    results = []

    # Initialize tqdm progress bar
    pbar = tqdm(total=len(endpoints), desc="Processing Endpoints", unit="endpoint")

    for endpoint in endpoints:
        method = endpoint["method"]
        route = endpoint["route"]
        url = base_url + route
        try:
            if method == "GET":
                response = requests.get(url)
            elif method == "POST":
                response = requests.post(url)
            elif method == "PUT":
                response = requests.put(url)
            elif method == "DELETE":
                response = requests.delete(url)
            elif method == "PATCH":
                response = requests.patch(url)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            status_code = response.status_code
            results.append({"Route": route, "Method": method, "Status Code": status_code})
        except requests.exceptions.RequestException as e:
            results.append({"Route": route, "Method": method, "Error": str(e)})
        
        # Update progress bar
        pbar.update(1)

    # Close tqdm progress bar
    pbar.close()

    # Prepare metadata
    metadata = {
        "base_url": args.base_url,
        "targets_file": args.targets_file,
        "results_file": args.export_file if args.export_file else "stdout"
    }

    # Prepare export data structure
    export_data = {
        "metadata": metadata,
        "responses": results
    }

    # Export results to JSON file if export_file is specified
    if args.export_file:
        with open(args.export_file, "w") as json_file:
            json.dump(export_data, json_file, indent=4)
        print(f"Results exported to {args.export_file}")
    else:
        # Print results as a table
        print(tabulate(results, headers="keys", tablefmt="grid"))

if __name__ == "__main__":
    main()
