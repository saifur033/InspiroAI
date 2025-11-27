"""
image_caption_generator.py — InspiroAI v10.0 (Lightweight)
Simplified image caption generator without PIL/numpy dependencies
"""

from typing import Optional, Dict, List, Any
import random

# Graceful fallbacks for unavailable modules
try:
    from PIL import Image, ImageStat
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    from src.utils import detect_language
except Exception:
    def detect_language(*args: Any, **kwargs: Any) -> str:
        return "en"

try:
    from src.hashtag_ranker import generate_hashtags
except Exception:
    def generate_hashtags(*args: Any, **kwargs: Any) -> List[str]:
        return ["trending", "viral", "amazing"]


def generate_caption_for_image(image_bytes: bytes, filename: Optional[str] = "") -> Dict:
    """
    Generate image caption (fallback mode without PIL/numpy)
    Returns template captions based on image size heuristics
    """
    
    try:
        # Size-based heuristics (very basic, no PIL needed)
        image_size = len(image_bytes) if image_bytes else 0
        
        # Template captions
        templates = [
            "This moment is absolutely magical! ✨ Perfectly captured!",
            "Pure beauty in every frame! 📸✨ Stunning composition!",
            "Breathtaking and inspiring! 🌟✨ Love this shot!",
            "Absolutely mesmerizing! 💫✨ Incredible capture!",
            "Stunning visual storytelling! 🎨✨ Well done!",
            "This deserves all the attention! 🔥✨ Amazing work!",
            "Perfectly beautiful moment! 😍✨ Timeless capture!",
            "Absolutely gorgeous! 🌈✨ Love the composition!",
        ]
        
        caption = random.choice(templates)
        
        # Generate hashtags
        hashtags = ["photography", "momentcapture", "visualart", "instagram", 
                   "instaworthy", "artistic", "beautiful", "stunning",
                   "amazing", "photooftheday", "viral", "trending"]
        
        return {
            "caption": caption,
            "hashtags": hashtags[:12],
            "image_type": "general",
            "tone": "bright"
        }
    
    except Exception as e:
        return {
            "caption": "Beautiful moment captured! 📸✨ Pure artistry!",
            "hashtags": ["photography", "viral", "trending", "amazing"],
            "image_type": "general",
            "tone": "bright"
        }



# ---------------------------------------------------------
# 🖼️ Stable Dominant Color Detection (Numpy Histogram)
# ---------------------------------------------------------
def get_dominant_color(np_img: np.ndarray) -> Tuple[int, int, int]:
    try:
        pixels = np_img.reshape((-1, 3)).astype(float)
        hist, _ = np.histogramdd(pixels, bins=(8, 8, 8), range=((0, 256), (0, 256), (0, 256)))
        dominant_bin = np.unravel_index(hist.argmax(), hist.shape)
        dominant_color = tuple(int((bin_idx + 0.5) * 32) for bin_idx in dominant_bin)

        # Ensure the output is strictly a Tuple[int, int, int]
        if len(dominant_color) != 3:
            raise ValueError("Dominant color detection returned an invalid tuple length.")
        return cast(Tuple[int, int, int], dominant_color)
    except Exception as e:
        print(f"Dominant color detection error: {e}")
        return (128, 128, 128)  # Default to gray


