from weatherBox import weatherBox
import os


def parse_records(records_str: str) -> list[str]:
    # Each token is formatted as e.g. "95.01962" — strip the trailing 4-digit year
    return [item[:-4] for item in records_str.split()] if records_str.strip() else []


if __name__ == '__main__':
    file_path = input("File path: ")
    location = input("Location: ")
    state = input("State: ")
    begin_year = input("Begin year: ")
    end_year = input("End year (blank for 'por'): ")
    end_year = "por" if end_year == '' else end_year
    record_high_input = input("Record highs: ")
    record_low_input = input("Record lows: ")
    nowdata_url = input("NOWData url: ")
    pdf_url = input("PDF url: ")

    col_map = {2: 'precipitation', 3: 'snow', 4: 'mean', 5: 'high', 6: 'low'}

    precips, snows, highs, lows, means = [], [], [], [], []

    with open(file_path, newline='') as climate_data:
        climate_data.readline()
        for row in climate_data:
            split_row = row.split(",")
            for i, category in col_map.items():
                if i >= len(split_row):
                    continue
                val = split_row[i].replace(' ', '').replace('"', '').replace('\n', '')
                match category:
                    case 'precipitation':
                        precips.append(val)
                    case 'snow':
                        if val:
                            snows.append(val)
                    case 'mean':
                        means.append(val)
                    case 'high':
                        highs.append(val)
                    case 'low':
                        lows.append(val)

    highs.append(f'{sum(float(x) for x in highs) / 12:.1f}')
    means.append(f'{sum(float(x) for x in means) / 12:.1f}')
    lows.append(f'{sum(float(x) for x in lows) / 12:.1f}')
    precips.append(f'{sum(float(x) for x in precips):.2f}')
    if snows:
        snows.append(f'{sum(float(x) for x in snows):.1f}')

    record_highs = parse_records(record_high_input)
    record_lows = parse_records(record_low_input)

    box = weatherBox()
    box.Americanize()

    location_str = f'{location}, {state}' if state else location
    box.setHeader(location_str, f'{begin_year}–{end_year}')

    if record_highs:
        box.setRecordHighs(record_highs)
    box.setMaxTemps(highs)
    box.setMeanTemps(means)
    box.setMinTemps(lows)
    if record_lows:
        box.setRecordLows(record_lows)
    box.setPrecip(precips)
    if snows:
        box.setSnowfall(snows)

    title = f'{location_str} Climate Data'
    box.setFooter(nowdata_url, title, "National Oceanic and Atmospheric Administration")
    box.setFooter2(pdf_url, title, "National Oceanic and Atmospheric Administration", format="PDF")

    if state:
        output_dir = os.path.join(os.getcwd(), state)
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, f'{location}.txt')
    else:
        path = f'{location}.txt'

    with open(path, 'w') as f:
        print(str(box), file=f)
