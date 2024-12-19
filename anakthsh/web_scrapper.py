import requests
from bs4 import BeautifulSoup
import json
from inverted_index import create_index

# Συνάρτηση για ανάκτηση και επεξεργασία των δεδομένων από τη Wikipedia
def fetch_wikipedia_data(url, all_data):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Ανάκτηση του τίτλου (προστασία αν δεν υπάρχει τίτλος)
        title_tag = soup.find('h1', id="firstHeading")
        title = title_tag.text if title_tag else "No Title Found"
        
        # Ανάκτηση όλων των παραγράφων του άρθρου
        paragraphs = soup.find_all('p')
        text_content = []
        for paragraph in paragraphs:
            text_content.append(paragraph.text.strip())
        
        # Δημιουργία ευρετηρίου για τις λέξεις
        # index = create_index(text_content)

        # Προσθήκη δεδομένων στο ενιαίο αρχείο
        all_data.append({
            "title": title,
            "content": text_content,
            # "index": index  # Αποθήκευση του ευρετηρίου
        })
        print(f"Data for {title} added to the collection.")
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")

# Συνάρτηση για αποθήκευση όλων των δεδομένων σε ένα αρχείο .json
def save_data_to_json(name, all_data):
    with open(name, "w", encoding="utf-8") as json_file:
        json.dump(all_data, json_file, ensure_ascii=False, indent=4)
    print(f"Saving data to {name}")

# Συνάρτηση για να διαβάσει τα URLs από το αρχείο links.txt
def read_urls_from_file():
    try:
        with open('links.txt', 'r') as file:
            urls = file.readlines()
        # Αφαιρούμε τα κενά και τα \n από το τέλος κάθε γραμμής
        urls = [url.strip() for url in urls]
        return urls
    except FileNotFoundError:
        print("File links.txt not found.")
        return []
    
def from_json_to_str(inp):
    documents = list()
    for document in inp:
        paragraphs = str()
        for paragraph in document['content']:
            paragraphs = paragraphs + paragraph + '\n'
        documents.append((paragraphs))  
    return documents

# Κύρια συνάρτηση που ζητάει URLs από τον χρήστη ή διαβάζει από το αρχείο
def web_scrapper():
    all_data = []  # Λίστα που θα κρατάει όλα τα δεδομένα
    print("Choose an option:")
    print("1. Enter URLs manually.")
    print("2. Read URLs from links.txt.")
    print("Type 'STOP' to stop the scraping and save the data.")

    while True:
        choice = input("Enter your choice (1/2): ").strip()
        if choice == '1':
            # Εισαγωγή URLs χειροκίνητα
            while True:
                url = input("Enter URL (or type 'STOP' to stop): ")
                if url.strip().upper() == 'STOP':
                    print("Stopping.")
                    return  # Exit the loop for manual URL input
                # Ensure the URL starts with 'https://en.wikipedia.org/wiki/'
                if not url.startswith('https://en.wikipedia.org/wiki/'):
                    print("Please enter a valid Wikipedia article URL (starting with 'https://en.wikipedia.org/wiki/').")
                    continue
                fetch_wikipedia_data(url, all_data)
                # Αποθήκευση όλων των δεδομένων στο τέλος
                if all_data:
                    print("Saving data.")
                    save_data_to_json("all_wikipedia_data.json",all_data)
                    save_data_to_json("all_wikipedia_index.json",create_index(from_json_to_str(all_data)))
                else:
                    print("No data to save.")

        
        elif choice == '2':
            # Ανάγνωση URLs από το αρχείο links.txt
            urls = read_urls_from_file()
            if not urls:
                print("No URLs found in links.txt. Please ensure the file exists and contains URLs.")
                break
            for url in urls:
                fetch_wikipedia_data(url, all_data)
                # Αποθήκευση όλων των δεδομένων στο τέλος
                if all_data:
                    print("Saving data.")
                    save_data_to_json("all_wikipedia_data.json",all_data)
                    save_data_to_json("all_wikipedia_index.json",create_index(from_json_to_str(all_data)))
                else:
                    print("No data to save.")

        elif choice.strip().upper() == 'STOP':
            print("Stopping.")
            break  # Exit the loop when 'STOP' is entered
        else:
            print("Invalid choice. Please choose 1 or 2.")

   
def main():
    web_scrapper();

if __name__ == "__main__":
    main()