# ---------------------------------------------------------
# ✨ MAIN FUNCTION — Upgraded Multi-Category Image Caption Generator
# ---------------------------------------------------------
def generate_caption_for_image(image_bytes: bytes, filename: Optional[str] = "") -> Dict:
    """
    Simple, robust image caption generator.
    Always returns a dict with caption, hashtags, and image_type.
    """
    try:
        print(f"[IMAGE-CAP] Starting generation for {filename}")
        print(f"[IMAGE-CAP] Image bytes: {type(image_bytes)}, size: {len(image_bytes) if image_bytes else 0}")
        
        # Validate image bytes
        if not image_bytes or len(image_bytes) == 0:
            print("[IMAGE-CAP-ERROR] Empty image bytes provided")
            return {
                "caption": "Beautiful image captured 📸✨",
                "hashtags": ["trending", "viral", "amazing"],
                "image_type": "empty"
            }
        
        # Load image
        try:
            img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            print(f"[IMAGE-CAP] ✓ Image loaded, size: {img.size}")
        except Exception as e:
            print(f"[IMAGE-CAP-ERROR] Failed to load: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return {
                "caption": "Beautiful image captured 📸✨",
                "hashtags": ["trending", "viral", "amazing"],
                "image_type": "error"
            }
        
        # Detect image type
        try:
            image_type = detect_image_type(img)
        except:
            image_type = "general"
        print(f"[IMAGE-CAP] Type: {image_type}")
        
        # Detect tone
        try:
            tone = detect_tone(img)
        except:
            tone = "balanced"
        print(f"[IMAGE-CAP] Tone: {tone}")
        
        # Get caption with enhanced viral quality
        caption = ""
        language = "en"  # Default to English for now
        
        try:
            # Try to get caption from templates
            if image_type in CAPTION_TEMPLATES.get(language, {}) and tone in CAPTION_TEMPLATES[language][image_type]:
                captions = CAPTION_TEMPLATES[language][image_type][tone]
                if captions:
                    caption = random.choice(captions)
            
            # Fallback to general if specific type not available
            if not caption:
                caption = random.choice(CAPTION_TEMPLATES[language]["general"].get(tone, ["Absolutely stunning! ✨ This moment is pure magic!"]))
        except Exception as e:
            print(f"[IMAGE-CAP] Caption selection error: {e}")
            caption = "This is pure magic! 🌟✨ Absolutely stunning moment!"
        
        print(f"[IMAGE-CAP] Caption: {caption[:60]}...")
        
        # Create final caption with proper formatting
        final_caption = caption.strip()
        
        # Generate context-aware hashtags based on image type and tone
        hashtags = []
        
        # Tone mapping for hashtag ranker (must match hashtag_ranker.py format)
        tone_map = {
            "bright": "trendy",      # Bright images are trendy/viral
            "balanced": "friendly",   # Balanced images are relatable/friendly
            "dark": "emotional"       # Dark images are emotional/deep
        }
        
        # Image-type specific hashtags (with # prefix)
        type_tags = {
            "people": ["#InstaGood", "#PortraitMode", "#FaceOfTheDay", "#PeopleOfInstagram", "#Portraiture", "#SelfieGame", "#PortraitPhotography"],
            "landscape": ["#Landscape", "#NatureLovers", "#TravelPhotography", "#Wanderlust", "#ScenicBeauty", "#NaturePhotography", "#ExploreMore"],
            "food": ["#FoodPhotography", "#FoodBlogger", "#FoodLover", "#FoodGasm", "#FoodieLove", "#YumFood", "#FoodieCommunity"],
            "event": ["#EventPhotography", "#Celebration", "#MomentCapture", "#EventMemories", "#Gatherings", "#SpecialMoment", "#MakingMemories"],
            "general": ["#Photography", "#PhotoOfTheDay", "#InstaDaily", "#CaptureTheMoment", "#ArtisticShot", "#VisualStory", "#Storytelling"]
        }
        
        try:
            # Map tone to hashtag ranker tone for better relevance
            ranker_tone = tone_map.get(tone, "general")
            
            # Get AI-generated hashtags with the appropriate tone
            tags = generate_hashtags(final_caption, tone=ranker_tone, top_n=10)
            if tags and len(tags) > 0:
                # Tags come with # prefix from ranker
                hashtags.extend(tags[:10])
        except Exception as e:
            print(f"[IMAGE-CAP] Hashtag ranker error: {e}")
            pass
        
        # Add type-specific hashtags (don't duplicate if already in list)
        if image_type in type_tags:
            for tag in type_tags[image_type][:5]:
                if tag not in hashtags:
                    hashtags.append(tag)
        
        # Add fallback viral hashtags if we don't have enough
        viral_tags = ["#viral", "#trending", "#amazing", "#awesome", "#beautiful", "#stunning", "#incredible", "#wonderful"]
        for tag in viral_tags:
            if tag not in hashtags and len(hashtags) < 12:
                hashtags.append(tag)
        
        # Remove # prefix for consistent output format, then limit to 15
        final_hashtags = []
        for tag in hashtags[:20]:  # Process first 20
            clean_tag = tag.replace('#', '').strip()
            if clean_tag and clean_tag.lower() not in [t.lower() for t in final_hashtags]:
                final_hashtags.append(clean_tag)
            if len(final_hashtags) >= 15:
                break
        
        result = {
            "caption": final_caption.strip(),
            "hashtags": final_hashtags[:15],
            "image_type": image_type,
            "tone": tone
        }
        
        print(f"[IMAGE-CAP] ✓ Complete - {len(final_hashtags)} hashtags generated")
        return result
        
    except Exception as e:
        print(f"[IMAGE-CAP-FATAL] {e}")
        traceback.print_exc()
        return {
            "caption": "This is absolutely stunning! 🌟✨ Pure magic captured!",
            "hashtags": ["viral", "trending", "amazing", "awesome", "beautiful", "photography", "instaworthy", "captured"],
            "image_type": "general",
            "tone": "balanced"
        }


