import requests
import os
import urllib.request
from urllib.parse import quote

# List of art forms, states, and Wikimedia Commons categories/search terms
art_forms = [
    ("Kalamkari", "andhrapradesh", "Category:Kalamkari", "Kalamkari Indian art"),
    ("Thangka Painting", "arunachalpradesh", "Category:Thangka", "Thangka Indian Buddhist art"),
    ("Sattriya Art", "assam", "Category:Assamese art", "Sattriya manuscript art"),
    ("Madhubani Painting", "bihar", "Category:Madhubani art", "Madhubani painting"),
    ("Bastar Art", "chhattisgarh", "Category:Bastar art", "Bastar tribal art"),
    ("Goan Christian Art", "goa", "Category:Christian art in India", "Goan Christian church art"),
    ("Pithora Painting", "gujarat", "Category:Pithora art", "Pithora tribal painting"),
    ("Sanji Wall Art", "haryana", "Category:Indian folk art", "Sanji wall art Haryana"),
    ("Pahari Painting", "himachalpradesh", "Category:Pahari painting", "Pahari miniature painting"),
    ("Sohrai Art", "jharkhand", "Category:Sohrai art", "Sohrai tribal art"),
    ("Mysore Painting", "karnataka", "Category:Mysore painting", "Mysore painting Indian art"),
    ("Kerala Mural Painting", "kerala", "Category:Kerala mural painting", "Kerala mural art"),
    ("Gond Art", "madhyapradesh", "Category:Gond art", "Gond tribal art"),
    ("Warli Painting", "maharashtra", "Category:Warli painting", "Warli tribal painting"),
    ("Manipuri Manuscript Art", "manipur", "Category:Manipuri art", "Manipuri manuscript art"),
    ("Khasi Bamboo Art", "meghalaya", "Category:Khasi art", "Khasi bamboo craft"),
    ("Mizo Textile Art", "mizoram", "Category:Mizo culture", "Mizo textile art"),
    ("Naga Wood Carving", "nagaland", "Category:Naga art", "Naga wood carving"),
    ("Pattachitra", "odisha", "Category:Pattachitra", "Pattachitra Indian art"),
    ("Phulkari Embroidery", "punjab", "Category:Phulkari", "Phulkari embroidery"),
    ("Rajasthani Miniature Painting", "rajasthan", "Category:Rajasthani painting", "Rajasthani miniature painting"),
    ("Sikkimese Thangka", "sikkim", "Category:Thangka", "Sikkimese Thangka art"),
    ("Tanjore Painting", "tamilnadu", "Category:Thanjavur painting", "Tanjore painting Indian art"),
    ("Cheriyal Scroll Painting", "telangana", "Category:Cheriyal scroll painting", "Cheriyal scroll painting"),
    ("Tripura Bamboo Art", "tripura", "Category:Tripura art", "Tripura bamboo craft"),
    ("Mughal Miniature Painting", "uttarpradesh", "Category:Mughal painting", "Mughal miniature painting"),
    ("Aipan Art", "uttarakhand", "Category:Aipan art", "Aipan folk art"),
    ("Bengal School of Art", "westbengal", "Category:Bengal school of art", "Bengal school painting"),
    ("Nicobari Shell Craft", "andamanandnicobarislands", "Category:Nicobarese culture", "Nicobari shell craft"),
    ("Kashmiri Pashmina Embroidery", "jammuandkashmir", "Category:Kashmiri embroidery", "Kashmiri Pashmina embroidery")
]

# Create images directory
os.makedirs("images", exist_ok=True)

# Wikimedia Commons API base URL
base_url = "https://commons.wikimedia.org/w/api.php"

for art, state, category, fallback_search in art_forms:
    try:
        # Try category first
        params = {
            "action": "query",
            "format": "json",
            "generator": "categorymembers",
            "gcmtitle": category,
            "gcmtype": "file",
            "gcmlimit": 1,
            "prop": "imageinfo",
            "iiprop": "url"
        }
        response = requests.get(base_url, params=params)
        data = response.json()

        img_url = None
        if "query" in data and "pages" in data["query"]:
            pages = data["query"]["pages"]
            for page_id, page in pages.items():
                if "imageinfo" in page:
                    img_url = page["imageinfo"][0]["url"]
                    break

        # Fallback to search if no image found in category
        if not img_url:
            params = {
                "action": "query",
                "format": "json",
                "generator": "search",
                "gsrsearch": fallback_search,
                "gsrnamespace": 6,  # Namespace 6 is for files
                "gsrlimit": 1,
                "prop": "imageinfo",
                "iiprop": "url"
            }
            response = requests.get(base_url, params=params)
            data = response.json()
            if "query" in data and "pages" in data["query"]:
                pages = data["query"]["pages"]
                for page_id, page in pages.items():
                    if "imageinfo" in page:
                        img_url = page["imageinfo"][0]["url"]
                        break

        # Download and save the image
        if img_url:
            urllib.request.urlretrieve(img_url, f"images/{state}.jpg")
            print(f"Downloaded {art} for {state}")
        else:
            print(f"No images found for {art} in {category} or search '{fallback_search}'")
    except Exception as e:
        print(f"Error downloading {art} for {state}: {e}")