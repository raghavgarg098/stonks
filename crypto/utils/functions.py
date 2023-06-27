def extract_percentage_value(percentage_string):
    try:
        # Remove the '%' symbol and any leading/trailing whitespace
        percentage_string = percentage_string.strip('%')
        # Convert the remaining string to a float
        percentage_value = float(percentage_string)
        return percentage_value
    except ValueError:
        # Handle the case when the input cannot be converted to a float
        return None


def extract_dollar_value(dollar_string):
    try:
        # Remove the '$' symbol and any commas
        dollar_string = dollar_string.replace('$', '').replace(',', '')
        # Convert the remaining string to a float
        dollar_value = float(dollar_string)
        return dollar_value
    except ValueError:
        # Handle the case when the input cannot be converted to a float
        return None


def extract_market_cap(combined_string):
    if combined_string == '--':
        return None

    try:
        # Find the index where the market cap value starts
        cap_index = combined_string.find('$') + 1

        # Extract the market cap value
        market_cap_string = combined_string[cap_index:]

        # Remove non-numeric characters (such as dots and commas) from the market cap string
        market_cap_string = ''.join(filter(str.isdigit, market_cap_string))

        # Convert the market cap value to a float
        market_cap = float(market_cap_string)

        # Check if the string contains trillion (T), billion (B), or million (M)
        if 'T' in combined_string:
            market_cap *= 1_000_000_000_000
        elif 'B' in combined_string:
            market_cap *= 1_000_000_000
        elif 'M' in combined_string:
            market_cap *= 1_000_000

        return int(market_cap)

    except (ValueError, IndexError):
        # Handle the case when the input cannot be converted or processed properly
        return None


def extract_numeric_volume(string):
    if string == '--':
        return None

    try:
        # Remove commas and any non-digit characters from the string
        numeric_string = ''.join(filter(str.isdigit, string))

        return numeric_string

    except ValueError:
        # Handle the case when the input cannot be converted to an integer
        return None