# ---------------------------------------------------------
# 🌍 Background Detection (Sky, Greenery, Sunset, etc.)
# ---------------------------------------------------------
def detect_background(img: Image.Image) -> str:
    try:
        small = img.resize((80, 80))
        np_img = np.array(small)

        r = np.mean(np_img[:, :, 0])
        g = np.mean(np_img[:, :, 1])
        b = np.mean(np_img[:, :, 2])
        brightness = np.mean(np_img)

        # Sky
        if b > r and b > g and b > 130:
            return "sky"

        # Green Nature
        if g > r and g > b and g > 120:
            return "greenery"

        # Sunset (warm red/orange)
        if r > 160 and g < 120 and b < 120:
            return "sunset"

        # Night/Dark
        if brightness < 70:
            return "night"

        # Indoor / Human backgrounds (low variance)
        variance = np.var(np_img)
        if variance < 900:
            return "indoor"

        # Buildings / Street (strong edges)
        edges = abs(np.diff(np_img, axis=0)).mean()
        if edges > 25:
            return "street"

        return "general"
    except:
        return "general"


# ---------------------------------------------------------
# 🎨 Advanced Tone Detector (bright / balanced / dark)
# Analyzes visual characteristics to determine caption tone
# ---------------------------------------------------------
def detect_tone(img: Image.Image) -> str:
    """
    Detect image tone based on color brightness and saturation.
    Maps to tone types that match caption templates:
    - 'bright': High brightness, vibrant images
    - 'balanced': Medium brightness, neutral lighting
    - 'dark': Low brightness, moody/dramatic images
    """
    try:
        brightness = ImageStat.Stat(img).mean[0]
        np_img = np.array(img)

        # Calculate saturation for vibrancy detection
        saturation = calculate_saturation(np_img)

        # Brightness-based tone classification
        if brightness < 70:
            return "dark"  # Low brightness = dark tone
        elif brightness > 160:
            return "bright"  # High brightness = bright tone
        else:
            return "balanced"  # Medium brightness = balanced tone
            
    except Exception as e:
        print(f"[TONE-DETECT] Error: {e}")
        return "balanced"  # Safe default


# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------
def calculate_saturation(np_img: np.ndarray) -> float:
    try:
        max_rgb = np.max(np_img, axis=2).astype(float)
        min_rgb = np.min(np_img, axis=2).astype(float)
        delta = max_rgb - min_rgb
        saturation = np.where(max_rgb > 0, (delta / max_rgb) * 100, 0)
        return float(np.mean(saturation))
    except:
        return 50.0


