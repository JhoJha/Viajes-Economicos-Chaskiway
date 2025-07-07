import requests
import re
import sqlite3
from urllib.parse import unquote
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('image_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# API configuration
WIKI_API_URL = "https://es.wikipedia.org/w/api.php"
COMMONS_API_URL = "https://commons.wikimedia.org/w/api.php"

# Updated department list with verified Wikipedia page titles
DEPARTAMENTOS_PERU = [
    "Departamento de Amazonas (Perú)",
    "Departamento de Áncash",
    "Departamento de Apurímac",
    "Departamento de Arequipa",
    "Departamento de Ayacucho",
    "Departamento de Cajamarca",
    "Provincia Constitucional del Callao",
    "Departamento de Cusco",
    "Departamento de Huancavelica",
    "Departamento de Huánuco",
    "Departamento de Ica",
    "Departamento de Junín",
    "Departamento de La Libertad",
    "Departamento de Lambayeque",
    "Departamento de Lima",
    "Departamento de Loreto",
    "Departamento de Madre de Dios",
    "Departamento de Moquegua",
    "Departamento de Pasco",
    "Departamento de Piura",
    "Departamento de Puno",
    "Departamento de San Martín",
    "Departamento de Tacna",
    "Departamento de Tumbes",
    "Departamento de Ucayali"
]

def create_database():
    """Create the SQLite database and table"""
    try:
        conn = sqlite3.connect('peru_images.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                departamento TEXT,
                lugar TEXT,
                image_title TEXT,
                image_url TEXT,
                license TEXT,
                description TEXT
            )
        ''')
        conn.commit()
        logger.info("Database created successfully")
        return True
    except sqlite3.Error as e:
        logger.error(f"Database creation failed: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def get_images_from_wiki(title):
    """Get images from a Wikipedia article"""
    try:
        params = {
            "action": "query",
            "titles": title,
            "prop": "images",
            "format": "json",
            "imlimit": 50  # Increase limit from default 10
        }
        
        logger.info(f"Fetching images for: {title}")
        response = requests.get(WIKI_API_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        pages = data.get("query", {}).get("pages", {})
        image_list = []
        
        for page_id, page in pages.items():
            if page_id == "-1":
                logger.warning(f"Page not found: {title}")
                continue
                
            images = page.get("images", [])
            logger.info(f"Found {len(images)} potential images for {title}")
            
            for img in images:
                img_title = img.get("title", "")
                # More lenient filtering - only exclude obvious non-photos
                if not re.search(r"\.svg$|mapa|bandera|flag|map|diagram|icono|logo", img_title, re.IGNORECASE):
                    # Handle Spanish Wikipedia's "Archivo:" prefix
                    clean_title = img_title.replace("Archivo:", "File:")
                    image_list.append(clean_title)
                    logger.debug(f"Included image: {clean_title}")
                else:
                    logger.debug(f"Filtered out image: {img_title}")
        
        return image_list
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed for {title}: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error processing {title}: {e}")
        return []

def get_image_info(image_title):
    """Get detailed information about an image from Wikimedia Commons"""
    try:
        params = {
            "action": "query",
            "titles": image_title,
            "prop": "imageinfo",
            "iiprop": "url|extmetadata",
            "iiurlwidth": 300,  # Get thumbnail URL
            "format": "json"
        }
        
        logger.debug(f"Fetching details for image: {image_title}")
        response = requests.get(COMMONS_API_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        pages = data.get("query", {}).get("pages", {})
        
        for page_id, page in pages.items():
            if page_id == "-1":
                logger.warning(f"Image not found: {image_title}")
                continue
                
            image_info = page.get("imageinfo", [{}])[0]
            if not image_info:
                continue
                
            # Get the best available URL (prefer thumbnail if available)
            image_url = image_info.get("thumburl") or image_info.get("url")
            
            if not image_url:
                logger.warning(f"No URL available for: {image_title}")
                continue
                
            # Get license information
            extmetadata = image_info.get("extmetadata", {})
            license_info = extmetadata.get("LicenseShortName", {}).get("value", "") or \
                          extmetadata.get("License", {}).get("value", "Desconocida")
            
            # Get description
            description = extmetadata.get("ImageDescription", {}).get("value", "") or \
                         extmetadata.get("ObjectName", {}).get("value", "")
            
            logger.info(f"Retrieved metadata for: {image_title}")
            return {
                "url": image_url,
                "license": license_info,
                "description": description
            }
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Image API request failed: {e}")
    except Exception as e:
        logger.error(f"Unexpected error processing image: {e}")
        
    return None

def save_to_db(departamento, lugar, image_title, image_url, license, description):
    """Save image data to the database"""
    conn = None
    try:
        conn = sqlite3.connect('peru_images.db')
        cursor = conn.cursor()
        
        # Check if image already exists
        cursor.execute('SELECT 1 FROM images WHERE image_url = ?', (image_url,))
        if cursor.fetchone():
            logger.debug(f"Image already exists: {image_title}")
            return False
            
        cursor.execute('''
            INSERT INTO images (departamento, lugar, image_title, image_url, license, description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (departamento, lugar, image_title, image_url, license, description))
        
        conn.commit()
        logger.info(f"Saved image to DB: {image_title}")
        return True
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return False
    finally:
        if conn:
            conn.close()

def main():
    """Main execution function"""
    logger.info("Starting image collection process")
    
    if not create_database():
        logger.error("Failed to initialize database")
        return
        
    for departamento in DEPARTAMENTOS_PERU:
        logger.info(f"\n{'='*50}\nProcessing department: {departamento}\n{'='*50}")
        
        images = get_images_from_wiki(departamento)
        if not images:
            logger.warning(f"No valid images found for {departamento}")
            continue
            
        saved_count = 0
        for img_title in images[:20]:  # Process up to 20 images per department
            img_info = get_image_info(img_title)
            if not img_info or not img_info.get("url"):
                logger.warning(f"Skipping image {img_title} - no valid metadata")
                continue
                
            if save_to_db(
                departamento=departamento,
                lugar=departamento,
                image_title=unquote(img_title.replace("File:", "")),
                image_url=img_info["url"],
                license=img_info["license"],
                description=img_info["description"]
            ):
                saved_count += 1
                
        logger.info(f"Saved {saved_count} images for {departamento}")
    
    logger.info("Image collection process completed")

if __name__ == "__main__":
    main()
