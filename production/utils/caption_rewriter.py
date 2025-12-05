"""
AI-powered caption rewriter
Transforms fake/spam captions into authentic, human-sounding versions
"""
import re
import random


class CaptionRewriter:
    """Intelligently rewrite captions to improve authenticity"""
    
    # Patterns that indicate fake/spam captions
    SPAM_PATTERNS = {
        'urls': r'(http[s]?://|www\.)\S+',
        'excessive_hashtags': r'#\w+',
        'excessive_punctuation': r'[!?]{2,}',
        'all_caps': r'\b[A-Z]{4,}\b',
        'generic_phrases': [
            r'i\s+am\s+a\s+student',
            r'looking\s+for\s+opportunity|opportunities',
            r'connect\s+with\s+me',
            r'feel\s+free\s+to\s+contact',
            r'dm\s+me',
            r'link\s+in\s+bio',
            r'check\s+this\s+out',
            r'dont?\s+miss\s+this?',
            r'limited\s+time',
            r'act\s+now',
            r'hurry',
            r'grab\s+yours?',
            r'click\s+here',
        ],
        'motivational_cliches': [
            r'blessed',
            r'grateful',
            r'amazing',
            r'awesome',
            r'incredible',
            r'life\s+changing',
            r'success',
            r'goals',
            r'believe\s+in\s+yourself',
            r'never\s+give\s+up',
            r'alhamdulillah',
        ]
    }
    
    AUTHENTIC_TRANSITIONS = [
        'honestly', 'ngl', 'not gonna lie', 'tbh', 'real talk',
        'like', 'literally', 'literally me', 'fr fr',
        'i swear', 'i cant', 'lol', 'lmao', 'smh',
        'idk', 'ig', 'istg'
    ]
    
    CASUAL_REPLACEMENTS = {
        'i am': ['im', 'i\'m'],
        'do not': ['dont', 'don\'t'],
        'cannot': ['can\'t', 'cant'],
        'will not': ['won\'t', 'wont'],
        'you are': ['you\'re', 'ur'],
        'they are': ['they\'re'],
        'we are': ['we\'re'],
        'have not': ['haven\'t', 'havent'],
        'has not': ['hasn\'t', 'hasnt'],
        'is not': ['isn\'t', 'isnt'],
        'am not': ['ain\'t', 'aint'],
    }
    
    @staticmethod
    def remove_spam_elements(caption):
        """Remove obvious spam indicators"""
        text = caption
        
        # Remove URLs
        text = re.sub(CaptionRewriter.SPAM_PATTERNS['urls'], '', text, flags=re.IGNORECASE)
        
        # Reduce excessive hashtags (keep max 2)
        hashtags = re.findall(r'#\w+', text)
        if len(hashtags) > 2:
            for hashtag in hashtags[2:]:
                text = text.replace(hashtag, '')
        
        # Fix excessive punctuation
        text = re.sub(r'[!?]{2,}', r'!', text)
        
        return text.strip()
    
    @staticmethod
    def remove_generic_phrases(caption):
        """Remove templated/generic phrases"""
        text = caption
        
        # Remove generic opening phrases - only EXACT matches
        generic_phrases_exact = [
            r'\bi\s+am\s+a\s+student\b',
            r'\blooking\s+for\s+opportunit(y|ies)\b',
            r'\bconnect\s+with\s+me\b',
            r'\bfeel\s+free\s+to\s+contact\b',
            r'\bdm\s+me\b',
            r'\blink\s+in\s+bio\b',
        ]
        
        for pattern in generic_phrases_exact:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    @staticmethod
    def remove_cliches(caption):
        """Remove motivational cliches"""
        text = caption
        
        # Remove standalone cliche words
        for pattern in CaptionRewriter.SPAM_PATTERNS['motivational_cliches']:
            # Only remove if it's a standalone word/phrase
            text = re.sub(r'\b' + pattern + r'\b', '', text, flags=re.IGNORECASE)
        
        # Clean up extra spaces
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    @staticmethod
    def add_casual_language(caption):
        """Make language more conversational and authentic"""
        text = caption
        
        # Add casual markers at the beginning sometimes
        if random.random() > 0.5 and len(text) > 20:
            casual_start = random.choice(CaptionRewriter.AUTHENTIC_TRANSITIONS)
            if not text.lower().startswith(('honestly', 'ngl', 'tbh', 'fr', 'lol', 'idk')):
                text = f"{casual_start} {text}"
        
        # Replace formal contractions with casual ones
        for formal, casual_options in CaptionRewriter.CASUAL_REPLACEMENTS.items():
            if re.search(r'\b' + formal.replace(' ', r'\s+') + r'\b', text, re.IGNORECASE):
                casual_choice = random.choice(casual_options)
                text = re.sub(r'\b' + formal.replace(' ', r'\s+') + r'\b', casual_choice, text, flags=re.IGNORECASE)
        
        return text.strip()
    
    @staticmethod
    def break_up_sentences(caption):
        """Break long sentences into shorter, more natural segments"""
        # Split on periods, question marks, exclamation marks but keep them
        sentences = re.split(r'([.!?])', caption)
        
        # Reconstruct with natural breaks
        result = []
        for i in range(0, len(sentences), 2):
            if i < len(sentences):
                sentence = sentences[i].strip()
                if sentence:
                    # Add to result
                    if result:
                        result.append(sentence)  # Natural space between sentences
                    else:
                        result.append(sentence)
                    
                    # Add back punctuation if it exists
                    if i + 1 < len(sentences) and sentences[i + 1]:
                        result.append(sentences[i + 1])
        
        # Join with proper spacing
        text = ''.join(result).strip()
        # Clean up spacing around punctuation
        text = re.sub(r'\s+([.!?])', r'\1', text)  # Remove space before punctuation
        text = re.sub(r'([.!?])\s*([a-zA-Z])', r'\1 \2', text)  # Add space after punctuation
        
        return text.strip()
    
    @staticmethod
    def add_personality(caption):
        """Add personal touches that make it more authentic"""
        # Don't add too many personal touches - keep it natural
        additions = [
            "\nanyway idk why im sharing this lol",
            "\nthats it. thats all i got",
            "\nno thoughts head empty",
            "\nbut hey thats just me",
            "\nprobs overthinking this",
        ]
        
        if len(caption) > 50 and random.random() > 0.6:
            caption += random.choice(additions)
        
        return caption.strip()
    
    @staticmethod
    def rewrite(caption):
        """
        Complete rewriting pipeline to transform fake caption into authentic one
        
        Process:
        1. Remove spam elements (URLs, excessive hashtags)
        2. Remove generic phrases
        3. Remove cliches
        4. Add casual language
        5. Break up sentences naturally
        6. Add personality
        """
        if not caption or len(caption.strip()) < 5:
            return "honestly not sure what to say lol"
        
        original_text = caption.strip()
        
        # Step 1: Remove spam
        text = CaptionRewriter.remove_spam_elements(caption)
        
        # Step 2: Remove generic phrases (more conservatively)
        text_after_generic = CaptionRewriter.remove_generic_phrases(text)
        
        # If we removed too much, keep more of the original
        if len(text_after_generic.split()) < 3:
            text = text  # Keep without generic phrase removal
        else:
            text = text_after_generic
        
        # Step 3: Remove cliches
        text = CaptionRewriter.remove_cliches(text)
        
        # If text became too short, keep something
        if len(text.strip()) < 5:
            # Start fresh but keep parts
            words = original_text.split()
            if len(words) > 0:
                text = ' '.join(words[:max(3, len(words)//2)])
            else:
                text = original_text
        
        # Step 4: Add casual language
        text = CaptionRewriter.add_casual_language(text)
        
        # Step 5: Break up sentences
        text = CaptionRewriter.break_up_sentences(text)
        
        # Step 6: Add personality (sometimes)
        if len(text.strip()) > 10:
            text = CaptionRewriter.add_personality(text)
        
        # Final cleanup
        text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
        text = text.strip()
        
        # Ensure we return something meaningful
        if not text or len(text) < 5:
            return "honestly idk what to say here lol"
        
        return text
    
    @staticmethod
    def analyze_fakeness(caption):
        """
        Analyze why a caption is detected as fake
        Returns explanation and specific issues found
        """
        issues = []
        
        # Check for URLs
        if re.search(CaptionRewriter.SPAM_PATTERNS['urls'], caption, re.IGNORECASE):
            issues.append("Contains URLs or links")
        
        # Check for excessive hashtags
        hashtags = re.findall(r'#\w+', caption)
        if len(hashtags) > 2:
            issues.append(f"Too many hashtags ({len(hashtags)} found, keep to 2 max)")
        
        # Check for excessive punctuation
        if re.search(r'[!?]{2,}', caption):
            issues.append("Excessive punctuation (!!!  or ???)")
        
        # Check for ALL CAPS
        all_caps_words = re.findall(r'\b[A-Z]{4,}\b', caption)
        if len(all_caps_words) > 0:
            issues.append(f"Too many ALL CAPS words ({len(all_caps_words)} found)")
        
        # Check for generic phrases
        found_generic = []
        for pattern in CaptionRewriter.SPAM_PATTERNS['generic_phrases']:
            if re.search(pattern, caption, re.IGNORECASE):
                found_generic.append(pattern.replace(r'\s+', ' '))
        if found_generic:
            issues.append(f"Contains generic/templated phrases")
        
        # Check for cliches
        found_cliches = []
        for pattern in CaptionRewriter.SPAM_PATTERNS['motivational_cliches']:
            if re.search(r'\b' + pattern + r'\b', caption, re.IGNORECASE):
                found_cliches.append(pattern.replace(r'\s+', ' '))
        if found_cliches:
            issues.append(f"Contains motivational cliches (e.g., '{found_cliches[0]}')")
        
        # Check for overly formal language
        formal_words = ['opportunity', 'professional', 'endeavor', 'pursuant', 'hereby']
        if any(word in caption.lower() for word in formal_words):
            issues.append("Too formal/professional tone")
        
        return {
            "issues": issues,
            "count": len(issues),
            "summary": " | ".join(issues) if issues else "No specific issues detected"
        }
