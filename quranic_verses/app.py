import streamlit as st
import json
import random
import requests
import re
import time
from collections import defaultdict

# Set page configuration
st.set_page_config(
    page_title="Quranic Verses By Mood",
    page_icon="☪️",
    layout="centered"
)

# Add custom CSS for styling
st.markdown("""
<style>
    .verse-card {
        background-color: #1E3A5F;
        color: #FFFFFF;
        border-radius: 10px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .verse-text {
        font-size: 22px;
        margin-bottom: 15px;
        line-height: 1.5;
        font-weight: 500;
    }
    .verse-reference {
        font-size: 16px;
        color: #E6C35C;
        font-style: italic;
        text-align: right;
    }
    .main-title {
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 30px;
        color: #1E3A5F;
    }
    .mood-subtitle {
        color: #1E3A5F;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #1E3A5F;
        color: white;
        border-radius: 12px;
        padding: 10px 20px;
        font-weight: bold;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #E6C35C;
        color: #1E3A5F;
    }
    .footer {
        text-align: center;
        color: #666;
        margin-top: 30px;
    }
    .loading {
        text-align: center;
        color: #1E3A5F;
        font-style: italic;
    }
    .info-box {
        background-color: #1E3A5F;
        color: #FFFFFF;
        border-left: 5px solid #E6C35C;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .mood-category {
        margin-bottom: 10px;
        font-weight: bold;
        color: #1E3A5F;
    }
    .category-container {
        background-color: #f5f5f5;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .search-box {
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Add custom CSS for the Daily Verse section
st.markdown("""
<style>
    .daily-verse-section {
        background-color: #f8f5e6;
        border-radius: 15px;
        padding: 20px;
        margin: 30px 0;
        border: 2px solid #E6C35C;
    }
    .daily-verse-title {
        color: #1E3A5F;
        text-align: center;
        font-size: 1.8em;
        margin-bottom: 15px;
        font-weight: bold;
    }
    .daily-verse-button {
        background-color: #E6C35C !important;
        color: #1E3A5F !important;
        font-size: 18px !important;
        padding: 15px 30px !important;
        border-radius: 50px !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s !important;
        font-weight: bold !important;
    }
    .daily-verse-button:hover {
        background-color: #1E3A5F !important;
        color: white !important;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2) !important;
        transform: translateY(-2px) !important;
    }
    .daily-verse-card {
        background: linear-gradient(135deg, #1E3A5F 0%, #2c5282 100%);
        border-radius: 15px;
        padding: 30px;
        margin-top: 20px;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        border-left: 5px solid #E6C35C;
    }
    .daily-verse-text {
        font-size: 24px;
        line-height: 1.6;
        margin-bottom: 20px;
        color: white;
        font-weight: 500;
        font-style: italic;
    }
    .daily-verse-reference {
        text-align: right;
        color: #E6C35C;
        font-size: 18px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.markdown("<h1 class='main-title'>Quranic Verses Based on Mood & Theme</h1>", unsafe_allow_html=True)

# Define a comprehensive set of moods and themes with keywords for classification
MOOD_KEYWORDS = {
    # Emotional States
    "happy": [
        "joy", "glad", "happiness", "rejoice", "pleased", "satisfied", "delight", "pleasure", 
        "enjoy", "cheer", "content", "merry", "blessed", "elated", "jubilant", "happy", "smile",
        "celebrate", "festive", "joyful", "joyous", "bliss", "ecstasy", "thrill", "exult",
        "triumph", "victory", "succeed", "fortunate", "lucky", "grateful", "thankful"
    ],
    "sad": [
        "grief", "sadness", "sorrow", "despair", "cry", "tears", "distress", "pain", "suffering", 
        "mourn", "lament", "weep", "anguish", "heartache", "misery", "unhappy", "sad", "bitter",
        "dejected", "downcast", "gloomy", "depressed", "melancholy", "regret", "remorse", "woe",
        "heavy-hearted", "troubled", "hurt", "agony", "torment", "affliction", "tragedy"
    ],
    "fear": [
        "afraid", "terror", "dread", "fear", "anxiety", "worry", "panic", "alarm", "horror", 
        "fright", "scared", "terrified", "apprehension", "frightened", "dismay", "shock", "awe",
        "nervous", "uneasy", "apprehensive", "concern", "distress", "tremble", "quake", "shudder",
        "threat", "danger", "peril", "intimidate", "daunting", "frightful", "terrible", "menace"
    ],
    "angry": [
        "anger", "rage", "wrath", "fury", "outrage", "irritated", "indignation", "displeasure", 
        "resentment", "irritation", "offense", "enraged", "infuriated", "hostile", "bitter",
        "furious", "mad", "fuming", "irate", "frustrated", "annoyed", "vexed", "provoked", 
        "exasperated", "incensed", "inflamed", "heated", "seething", "hatred", "vengeance"
    ],
    "love": [
        "love", "beloved", "affection", "compassion", "kindness", "tenderness", "devotion",
        "fondness", "adoration", "attachment", "care", "cherish", "intimacy", "warmth", "close",
        "dear", "endearment", "darling", "sweetheart", "companion", "friendship", "relationship",
        "passion", "romantic", "embrace", "unite", "bond", "connection", "sympathize", "empathy"
    ],
    "gratitude": [
        "thank", "gratitude", "thankful", "grateful", "appreciate", "recognition", "acknowledgment",
        "indebted", "bless", "praise", "extol", "glorify", "exalt", "honor", "revere", "owe", 
        "obliged", "acknowledgment", "gratefulness", "appreciation", "regard", "value", "recognize",
        "esteem", "admire", "respect", "venerate", "tribute", "worship", "adoration"
    ],

    # Spiritual States
    "faith": [
        "faith", "believe", "belief", "trust", "certainty", "conviction", "devotion", "piety",
        "truthful", "sincere", "faithful", "confidence", "assurance", "dedication", "devout", 
        "loyal", "committed", "trusting", "trustworthy", "expectant", "rely", "depend", "count on",
        "fidelity", "allegiance", "loyalty", "religious", "spiritual", "sacred", "holy", "divine",
        "creed", "doctrine", "dogma", "worship", "religion", "soul", "spirit"
    ],
    "hope": [
        "hope", "aspire", "anticipate", "expectation", "optimism", "prospect", "look forward",
        "wish", "desire", "longing", "yearning", "promising", "encouraging", "positive", "expect",
        "await", "optimistic", "hopeful", "inspire", "inspirit", "invigorate", "cheer", "believe",
        "trust", "assured", "confident", "eagerness", "aspiration", "ambition", "dream", "ideal"
    ],
    "patience": [
        "patience", "patient", "perseverance", "endurance", "steadfastness", "fortitude",
        "tolerance", "restraint", "composure", "calmness", "wait", "forbearance", "resilience", 
        "constancy", "persistence", "determination", "resolve", "tenacity", "diligence", "attentive",
        "deliberate", "long-suffering", "stoicism", "serenity", "tranquility", "self-control",
        "self-discipline", "self-restraint", "abide", "bear with", "put up with"
    ],
    "repentance": [
        "repent", "forgiveness", "pardon", "mercy", "remorse", "regret", "contrition", "penitent",
        "apologize", "atone", "redeem", "absolve", "purify", "cleanse", "redemption", "atonement",
        "expiation", "amends", "sorry", "guilt", "conscience", "confession", "admit", "acknowledge",
        "return", "turn back", "convert", "transform", "change", "reform", "revert", "penance"
    ],

    # Ethical Virtues
    "justice": [
        "justice", "fair", "right", "equity", "impartial", "righteous", "honest", "integrity",
        "upright", "moral", "ethical", "principled", "equitable", "balanced", "lawful", "legal",
        "legitimate", "deserved", "merited", "earned", "due", "proper", "correct", "appropriate",
        "reasonable", "just", "equality", "fairness", "impartiality", "unbiased", "objective", 
        "judgment", "verdict", "sentence", "decree", "award", "recompense", "compensate", "redress"
    ],
    "wisdom": [
        "wisdom", "knowledge", "understanding", "insight", "intellect", "discernment", "prudence",
        "judgment", "perception", "foresight", "comprehension", "reason", "enlightenment", "sage", 
        "wise", "intelligent", "smart", "clever", "astute", "shrewd", "perceptive", "judicious",
        "sensible", "reasonable", "rational", "logical", "sound", "thoughtful", "reflective", 
        "contemplative", "philosophical", "profound", "deep", "meaningful", "profound", "learned"
    ],
    "humility": [
        "humble", "modesty", "meek", "unpretentious", "unassuming", "submissive", "lowliness",
        "servitude", "respectful", "deferential", "obedient", "compliant", "yielding", "modest", 
        "unassuming", "unobtrusive", "unostentatious", "simple", "ordinary", "egoless", "selfless",
        "self-effacing", "unboastful", "unpretending", "reserved", "bashful", "subservient",
        "servile", "inferior", "unimportant", "insignificant", "low", "bend", "bow", "stoop"
    ],
    "generosity": [
        "generous", "give", "charity", "alms", "donate", "spend", "benevolent", "kind",
        "magnanimous", "liberal", "munificent", "bountiful", "philanthropic", "selfless", "sharing",
        "giving", "charitable", "altruistic", "unselfish", "benevolence", "beneficence", "bounty", 
        "goodwill", "kindness", "hospitality", "unsparingness", "openhandedness", "free-handed",
        "gift", "present", "offering", "contribution", "donation", "philanthropy", "distribute"
    ],

    # Life Challenges & Responses
    "struggle": [
        "struggle", "strive", "effort", "hardship", "difficulty", "challenge", "trial", "adversity",
        "obstacle", "hindrance", "resistance", "opposition", "battle", "fight", "contend", "attempt",
        "endeavor", "labor", "work", "toil", "strain", "stress", "pressure", "burden", "load",
        "problem", "trouble", "predicament", "plight", "quandary", "dilemma", "tribulation",
        "ordeal", "test", "compete", "wrestle", "grapple", "clash", "conflict", "confrontation"
    ],
    "guidance": [
        "guide", "guidance", "lead", "direct", "show", "instruct", "teach", "counsel", "advise",
        "direction", "path", "way", "route", "course", "navigation", "steer", "conduct", "help", 
        "assist", "aid", "support", "mentor", "tutor", "coach", "educate", "train", "enlighten",
        "illuminate", "light", "beacon", "signal", "sign", "indicator", "mark", "landmark",
        "signpost", "compass", "map", "plan", "blueprint", "model", "exemplar", "example", "pattern"
    ],
    "success": [
        "success", "victory", "triumph", "achieve", "accomplish", "attain", "realize", "win",
        "conquer", "prevail", "prosper", "flourish", "thrive", "excel", "master", "overcome", 
        "succeed", "achieve", "accomplish", "complete", "fulfill", "execute", "perform", "conclude",
        "finalize", "perfect", "consummate", "crown", "cap", "clinch", "secure", "gain", "acquire",
        "obtain", "procure", "achievement", "accomplishment", "attainment", "feat", "exploit", "deed"
    ],
    "peace": [
        "peace", "tranquility", "calm", "serenity", "harmony", "quiet", "stillness", "rest",
        "repose", "relaxation", "reconciliation", "truce", "accord", "agreement", "settlement", 
        "cease-fire", "armistice", "treaty", "pact", "compromise", "understanding", "peaceful",
        "serene", "tranquil", "halcyon", "calm", "placid", "quiet", "still", "untroubled", "secure",
        "safe", "stable", "steady", "balance", "equilibrium", "equipoise", "proportion", "symmetry"
    ],

    # Relationship with God
    "devotion": [
        "devote", "worship", "adore", "reverence", "venerate", "glorify", "praise", "exalt", 
        "magnify", "extol", "supplicate", "invoke", "beseech", "implore", "entreat", "petition", 
        "pray", "appeal", "request", "solicit", "plead", "devotion", "dedication", "commitment",
        "consecration", "piety", "religiousness", "sacredness", "sanctity", "holiness", "godliness",
        "spirituality", "faithful", "dedicated", "committed", "loyal", "steadfast", "staunch"
    ],
    "creation": [
        "create", "make", "form", "fashion", "produce", "generate", "design", "craft", "construct",
        "build", "establish", "heaven", "earth", "universe", "world", "existence", "nature", "life", 
        "creation", "creature", "being", "living", "organism", "animal", "plant", "vegetation",
        "flora", "fauna", "sky", "land", "sea", "mountains", "rivers", "trees", "sun", "moon", "stars",
        "planets", "galaxies", "cosmos", "universe", "mankind", "humankind", "humanity", "people"
    ],
    "afterlife": [
        "afterlife", "hereafter", "resurrection", "paradise", "heaven", "garden", "hell", "fire",
        "judgment", "reckoning", "account", "reward", "punishment", "eternal", "immortal", "final", 
        "day of judgment", "day of resurrection", "last day", "end", "death", "life after death",
        "eternity", "everlasting", "perpetual", "endless", "unending", "infinite", "boundless",
        "limitless", "never-ending", "forevermore", "salvation", "damnation", "retribution", "recompense"
    ],
    
    # Additional Themes
    "mercy": [
        "mercy", "compassion", "forgiveness", "pardon", "clemency", "leniency", "forbearance",
        "tolerance", "lenity", "amnesty", "reprieve", "quarter", "pity", "sympathy", "empathy",
        "commiseration", "tenderness", "kindness", "mildness", "gentleness", "benevolence", 
        "charity", "benignity", "goodwill", "grace", "beneficence", "kindliness", "humaneness",
        "humanism", "soft-heartedness", "warm-heartedness", "feeling", "consideration", "indulgence"
    ],
    "blessing": [
        "blessing", "benediction", "grace", "favor", "benefit", "advantage", "privilege", "boon",
        "gift", "present", "reward", "endowment", "bestowal", "conferment", "grant", "bless",
        "blessed", "blissful", "fortunate", "lucky", "favorable", "auspicious", "propitious",
        "providential", "benevolent", "generous", "munificent", "bountiful", "plentiful", "abundant"
    ],
    "prayer": [
        "prayer", "supplication", "invocation", "entreaty", "petition", "plea", "request", "appeal",
        "solicitation", "imploration", "devotion", "worship", "adoration", "praise", "thanksgiving",
        "glorification", "exaltation", "magnification", "pray", "supplicate", "beseech", "implore",
        "entreat", "call upon", "invoke", "address", "appeal to", "solicit", "beg", "request"
    ],
    "teaching": [
        "teach", "instruct", "educate", "train", "tutor", "coach", "mentor", "guide", "direct",
        "advise", "counsel", "edify", "enlighten", "illuminate", "inform", "apprise", "notify",
        "lesson", "instruction", "teaching", "education", "training", "doctrine", "dogma", "tenet",
        "precept", "principle", "maxim", "aphorism", "axiom", "dictum", "saying", "adage", "proverb"
    ],
    "truth": [
        "truth", "reality", "fact", "actuality", "certainty", "certitude", "verity", "genuineness",
        "authenticity", "accuracy", "correctness", "precision", "exactness", "validity", "factuality",
        "true", "real", "actual", "genuine", "authentic", "accurate", "correct", "precise", "exact",
        "valid", "factual", "honest", "truthful", "sincere", "candid", "frank", "open", "forthright"
    ],
    "family": [
        "family", "household", "home", "relatives", "relation", "kin", "kinship", "kindred", "kith",
        "blood", "lineage", "ancestry", "descent", "extraction", "heritage", "parentage", "pedigree",
        "genealogy", "father", "mother", "parent", "child", "son", "daughter", "brother", "sister",
        "sibling", "spouse", "husband", "wife", "marriage", "matrimony", "wedding", "bride", "groom"
    ]
}

# Function to fetch Quranic verses from API
@st.cache_data(ttl=3600)  # Cache for an hour
def fetch_quran_data():
    """Fetch English translation of Quran using Quran.com API for more modern language"""
    try:
        # Create a list to store all surah data
        all_surahs = []
        
        # Create a progress bar
        progress_bar = st.progress(0)
        loading_text = st.empty()
        loading_text.markdown("Fetching Quran data...")
        
        # Quran has 114 surahs, we'll fetch them one by one with their translations
        for surah_number in range(1, 115):
            # Use Quran.com API (v4) to get a more modern translation
            url = f"https://api.quran.com/api/v4/verses/by_chapter/{surah_number}?language=en&words=true&translations=131"
            # Translation 131 is Saheeh International which is in more modern English
            
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            # Extract the surah data and format it to match our structure
            surah_data = response.json()
            
            # Extract the name from a different endpoint if needed
            surah_info_url = f"https://api.quran.com/api/v4/chapters/{surah_number}?language=en"
            surah_info_response = requests.get(surah_info_url)
            surah_info = surah_info_response.json()
            
            # Format the data to match our expected structure
            formatted_surah = {
                "number": surah_number,
                "name": surah_info["chapter"]["name_simple"],
                "ayahs": []
            }
            
            # Process each verse
            for verse in surah_data["verses"]:
                verse_text = ""
                # Get the translation text
                for translation in verse["translations"]:
                    verse_text = translation["text"]
                    break
                
                # Format the verse
                formatted_verse = {
                    "number": verse["verse_number"],
                    "text": verse_text,
                    "numberInSurah": verse["verse_number"]
                }
                
                formatted_surah["ayahs"].append(formatted_verse)
            
            all_surahs.append(formatted_surah)
            
            # Update progress bar instead of writing text
            progress = surah_number / 114
            progress_bar.progress(progress)
            loading_text.markdown(f"Fetching Quran data... {surah_number}/114 surahs processed")
        
        # Clear progress elements when done
        progress_bar.empty()
        loading_text.empty()
        
        return all_surahs
            
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch Quran data: {str(e)}")
        
        # Fall back to the original API if the new one fails
        try:
            st.warning("Falling back to alternative API...")
            url = "https://api.alquran.cloud/v1/quran/en.sahih"  # Using Sahih International translation
            response = requests.get(url)
            response.raise_for_status()
            
            quran_data = response.json()
            if quran_data["code"] == 200:
                return quran_data["data"]["surahs"]
            else:
                return None
                
        except requests.exceptions.RequestException:
            return None

# Function to classify verse by mood
def classify_verse_mood(verse_text):
    """Classify verse text into multiple moods based on keyword presence"""
    verse_text = verse_text.lower()
    mood_scores = defaultdict(float)
    matched_moods = []
    
    # Perform exact word boundary matches first (higher score)
    for mood, keywords in MOOD_KEYWORDS.items():
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', verse_text):
                mood_scores[mood] += 1.0
    
    # Then try partial/stemmed matches if needed
    if not mood_scores:
        for mood, keywords in MOOD_KEYWORDS.items():
            for keyword in keywords:
                if keyword in verse_text:
                    mood_scores[mood] += 0.5  # Lower score for partial matches
    
    # Get all moods that have scores
    if mood_scores:
        # Find the highest score
        max_score = max(mood_scores.values())
        
        # Get all moods with the highest score
        primary_mood = max(mood_scores.items(), key=lambda x: x[1])[0]
        matched_moods.append(primary_mood)
        
        # Add secondary moods that have reasonable scores (at least half of max)
        for mood, score in mood_scores.items():
            if mood != primary_mood and score >= max_score * 0.5:
                matched_moods.append(mood)
    
    return matched_moods

# Function to classify verse by mood - more aggressive version
def classify_verse_mood(verse_text):
    """Classify verse text into multiple moods based on keyword presence - more inclusive version"""
    verse_text = verse_text.lower()
    mood_scores = defaultdict(float)
    matched_moods = []
    
    # Perform exact word boundary matches first (higher score)
    for mood, keywords in MOOD_KEYWORDS.items():
        for keyword in keywords:
            # Use word boundary for multi-word keywords
            if len(keyword.split()) > 1:
                if keyword in verse_text:
                    mood_scores[mood] += 1.5  # Extra weight for multi-word matches
            # Use word boundary for single words
            elif re.search(r'\b' + re.escape(keyword) + r'\b', verse_text):
                mood_scores[mood] += 1.0
            # Partial match as a backup with lower weight
            elif keyword in verse_text:
                mood_scores[mood] += 0.5
    
    # If we still have no matches, check for keyword stems (more aggressive matching)
    if not mood_scores:
        for mood, keywords in MOOD_KEYWORDS.items():
            for keyword in keywords:
                # Check for word stems (first 4+ characters)
                if len(keyword) > 4:
                    stem = keyword[:4]  # Take first 4 characters as stem
                    if re.search(r'\b' + re.escape(stem), verse_text):
                        mood_scores[mood] += 0.3  # Lower score for stem matches
    
    # Get thematic moods based on content analysis
    # Many Quranic verses address believers or refer to Allah, so add these themes when appropriate
    if "believe" in verse_text or "faithful" in verse_text or "righteous" in verse_text:
        mood_scores["faith"] += 0.8
    
    if "allah" in verse_text or "god" in verse_text or "lord" in verse_text:
        mood_scores["devotion"] += 0.8
    
    # If we have scores, determine which moods to return
    if mood_scores:
        # Find the highest score
        max_score = max(mood_scores.values())
        
        # Get the primary mood (highest score)
        primary_mood = max(mood_scores.items(), key=lambda x: x[1])[0]
        matched_moods.append(primary_mood)
        
        # Add secondary moods with scores at least 40% of max (more inclusive)
        for mood, score in mood_scores.items():
            if mood != primary_mood and score >= max_score * 0.4:  # Lower threshold to include more matches
                matched_moods.append(mood)
    
    return matched_moods

# Function to process and organize Quran data by mood
@st.cache_data(ttl=3600)  # Cache for an hour
def organize_verses_by_mood(quran_data):
    """Process Quran data and organize verses by mood."""
    verses_by_mood = defaultdict(list)
    all_verses = []
    verse_count = 0
    categorized_count = 0
    
    with st.spinner('Analyzing verses and classifying by mood...'):
        progress_bar = st.progress(0)
        progress_text = st.empty()
        
        # Count total verses for progress tracking
        total_verses = sum(len(surah["ayahs"]) for surah in quran_data)
        
        for surah in quran_data:
            surah_number = surah["number"]
            
            for verse in surah["ayahs"]:
                verse_text = verse["text"]
                verse_number = verse["numberInSurah"]
                verse_count += 1
                
                # Create verse object
                verse_obj = {
                    "verse": verse_text,
                    "reference": f"Quran {surah_number}:{verse_number}",
                    "surah": surah_number,
                    "ayah": verse_number
                }
                
                # Add to all verses list
                all_verses.append(verse_obj)
                
                # Classify the verse into potentially multiple moods
                moods = classify_verse_mood(verse_text)
                
                if moods:  # Only add if moods are detected
                    categorized_count += 1
                    for mood in moods:
                        verses_by_mood[mood].append(verse_obj)
                else:
                    # Add to uncategorized category
                    verses_by_mood["uncategorized"].append(verse_obj)
                
                # Update progress
                progress = verse_count / total_verses
                progress_bar.progress(progress)
                
                # Update progress text every 100 verses to avoid UI slowdown
                if verse_count % 100 == 0 or verse_count == total_verses:
                    progress_text.text(f"Analyzed {verse_count}/{total_verses} verses... ({categorized_count} categorized so far)")
        
        # Complete progress and clean up
        progress_bar.progress(1.0)
        time.sleep(0.5)  # Give users time to see completion
        progress_bar.empty()
        progress_text.empty()
    
    # Add stats
    verses_by_mood["_stats"] = {
        "total_verses": verse_count,
        "categorized_verses": categorized_count,
        "uncategorized_verses": verse_count - categorized_count
    }
    
    # Also store all verses in case we want to search through them
    verses_by_mood["_all"] = all_verses
    
    return dict(verses_by_mood)

# Function to export categorized verses to a dedicated JSON file
def export_verses_to_json(verses_by_mood, filename="categorized_quranic_verses.json"):
    """Export all categorized verses to a dedicted JSON file for faster loading in future."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(verses_by_mood, file, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.warning(f"Failed to export categorized verses: {str(e)}")
        return False
    

# Function to load mood categorized data
@st.cache_data
def load_mood_data():
    """Load verses organized by mood, either from saved file, API or fallback."""
    
    # Create containers for progress updates
    status_container = st.empty()
    
    # First try to load from the dedicated categorized verses file
    try:
        status_container.info("Checking for saved categorized verses...")
        with open("categorized_quranic_verses.json", "r", encoding="utf-8") as file:
            saved_data = json.load(file)
            
        # Verify it has our stats
        if saved_data and "_stats" in saved_data:
            categorized = saved_data["_stats"]["categorized_verses"]
            total = saved_data["_stats"]["total_verses"]
            status_container.success(f"✓ Loaded {categorized} categorized verses from saved file ({categorized/total:.1%} of Quran)")
            return saved_data
    except (FileNotFoundError, json.JSONDecodeError):
        status_container.info("No saved categorized verses file found. Will create one...")
    
    # If no saved file exists, try to load from API
    status_container.info("Fetching verses from Quran API...")
    quran_data = fetch_quran_data()
    
    if quran_data:
        # Organize verses by mood
        verses_by_mood = organize_verses_by_mood(quran_data)
        
        # Export the organized data to a dedicated JSON file
        if export_verses_to_json(verses_by_mood):
            status_container.success(f"✓ {verses_by_mood['_stats']['categorized_verses']} verses classified and saved for faster loading next time.")
        
        # Clear the status
        status_container.empty()
        return verses_by_mood
    else:
        # If API fails, try to use the original file as a fallback
        try:
            with open("quranic_verses_by_mood.json", "r", encoding="utf-8") as file:
                fallback_data = json.load(file)
                status_container.warning("Using fallback data source.")
                return fallback_data
        except (FileNotFoundError, json.JSONDecodeError):
            status_container.error("Could not load verses data from API or fallback file.")
            return None

# Function to get a random verse based on mood
def get_random_verse(mood_data):
    return random.choice(mood_data)

# Group moods into categories for better organization
MOOD_CATEGORIES = {
    "Emotional States": ["happy", "sad", "fear", "angry", "love", "gratitude"],
    "Spiritual States": ["faith", "hope", "patience", "repentance"],
    "Ethical Virtues": ["justice", "wisdom", "humility", "generosity"],
    "Life Challenges & Responses": ["struggle", "guidance", "success", "peace"],
    "Relationship with God": ["devotion", "creation", "afterlife"],
    "Additional Themes": ["mercy", "blessing", "prayer", "teaching", "truth", "family"],
    "Other": ["uncategorized"]
}

# Main app logic
try:
    # Show loading spinner while fetching and organizing data
    with st.spinner('Loading Quranic verses...'):
        data = load_mood_data()
    
    if data:
        # Remove special keys from display
        display_moods = [m for m in data.keys() if not m.startswith('_')]
        
   # Add a prominent Daily Verse section with auto-display feature
        st.markdown("---")
        
        # Create a beautifully styled Daily Verse section
        st.markdown("""
        <div class='daily-verse-section'>
            <div class='daily-verse-title'>💫 Daily Quranic Verse</div>
        """, unsafe_allow_html=True)
        
        # Auto-select a random verse if not already in session state
        if 'daily_verse' not in st.session_state:
            if "_all" in data:
                st.session_state.daily_verse = random.choice(data["_all"])
            else:
                # Fallback if _all isn't available - get a random verse from any category
                all_verses = []
                for mood in data:
                    if not mood.startswith("_") and len(data[mood]) > 0:
                        all_verses.extend(data[mood])
                if all_verses:
                    st.session_state.daily_verse = random.choice(all_verses)
        
        # Add just a refresh button
        daily_verse_col1, daily_verse_col2 = st.columns([3, 1])
        with daily_verse_col2:
            if st.button("🔄 New Verse", key="refresh_verse_button", use_container_width=True):
                # Get a random verse from the entire Quran
                if "_all" in data:
                    st.session_state.daily_verse = random.choice(data["_all"])
                else:
                    # Fallback if _all isn't available - get a random verse from any category
                    all_verses = []
                    for mood in data:
                        if not mood.startswith("_") and len(data[mood]) > 0:
                            all_verses.extend(data[mood])
                    if all_verses:
                        st.session_state.daily_verse = random.choice(all_verses)

        # Display the daily verse
        if 'daily_verse' in st.session_state:
            daily_verse = st.session_state.daily_verse
            
            st.markdown(
                f"""
                <div class="daily-verse-card">
                    <div class="daily-verse-text">"{daily_verse['verse']}"</div>
                    <div class="daily-verse-reference">
                        {daily_verse['reference']} (Surah {daily_verse['surah']}, Ayah {daily_verse['ayah']})
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
        
        # Close the daily verse section
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")



        # Add search functionality
        st.markdown("<h3 class='mood-subtitle'>Search for a Specific Theme</h3>", unsafe_allow_html=True)
        search_term = st.text_input("Enter keywords to find specific themes:", key="search_box")
        
        if search_term:
            search_term = search_term.lower()
            matched_moods = []
            
            # Find moods that match the search term
            for mood in display_moods:
                if search_term in mood or any(search_term in kw for kw in MOOD_KEYWORDS.get(mood, [])):
                    matched_moods.append(mood)
            
            if matched_moods:
                st.success(f"Found {len(matched_moods)} matching themes")
                display_moods = matched_moods
            else:
                st.warning("No matching themes found. Showing all themes.")
        
     

        # Display moods by category
        st.markdown("<h3 class='mood-subtitle'>Select a Mood or Theme:</h3>", unsafe_allow_html=True)
        
        # Create tabs for each category
        tabs = st.tabs([category for category in MOOD_CATEGORIES.keys()])
        
        # For each category tab, display the moods in that category
        for i, (category, moods_in_category) in enumerate(MOOD_CATEGORIES.items()):
            with tabs[i]:
                # Filter to only include moods that exist in our data
                available_moods = [m for m in moods_in_category if m in display_moods]
                if not available_moods:
                    st.write("No moods available in this category.")
                    continue
                
                # Create rows with 3 moods per row
                moods_per_row = 3
                for j in range(0, len(available_moods), moods_per_row):
                    row_moods = available_moods[j:j+moods_per_row]
                    cols = st.columns(moods_per_row)
                    
                    for k, mood in enumerate(row_moods):
                        with cols[k]:
                            # Display counts with each mood
                            mood_count = len(data[mood])
                            button_label = f"{mood.capitalize()} ({mood_count})"
                            
                            if st.button(button_label, key=f"mood_{category}_{mood}", use_container_width=True):
                                if mood_count > 0:
                                    # Get a random verse for the selected mood
                                    random_verse = get_random_verse(data[mood])
                                    
                                    # Store the selected mood and verse in session state
                                    st.session_state.selected_mood = mood
                                    st.session_state.current_verse = random_verse
                                else:
                                    st.warning(f"No verses found for {mood} mood.")
        
        # "Other" category for any moods not in the categories
        other_moods = [m for m in display_moods if not any(m in category_moods for category_moods in MOOD_CATEGORIES.values())]
        if other_moods:
            st.markdown("<h3 class='mood-subtitle'>Other Themes:</h3>", unsafe_allow_html=True)
            # Create rows with 3 moods per row
            moods_per_row = 3
            for j in range(0, len(other_moods), moods_per_row):
                row_moods = other_moods[j:j+moods_per_row]
                cols = st.columns(moods_per_row)
                
                for k, mood in enumerate(row_moods):
                    with cols[k]:
                        # Display counts with each mood
                        mood_count = len(data[mood])
                        button_label = f"{mood.capitalize()} ({mood_count})"
                        
                        if st.button(button_label, key=f"mood_other_{mood}", use_container_width=True):
                            if mood_count > 0:
                                # Get a random verse for the selected mood
                                random_verse = get_random_verse(data[mood])
                                
                                # Store the selected mood and verse in session state
                                st.session_state.selected_mood = mood
                                st.session_state.current_verse = random_verse
                            else:
                                st.warning(f"No verses found for {mood} mood.")
        
        # Display random verse based on selected mood
        if 'selected_mood' in st.session_state and 'current_verse' in st.session_state:
            mood = st.session_state.selected_mood
            verse = st.session_state.current_verse
            
            st.markdown("---")
            st.markdown(f"<h2 class='mood-subtitle'>Verse for {mood.capitalize()} Theme</h2>", unsafe_allow_html=True)
            
            # Display the random verse in a beautiful card
            st.markdown(
                f"""
                <div class="verse-card">
                    <div class="verse-text">"{verse['verse']}"</div>
                    <div class="verse-reference">
                        {verse['reference']} (Surah {verse['surah']}, Ayah {verse['ayah']})
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            # Add button to get another verse for the same mood
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Show Another Verse", key="another_verse"):
                    mood_data = data[mood]
                    if len(mood_data) > 1:
                        new_verse = get_random_verse(mood_data)
                        attempts = 0
                        while new_verse == verse and attempts < 5:  # Ensure we get a different verse
                            new_verse = get_random_verse(mood_data)
                            attempts += 1
                        st.session_state.current_verse = new_verse
                        st.rerun()
            with col2:
                if st.button("Copy Verse", key="copy_verse"):
                    # Prepare the text to copy
                    copy_text = f"{verse['verse']} - {verse['reference']}"
                    # Create a text area that's easy to copy from but doesn't look like a code block
                    st.text_area("", value=copy_text, height=100, key="copy_area", help="Click and press Ctrl+A, Ctrl+C to copy")
    else:
        st.error("Failed to load Quranic verses. Please check your internet connection and try again.")

except Exception as e:
    st.error(f"An error occurred: {str(e)}")

# Add a footer
st.markdown("---")
st.markdown(
    """
    <div class="footer">
        Made with ❤️ | Data sourced from Quran.com API (Sahih International Translation)
    </div>
    """, 
    unsafe_allow_html=True
) 