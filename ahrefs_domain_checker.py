from seleniumbase import SB
import json
import sys
import argparse

def check_domain_authority(domains):
    """Check Data"""
    all_results = []

    with SB(uc=True, test=True) as sb:
        url = "https://ahrefs.com/website-authority-checker/"
        sb.uc_open_with_reconnect(url, 5)

        for domain in domains:
            print(f"Checking domain: {domain}")

            # Clear input and type new domain
            sb.clear('input[type="text"]')
            sb.type('input[type="text"]', domain)
            sb.press_keys('input[type="text"]', "\n")
            sb.sleep(3)

            # Handle captcha if present
            sb.uc_gui_click_captcha()
            sb.sleep(2)

            # Wait for results modal to appear
            sb.wait_for_element('button[class*="closeButton"]', timeout=30)

            # Extract Domain Rating
            domain_rating = None
            try:
                value_spans = sb.find_elements('span')
                for span in value_spans:
                    text = span.text.strip()
                    if (text.isdigit() and len(text) <= 3 and text != "0"):
                        domain_rating = int(text)
                        break
            except Exception as e:
                print(f"Error extracting domain rating: {e}")

            # Extract Backlinks
            backlinks = None
            backlinks_dofollow_percentage = None
            try:
                all_text = sb.get_text('body')
                lines = all_text.split('\n')
                for line in lines:
                    line = line.strip()
                    if (('K' in line or 'M' in line) and
                        any(char.isdigit() for char in line) and
                        'Backlinks' in all_text):
                        import re
                        match = re.search(r'(\d+(?:\.\d+)?)([KM]?)', line)
                        if match:
                            num = float(match.group(1))
                            multiplier = match.group(2)
                            if multiplier == 'K':
                                backlinks = int(num * 1000)
                            elif multiplier == 'M':
                                backlinks = int(num * 1000000)
                            else:
                                backlinks = int(num)
                    elif ('%' in line and 'dofollow' in line and 'Backlinks' in all_text):
                        match = re.search(r'(\d+)', line)
                        if match:
                            backlinks_dofollow_percentage = int(match.group(1))
            except Exception as e:
                print(f"Error extracting backlinks: {e}")

            # Extract Linking Websites
            linking_websites = None
            linking_websites_dofollow_percentage = None
            try:
                all_text = sb.get_text('body')
                lines = all_text.split('\n')
                for line in lines:
                    line = line.strip()
                    if (line.isdigit() and len(line) <= 4 and int(line) > 10 and 'Linking websites' in all_text):
                        linking_websites = int(line)
                    elif ('%' in line and 'dofollow' in line and 'Linking websites' in all_text):
                        match = re.search(r'(\d+)', line)
                        if match:
                            linking_websites_dofollow_percentage = int(match.group(1))
            except Exception as e:
                print(f"Error extracting linking websites: {e}")

            # Create result data
            result_data = {
                "domain": domain,
                "domain_rating": domain_rating,
                "backlinks": backlinks,
                "backlinks_dofollow_percentage": backlinks_dofollow_percentage,
                "linking_websites": linking_websites,
                "linking_websites_dofollow_percentage": linking_websites_dofollow_percentage
            }

            all_results.append(result_data)

            # Close the modal
            try:
                sb.execute_script("document.querySelector('button[class*=\"closeButton\"]').click();")
                sb.sleep(1)
            except Exception as e:
                print(f"Error closing modal: {e}")

        # Print results
        print(json.dumps(all_results, indent=2))
        sb.post_message("SeleniumBase wasn't detected", duration=4)
        print(f"Success! Checked {len(domains)} domains without detection!")

def main():
    parser = argparse.ArgumentParser(description='Check Data')
    parser.add_argument('--data', type=str, required=True,
                       help='Comma-separated list of data to check')
    args = parser.parse_args()

    # Parse domains
    domains = [domain.strip() for domain in args.domains.split(',')]

    check_domain_authority(domains)

if __name__ == "__main__":
    main()