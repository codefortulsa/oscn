import oscn
from pathlib import Path
import logging
import random

# Configure logging to show progress and any issues.
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Define the courts and case types to sample from.
COURTS = ["texas", "oklahoma", "tulsa", "cleveland"]
TYPES = list(set(["CJ", "CS", "CM", "CF", "SC"]))  # Use set to remove duplicate 'CM'.
YEAR = "2024"  # Use a recent year to increase the likelihood of finding cases.
SAMPLE_SIZE = 5
HTML_DIR = Path("data/html")
MAX_CASE_NUMBER = 5000


def save_sample_case_html():
    """
    Fetches a random sample of cases from specified courts and types,
    and saves the HTML content of each case to a file.
    """
    try:
        # Ensure the target directory for HTML files exists.
        HTML_DIR.mkdir(parents=True, exist_ok=True)
        logging.info(f"Data directory is ready at: {HTML_DIR.resolve()}")

        for court in COURTS:
            for case_type in TYPES:
                logging.info(
                    f"Fetching {SAMPLE_SIZE} random cases for court='{court}', type='{case_type}', year='{YEAR}'"
                )

                saved_count = 0
                total_attempts = 0
                # Limit attempts to prevent infinite loops if cases are sparse.
                max_attempts = SAMPLE_SIZE * 10

                while saved_count < SAMPLE_SIZE and total_attempts < max_attempts:
                    total_attempts += 1
                    number = random.randint(1, MAX_CASE_NUMBER)

                    # Retry logic for a single random number seed.
                    # It will try the random number, then half, then half of that, etc.
                    max_retries_per_seed = 15  # Safety break for the inner loop
                    for _ in range(max_retries_per_seed):
                        if number == 0:
                            logging.warning(
                                f"Retry number became 0 for {court}-{case_type}. Trying new random number."
                            )
                            break

                        logging.info(
                            f"Attempting to fetch case: {court}-{case_type}-{YEAR}-{number}"
                        )
                        case = oscn.request.Case(
                            county=court, type=case_type, year=YEAR, number=number
                        )

                        if case.text:
                            file_path = HTML_DIR / f"{case.index}.html"
                            logging.info(
                                f"Saving HTML for case: {case.index} -> {file_path}"
                            )
                            file_path.write_text(case.text, encoding="utf-8")
                            saved_count += 1
                            break  # Found a valid case, move to the next sample.
                        else:
                            logging.warning(
                                f"Case number {number} is invalid. Retrying with {int(number / 2)}."
                            )
                            number = int(number / 2)
                    else:  # This 'else' belongs to the for-loop, runs if the loop finishes without break
                        logging.warning(
                            f"Could not find a valid case for random seed after {max_retries_per_seed} retries."
                        )

                if saved_count < SAMPLE_SIZE and total_attempts >= max_attempts:
                    logging.warning(
                        f"Reached max attempts ({max_attempts}). Only saved {saved_count}/{SAMPLE_SIZE} cases for {court}-{case_type}-{YEAR}."
                    )

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}", exc_info=True)


if __name__ == "__main__":
    save_sample_case_html()