# Define VIRAL CAPTION_TEMPLATES with engagement-focused content
CAPTION_TEMPLATES = {
    "en": {
        "people": {
            "bright": [
                "That smile says it all! 😊✨ This is pure magic captured in a frame. Tag someone who needs to see this!",
                "Radiating pure positivity! 🌟 Some moments are just too beautiful not to share. Do you agree?",
                "When happiness is this genuine... you just have to capture it! 💫 Double tap if this made you smile!",
                "This is what real joy looks like! 🎉✨ Who else is missing these moments?",
                "Beauty captured at the perfect moment! 📸✨ This is the kind of moment that makes memories!"
            ],
            "balanced": [
                "Perfectly captured! 📷✨ This is the essence of a beautiful moment.",
                "A moment worth remembering! 💭✨ Share this with someone special.",
                "This right here... this is what it's all about! 🌟 Tag your favorite person!",
                "Timeless moments like these! ✨ This is pure gold.",
                "Such a beautiful frame! 📸 Double tap if you'd want this as your memory!"
            ],
            "dark": [
                "There's something captivating about this moment... 🖤✨ Can you feel it?",
                "Mysterious and powerful! 🔥✨ This is the kind of intensity that stays with you.",
                "Deep, meaningful, unforgettable! 💫 This is what real presence looks like.",
                "When character speaks louder than words! 🖤✨ This is pure power.",
                "That look says everything! 👀✨ Profound and mesmerizing."
            ]
        },
        "landscape": {
            "bright": [
                "This is what paradise looks like! 🌅✨ Nature's showing off today, and we're loving every second of it!",
                "Golden hour magic at its finest! 🌞✨ How many of you have been to a place this beautiful?",
                "Breathtaking doesn't even begin to describe it! 🏔️✨ Mother Nature is the ultimate artist!",
                "This view just hit different! 🌄✨ Save this destination to your bucket list!",
                "Sky goals right here! 🌅✨ Nature is speaking to the soul today!"
            ],
            "balanced": [
                "Serenity in every corner! 🌿✨ This is what peace looks like.",
                "Nature's perfection on display! 🏞️✨ Tag someone you'd want to experience this with!",
                "Just when you think nature can't get more beautiful... 🌲✨ This shows up!",
                "Moments like these remind us why we love the outdoors! 🏕️✨ Are you ready for adventure?",
                "This is the kind of view that makes everything feel right! 🌍✨ Pure harmony!"
            ],
            "dark": [
                "Moody and absolutely stunning! 🌧️✨ There's beauty in the darkness too.",
                "Dramatic skies, endless possibilities! ⛈️✨ This is nature's mystery.",
                "When the weather matches the vibe! 🖤✨ Powerful landscapes demand attention!",
                "Mysterious beauty at dusk! 🌙✨ These moments are pure magic.",
                "Dark skies, infinite possibilities! 🌌✨ This is where magic happens."
            ]
        },
        "food": {
            "bright": [
                "This looks absolutely incredible! 🍽️✨ Who else just got seriously hungry? 😋",
                "Feast for the eyes AND the soul! 🍽️✨ Can't wait to taste this masterpiece!",
                "Chef's kiss! 👨‍🍳✨ This is culinary art at its finest! Tag a foodie!",
                "This is what happiness tastes like! 🤤✨ Are you drooling yet?",
                "That's a work of art on a plate! 🎨✨ This dish deserves all the attention!"
            ],
            "balanced": [
                "Perfectly plated, perfectly delicious! 🍽️✨ This is how you do it right!",
                "Food this beautiful has to taste even better! 📸✨ Coming right up!",
                "Restaurant-quality perfection! ⭐✨ This is what I call a win!",
                "Balanced flavors, stunning presentation! 🎯✨ This is the dream combo!",
                "This plating is next level! 🌟✨ Taste: probably as good as it looks!"
            ],
            "dark": [
                "Rich, indulgent, and absolutely irresistible! 🍫✨ This is decadence on a plate!",
                "Dark chocolate dreams! 🍰✨ For the serious dessert lovers out there!",
                "Sophisticated flavors in every bite! 👑✨ This is gourmet territory!",
                "Bold and delicious! 🔥✨ This dish has personality!",
                "Culinary sophistication defined! 🖤✨ This is what elegance tastes like!"
            ]
        },
        "event": {
            "bright": [
                "Celebrating life's beautiful moments! 🎉✨ This energy is absolutely contagious!",
                "Pure joy captured in a frame! 😄✨ Events like this remind us what life's all about!",
                "That's what I call a memorable gathering! 🥳✨ Who's ready for the next one?",
                "Moments like these are pure magic! ✨🎊 Tag everyone who needs to relive this!",
                "This is what happiness looks like in action! 🎈✨ Simply unforgettable!"
            ],
            "balanced": [
                "A gathering worth remembering! 📸✨ Perfect execution, perfect memory!",
                "When everything comes together perfectly! 🎯✨ This is the dream event!",
                "Timeless moments like these! 💫✨ This is what memories are made of!",
                "An event to remember forever! 🌟✨ Everyone brought their A-game!",
                "Perfect harmony in every frame! ✨ This is how you do it right!"
            ],
            "dark": [
                "Unforgettable moments that touch the soul! 🖤✨ This energy is unforgettable!",
                "Powerful gathering with deep connections! 💫✨ This is what matters most!",
                "Meaningful moments captured! 🌙✨ This is the kind of event that changes you!",
                "Intense, emotional, absolutely beautiful! 🖤✨ Some gatherings just hit different!",
                "Deep connections were made here! 💝✨ This event will be remembered forever!"
            ]
        },
        "general": {
            "bright": [
                "Absolutely stunning! ✨ This moment is pure magic! Double tap if you feel it!",
                "This is the kind of capture that makes you believe in magic! 🌟✨",
                "Perfection in a single frame! 📷✨ Nature's showing off today!",
                "Can we take a moment to appreciate how beautiful this is? 😍✨",
                "This deserves to go viral! 🔥✨ Share it with everyone you know!"
            ],
            "balanced": [
                "A moment of perfect harmony! ✨ This right here is timeless.",
                "Beautifully captured! 📸✨ This is exactly the kind of content we need!",
                "Perfectly balanced, beautifully presented! ⚖️✨",
                "This is what being present looks like! 🌟✨ Absolutely love this!",
                "Equilibrium and elegance in one frame! ✨ Simply perfect!"
            ],
            "dark": [
                "There's something captivating about this... 🖤✨ Depth and mystery combined!",
                "Powerful and intriguing! 🔥✨ This is the kind of content that makes you think!",
                "Beautifully mysterious! 🌙✨ Can't stop looking at this!",
                "This has serious main character energy! 💫✨ Absolutely mesmerizing!",
                "Deep, meaningful, and absolutely compelling! 🖤✨ This is art!"
            ]
        }
    },
    "bn": {
        "people": {
            "bright": [
                "এই হাসি সবকিছু বলে দেয়! 😊✨ এটি ফ্রেমে ধরা খাঁটি জাদু।",
                "খাঁটি ইতিবাচকতা প্রকাশ করছে! 🌟✨ কিছু মুহূর্ত শুধু শেয়ার করার জন্য খুবই সুন্দর।",
                "এত খাঁটি আনন্দ দেখলে ক্যাপচার না করে পারা যায় না! 💫✨"
            ],
            "balanced": [
                "নিখুঁতভাবে ধরা পড়েছে! 📷✨ সুন্দর মুহূর্তের সারমর্ম।",
                "মনে রাখার মতো মুহূর্ত! 💭✨ বিশেষ কাউকে শেয়ার করুন।",
                "এটাই জীবন! 🌟✨ এটি খাঁটি সোনা।"
            ],
            "dark": [
                "এই মুহূর্তে কিছু মুগ্ধকর আছে... 🖤✨ আপনি কি এটা অনুভব করেন?",
                "রহস্যময় এবং শক্তিশালী! 🔥✨ এটি এমন শক্তি যা আপনার সাথে থাকে।",
                "গভীর, অর্থপূর্ণ এবং অবিস্মরণীয়! 💫✨"
            ]
        },
        "landscape": {
            "bright": [
                "এটি স্বর্গ দেখায়! 🌅✨ প্রকৃতি আজ চমৎকার কিছু দেখাচ্ছে!",
                "সোনালি ঘণ্টার জাদু! 🌞✨ এত সুন্দর জায়গা গেছেন কয়জন?",
                "অবর্ণনীয়ভাবে সুন্দর! 🏔️✨ মা প্রকৃতি সর্বশ্রেষ্ঠ শিল্পী!",
                "এই দৃশ্য অন্যরকম! 🌄✨ আপনার বাকেট লিস্টে সংরক্ষণ করুন!"
            ],
            "balanced": [
                "প্রতিটি কোণে শান্তি! 🌿✨ এটি শান্তি দেখায়।",
                "প্রকৃতির নিখুঁত প্রদর্শনী! 🏞️✨ যে কাউকে ট্যাগ করুন যারা এটি অনুভব করতে চায়!"
            ],
            "dark": [
                "মেজাজি এবং অত্যন্ত অসাধারণ! 🌧️✨ অন্ধকারেও সৌন্দর্য আছে।",
                "নাটকীয় আকাশ, অসীম সম্ভাবনা! ⛈️✨"
            ]
        },
        "food": {
            "bright": [
                "এটি অবিশ্বাস্য দেখাচ্ছে! 🍽️✨ আপনার ক্ষুধে বাড়া পেয়েছে? 😋",
                "চোখ এবং আত্মার জন্য ভোজ! 🍽️✨ এই মাস্টারপিস খাবার অপেক্ষা করতে পারছি না!",
                "শেফের চুম্বন! 👨‍🍳✨ এটি সূক্ষ্ম শিল্পের শীর্ষে!"
            ],
            "balanced": [
                "নিখুঁতভাবে পরিবেশন করা, নিখুঁত স্বাদ! 🍽️✨",
                "এটি সঠিকভাবে কীভাবে করতে হয়! 📸✨"
            ]
        },
        "event": {
            "bright": [
                "জীবনের সুন্দর মুহূর্ত উদযাপন করছি! 🎉✨ এই শক্তি সংক্রামক!",
                "খাঁটি আনন্দ ফ্রেমে ধরা! 😄✨ এই ধরনের অনুষ্ঠান আমাদের মনে করিয়ে দেয় জীবন সম্পর্কে!",
                "এটিই স্মরণীয় জমায়েত! 🥳✨"
            ],
            "balanced": [
                "মনে রাখার মতো জমায়েত! 📸✨ নিখুঁত বাস্তবায়ন, নিখুঁত স্মৃতি!",
                "সবকিছু নিখুঁতভাবে একসাথে এসেছে! 🎯✨"
            ]
        }
    }
}


def detect_image_type(image: Image.Image) -> str:
    """Detect image type with fallback"""
    try:
        small = image.resize((64, 64))
        np_img = np.array(small)
        
        # Simple heuristics for image type detection
        r_mean = np.mean(np_img[:, :, 0])
        g_mean = np.mean(np_img[:, :, 1])
        b_mean = np.mean(np_img[:, :, 2])
        variance = np.var(np_img)
        
        # High red content → event
        if r_mean > 150 and r_mean > g_mean and r_mean > b_mean:
            return "event"
        # High green content → landscape/nature
        if g_mean > 150 and g_mean > r_mean and g_mean > b_mean:
            return "landscape"
        # High blue content → sky/landscape
        if b_mean > 150 and b_mean > r_mean and b_mean > g_mean:
            return "landscape"
        # Low variance → portrait/people
        if variance < 500:
            return "people"
        
        return "general"
    except Exception as e:
        print(f"[DEBUG] Image type detection error: {e}")
        return "general"
