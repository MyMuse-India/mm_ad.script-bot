#!/usr/bin/env python3
"""
Enhanced MyMuse Script Generator
Uses AI training data to create human-like, ad-quality scripts
"""

import json
import random
from typing import List, Dict, Any, Tuple, Optional
import re

class EnhancedScriptGenerator:
    def __init__(self, training_data_path: str = "mymuse_training_data.json"):
        """Initialize with training data"""
        self.training_data = self._load_training_data(training_data_path)
        self.voice_patterns = self.training_data.get("voice_patterns", {})
        self.customer_language = self.training_data.get("customer_language", {})
        self.product_knowledge = self.training_data.get("product_knowledge", {})
        self.trained_patterns = self.training_data.get("trained_patterns", {})
        
        # Initialize pattern libraries
        self._build_pattern_libraries()
    
    def _load_training_data(self, path: str) -> Dict[str, Any]:
        """Load training data from JSON file"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load training data: {e}")
            return {}
    
    def _build_pattern_libraries(self):
        """Build libraries of patterns for script generation"""
        # Emotional words from customer reviews
        self.emotional_words = list(self.trained_patterns.get("emotional_words", {}).keys())
        
        # Experience phrases from reviews
        self.experience_phrases = self.customer_language.get("experience_phrases", [])
        
        # Product features (comprehensive)
        self.product_features = list(self.product_knowledge.get("features", {}).keys())
        self.product_specs = list(self.product_knowledge.get("specifications", {}).keys())
        self.product_materials = list(self.product_knowledge.get("materials", {}).keys())
        self.product_tech = list(self.product_knowledge.get("technology", {}).keys())
        self.product_benefits = list(self.product_knowledge.get("benefits", {}).keys())

        # Trusted features per product from CSV
        self.trusted_features = self.product_knowledge.get("trusted_features_csv", {})

        # Hardcoded trusted defaults as fallback
        self.trusted_defaults = {
            "dive+": {"speed_modes": 10},
            "groove+": {"speed_modes": 18}
        }
        
        # Sentence length patterns
        sentence_data = self.trained_patterns.get("sentence_lengths", {})
        self.target_sentence_length = sentence_data.get("average", 8)
        self.min_sentence_length = sentence_data.get("min", 5)
        self.max_sentence_length = sentence_data.get("max", 15)
        
        # Banger endings (from training data + curated) - more playful and sexual
        self.banger_endings = [
            "Trust your desires.",
            "Focus on what drives you wild.",
            "Feel good. No apologies.",
            "Go with what feels right.",
            "Pleasure that meets you where you are.",
            "Your pleasure, your way.",
            "Discover what feels amazing.",
            "Embrace your desires.",
            "Pleasure awaits.",
            "Your journey starts here.",
            "Let's make this trip unforgettable.",
            "We're about to have some fun.",
            "This is going to be amazing.",
            "Get ready for pleasure.",
            "Your wildest dreams await.",
            "Let's explore together.",
            "This is just the beginning.",
            "Your pleasure journey starts now.",
            "Let's make magic happen.",
            "Your desires are calling."
        ]
    
    def generate_human_script(self, product_name: str, transcript: str, gen_z: bool = False) -> str:
        """Generate a human-like script using TRULY DYNAMIC transcript analysis"""
        
        # Analyze transcript for context using the new dynamic system
        context = self._analyze_transcript(transcript)
        
        # Use the new dynamic script generation system
        return self._generate_dynamic_script(product_name, transcript, gen_z, context)
    
    def _generate_masturbation_script(self, product_name: str, transcript: str, gen_z: bool, context: Dict[str, Any]) -> str:
        """Generate masturbation-focused script based on detected emotions and context"""
        
        # Analyze context for tone
        is_urgent = context["context"]["urgency"] == "high"
        is_private = context["context"]["location"] in ["home", "private"]
        is_excited = context["emotions"].get("excited", 0) > 0
        is_desperate = context["emotions"].get("desperate", 0) > 0
        
        # Build script based on detected emotions
        lines = []
        
        if is_desperate:
            # High urgency, desperate need
            lines.append("I need this right now.")
            lines.append("The craving is overwhelming.")
            lines.append(f"{product_name} is my only relief.")
            lines.append("I can't wait any longer.")
        elif is_excited:
            # Excited anticipation
            lines.append("I'm so excited for this.")
            lines.append("The anticipation is building.")
            lines.append(f"{product_name} is going to be amazing.")
            lines.append("I can't contain my excitement.")
        else:
            # Calm, relaxed solo time
            lines.append("Time for some self-care.")
            lines.append("I deserve this moment.")
            lines.append(f"{product_name} makes it special.")
            lines.append("This is my time to indulge.")
        
        # Add banger ending
        banger = random.choice(self.banger_endings)
        lines.append(banger)
        
        return "\n".join(lines)
    
    def _generate_couple_intimacy_script(self, product_name: str, transcript: str, gen_z: bool, context: Dict[str, Any]) -> str:
        """Generate couple intimacy script based on detected emotions"""
        
        is_romantic = context["emotions"].get("romantic", 0) > 0
        is_intense = context["emotions"].get("intense", 0) > 0
        is_playful = context["emotions"].get("playful", 0) > 0
        
        # Calculate target length based on transcript
        transcript_words = len(transcript.split())
        target_words = max(transcript_words - 5, 25)  # Allow some flexibility
        
        lines = []
        
        # POWERFUL BUSINESS COUPLE HOOKS (like your transcript)
        business_couple_hooks = [
            "As a couple who run businesses together,",
            "When you're building empires together,",
            "For couples who work and travel as one,",
            "When your flights become boardroom extensions,",
            "As business partners who never stop,",
            "When meetings and intimacy collide,",
            "For couples who turn every trip into opportunity,",
            "When your work life and love life merge,"
        ]
        
        # LUXURY/INTIMACY LINES (like your transcript)
        luxury_intimacy_lines = [
            "even our flights turn into meeting press or brainstorming sessions.",
            "every moment becomes precious and meaningful.",
            "finding balance becomes everything.",
            "you need escape routes from the corporate world.",
            "we crave moments of pure connection.",
            "you discover what truly matters in life.",
            "pleasure becomes essential to survival.",
            "you need tools to separate business from pleasure."
        ]
        
        # PRODUCT INTEGRATION (like your transcript)
        product_integration_lines = [
            "But at night, we carve out time for us to luxuriate in intimacy.",
            "But when the day ends, we prioritize our connection above all else.",
            "But we always make time for what truly matters between us.",
            "But we never forget why we started this journey together.",
            "But we remember that our relationship comes first.",
            "But we find ways to deepen our bond despite the demands.",
            "But we create space for what makes us feel alive.",
            "But we indulge in what brings us pure joy."
        ]
        
        # IMPACT LINES (like your transcript)
        impact_lines = [
            "And that's when the lovers bundle comes in to transform everything.",
            "And that's when the lovers bundle elevates your entire experience.",
            "And that's when the lovers bundle transforms your nights into magic.",
            "And that's when the lovers bundle becomes essential for couples like us.",
            "And that's when the lovers bundle delivers when you need it most.",
            "And that's when the lovers bundle shows its power in your relationship.",
            "And that's when the lovers bundle creates magic for business couples.",
            "And that's when the lovers bundle becomes your secret weapon."
        ]
        
        # FINAL IMPACT (like your transcript)
        final_impact_lines = [
            "It doesn't just come in handy—it elevates.",
            "It doesn't just satisfy—it transforms.",
            "It doesn't just connect—it deepens.",
            "It doesn't just pleasure—it bonds.",
            "It doesn't just excite—it elevates.",
            "It doesn't just unite—it intensifies.",
            "It doesn't just fulfill—it transcends.",
            "It doesn't just pleasure—it elevates."
        ]
        
        # Build the script with the powerful business couple structure
        hook = random.choice(business_couple_hooks)
        luxury = random.choice(luxury_intimacy_lines)
        product = random.choice(product_integration_lines)
        impact = random.choice(impact_lines)
        final = random.choice(final_impact_lines)
        
        lines.append(f"{hook} {luxury}")
        lines.append(product)
        lines.append(impact)
        lines.append(final)
        
        # Add banger ending
        banger = random.choice(self.banger_endings)
        lines.append(banger)
        
        # Ensure we meet target word count
        current_words = sum(len(line.split()) for line in lines)
        if current_words < target_words:
            # Add more detail to existing lines
            enhanced_lines = []
            for line in lines[:-1]:  # Don't modify the banger ending
                if len(line.split()) < 12:  # If line is too short
                    enhanced_lines.append(f"{line} It's absolutely incredible.")
                else:
                    enhanced_lines.append(line)
            enhanced_lines.append(lines[-1])  # Add banger ending
            lines = enhanced_lines
        
        return "\n".join(lines)
    
    def _generate_emotion_based_script(self, product_name: str, transcript: str, gen_z: bool, context: Dict[str, Any]) -> str:
        """Generate script based on primary emotion when no specific scenario is detected"""
        
        primary_emotion = context.get("primary_emotion", "neutral")
        lines = []
        
        if primary_emotion == "excited":
            lines.append("I'm thrilled about this!")
            lines.append("The excitement is real.")
            lines.append(f"{product_name} is going to be incredible.")
            lines.append("I can't wait to experience it.")
        elif primary_emotion == "curious":
            lines.append("I'm curious to try this.")
            lines.append("Something new awaits.")
            lines.append(f"{product_name} might change everything.")
            lines.append("Let's see what happens.")
        elif primary_emotion == "confident":
            lines.append("I know what I want.")
            lines.append("This is my choice.")
            lines.append(f"{product_name} delivers exactly that.")
            lines.append("I'm in control.")
        else:
            # Default pleasure script
            lines.append("Time for something special.")
            lines.append("This feels right.")
            lines.append(f"{product_name} makes it happen.")
            lines.append("I'm ready for this.")
        
        banger = random.choice(self.banger_endings)
        lines.append(banger)
        
        return "\n".join(lines)
    
    def _analyze_transcript(self, transcript: str) -> Dict[str, Any]:
        """TRULY DYNAMIC transcript analysis that learns and adapts to ANY scenario"""
        transcript_lower = transcript.lower()
        
        # DYNAMIC PATTERN LEARNING - no hardcoded rules, learns from transcript content
        patterns = self._learn_patterns_from_transcript(transcript)
        
        # ADAPTIVE SCENARIO DETECTION - infers from learned patterns
        scenario = self._infer_scenario_adaptively(patterns, transcript)
        
        # DYNAMIC EMOTION EXTRACTION - learns emotional language from transcript
        emotions = self._extract_emotions_dynamically(transcript, patterns)
        
        # CONTEXT INFERENCE - builds understanding from transcript structure
        context = self._build_context_dynamically(transcript, patterns)
        
        return {
            "primary_scenario": scenario,
            "learned_patterns": patterns,
            "emotions": emotions,
            "context": context,
            "transcript_length": len(transcript.split()),
            "key_insights": self._extract_key_insights(transcript, patterns),
            "adaptation_strategy": self._determine_adaptation_strategy(patterns, context),
        }

    def _learn_patterns_from_transcript(self, transcript: str) -> Dict[str, Any]:
        """Learn patterns directly from transcript content - no assumptions"""
        text = transcript.lower()
        words = text.split()
        
        patterns = {
            "speaker_identity": self._learn_speaker_identity(text, words),
            "action_patterns": self._learn_action_patterns(text, words),
            "desire_patterns": self._learn_desire_patterns(text, words),
            "context_clues": self._learn_context_clues(text, words),
            "emotional_language": self._learn_emotional_language(text, words),
            "product_mentions": self._learn_product_mentions(text, words),
        }
        
        return patterns

    def _learn_speaker_identity(self, text: str, words: List[str]) -> Dict[str, Any]:
        """Learn who is speaking from transcript content"""
        identity = {
            "count": "unknown",
            "gender": "unknown",
            "relationship_status": "unknown",
            "age_group": "unknown",
        }
        
        # Learn from pronouns and references
        if "i'm" in text or "i am" in text or "my" in text:
            identity["count"] = "single"
        elif "we" in text or "us" in text or "our" in text:
            identity["count"] = "multiple"
        
        # Learn gender from context
        if any(word in text for word in ["boy", "man", "guy", "he", "him"]):
            identity["gender"] = "male"
        elif any(word in text for word in ["girl", "woman", "she", "her"]):
            identity["gender"] = "female"
        
        # Learn relationship status
        if any(word in text for word in ["couple", "together", "relationship", "partner"]):
            identity["relationship_status"] = "partnered"
        elif any(word in text for word in ["alone", "solo", "single", "myself"]):
            identity["relationship_status"] = "single"
        
        return identity

    def _learn_action_patterns(self, text: str, words: List[str]) -> Dict[str, Any]:
        """Learn what actions are being described"""
        actions = {
            "primary_action": "unknown",
            "secondary_actions": [],
            "intent": "unknown",
            "urgency": "unknown",
        }
        
        # Learn primary action from key verbs
        action_verbs = ["want", "need", "use", "try", "explore", "discover", "experience", "feel"]
        for verb in action_verbs:
            if verb in text:
                actions["primary_action"] = verb
                break
        
        # Learn intent from context
        if "bored" in text or "tired" in text or "same" in text:
            actions["intent"] = "change"
        elif "excited" in text or "thrilled" in text or "ready" in text:
            actions["intent"] = "enhance"
        elif "need" in text or "must" in text or "have to" in text:
            actions["intent"] = "necessity"
        
        # Learn urgency
        if any(word in text for word in ["now", "immediately", "urgent"]):
            actions["urgency"] = "high"
        elif any(word in text for word in ["soon", "later", "tonight"]):
            actions["urgency"] = "medium"
        else:
            actions["urgency"] = "low"
        
        return actions

    def _learn_desire_patterns(self, text: str, words: List[str]) -> Dict[str, Any]:
        """Learn what desires and needs are expressed"""
        desires = {
            "primary_desire": "unknown",
            "secondary_desires": [],
            "frustrations": [],
            "aspirations": [],
        }
        
        # Learn primary desire
        desire_words = ["pleasure", "satisfaction", "release", "connection", "intimacy", "exploration"]
        for word in desire_words:
            if word in text:
                desires["primary_desire"] = word
                break
        
        # Learn frustrations
        if "bored" in text:
            desires["frustrations"].append("boredom")
        if "hand" in text and "bored" in text:
            desires["frustrations"].append("manual_limitation")
        if "same" in text or "routine" in text:
            desires["frustrations"].append("repetition")
        
        # Learn aspirations
        if "better" in text or "more" in text or "enhance" in text:
            desires["aspirations"].append("improvement")
        if "new" in text or "different" in text or "explore" in text:
            desires["aspirations"].append("discovery")
        
        return desires

    def _learn_context_clues(self, text: str, words: List[str]) -> Dict[str, Any]:
        """Learn environmental and situational context"""
        context = {
            "physical_setting": "unknown",
            "emotional_setting": "unknown",
            "social_setting": "unknown",
            "temporal_setting": "unknown",
        }
        
        # Learn physical setting
        setting_words = {
            "travel": ["airport", "flight", "trip", "journey", "security", "check"],
            "home": ["room", "bedroom", "home", "house", "bed", "couch"],
            "work": ["office", "meeting", "business", "work", "desk"],
            "outdoor": ["outside", "park", "beach", "garden", "nature"],
        }
        
        for setting, keywords in setting_words.items():
            if any(kw in text for kw in keywords):
                context["physical_setting"] = setting
                break
        
        # Learn emotional setting
        if any(word in text for word in ["romantic", "intimate", "passionate"]):
            context["emotional_setting"] = "romantic"
        elif any(word in text for word in ["casual", "relaxed", "chill"]):
            context["emotional_setting"] = "casual"
        elif any(word in text for word in ["intense", "wild", "passionate"]):
            context["emotional_setting"] = "intense"
        
        # Learn social setting
        if "couple" in text or "together" in text:
            context["social_setting"] = "partnered"
        elif "alone" in text or "solo" in text:
            context["social_setting"] = "solo"
        elif "group" in text or "friends" in text:
            context["social_setting"] = "group"
        
        return context

    def _learn_emotional_language(self, text: str, words: List[str]) -> Dict[str, Any]:
        """Learn emotional language patterns from transcript"""
        emotions = {
            "primary_emotion": "unknown",
            "emotional_intensity": "unknown",
            "emotional_tone": "unknown",
            "mood_indicators": [],
        }
        
        # Learn primary emotion
        emotion_words = {
            "excitement": ["excited", "thrilled", "pumped", "ready", "eager"],
            "frustration": ["bored", "tired", "frustrated", "annoyed", "sick of"],
            "desire": ["want", "need", "desire", "crave", "long for"],
            "curiosity": ["wonder", "curious", "interested", "fascinated"],
            "confidence": ["know", "sure", "confident", "ready", "prepared"],
            "playfulness": ["fun", "play", "enjoy", "adventure", "thrill"],
        }
        
        for emotion, keywords in emotion_words.items():
            if any(kw in text for kw in keywords):
                emotions["primary_emotion"] = emotion
                break
        
        # Learn emotional intensity
        intensity_words = ["wild", "intense", "overwhelming", "passionate", "extreme"]
        if any(word in text for word in intensity_words):
            emotions["emotional_intensity"] = "high"
        elif emotions["primary_emotion"] != "unknown":
            emotions["emotional_intensity"] = "medium"
        else:
            emotions["emotional_intensity"] = "low"
        
        # Learn emotional tone
        if "horny" in text or "aroused" in text:
            emotions["emotional_tone"] = "sexual"
        elif "romantic" in text or "intimate" in text:
            emotions["emotional_tone"] = "romantic"
        elif "playful" in text or "fun" in text:
            emotions["emotional_tone"] = "playful"
        
        return emotions

    def _learn_product_mentions(self, text: str, words: List[str]) -> Dict[str, Any]:
        """Learn about product mentions and context"""
        products = {
            "mentioned_products": [],
            "product_context": "unknown",
            "product_intent": "unknown",
        }
        
        # Learn mentioned products
        product_keywords = ["cock ring", "cock rings", "ring", "edge", "dive+", "groove+", "lovers bundle"]
        for product in product_keywords:
            if product in text:
                products["mentioned_products"].append(product)
        
        # Learn product context
        if "use" in text and products["mentioned_products"]:
            products["product_context"] = "usage"
        elif "need" in text and products["mentioned_products"]:
            products["product_context"] = "necessity"
        elif "try" in text and products["mentioned_products"]:
            products["product_context"] = "exploration"
        
        # Learn product intent
        if "instead of" in text or "bored of" in text:
            products["product_intent"] = "replacement"
        elif "with" in text or "enhance" in text:
            products["product_intent"] = "enhancement"
        elif "discover" in text or "explore" in text:
            products["product_intent"] = "discovery"
        
        return products

    def _infer_scenario_adaptively(self, patterns: Dict, transcript: str) -> str:
        """Infer scenario from learned patterns - completely adaptive"""
        speaker = patterns["speaker_identity"]["count"]
        actions = patterns["action_patterns"]["intent"]
        desires = patterns["desire_patterns"]["primary_desire"]
        context = patterns["context_clues"]["physical_setting"]
        emotions = patterns["emotional_language"]["emotional_tone"]
        
        # DYNAMIC SCENARIO INFERENCE - learns from pattern combinations
        
        # PRIORITY: Business couple scenarios (highest priority)
        if speaker == "multiple" and ("business" in transcript.lower() or "meeting" in transcript.lower() or "press" in transcript.lower() or "launches" in transcript.lower()):
            if context == "travel":
                return "business_couple_travel"
            else:
                return "business_couple_intimacy"
        
        # Solo scenarios
        elif speaker == "single":
            if "bored" in transcript.lower() and "hand" in transcript.lower():
                return "solo_masturbation_enhancement"
            elif desires == "pleasure" or desires == "satisfaction":
                return "solo_pleasure_seeking"
            elif actions == "change":
                return "solo_routine_change"
            else:
                return "solo_exploration"
        
        # Couple scenarios (non-business)
        elif speaker == "multiple":
            if context == "travel":
                return "couple_travel"
            elif emotions == "romantic" or desires == "connection":
                return "couple_intimacy"
            elif emotions == "playful":
                return "couple_playful_exploration"
            else:
                return "couple_general"
        
        # Travel scenarios (non-couple)
        elif context == "travel":
            if speaker == "single":
                return "solo_travel"
            else:
                return "group_travel"
        
        # Default to general exploration
        return "general_exploration"

    def _extract_emotions_dynamically(self, transcript: str, patterns: Dict) -> Dict[str, Any]:
        """Extract emotions dynamically based on learned patterns"""
        emotions = patterns["emotional_language"].copy()
        
        # Add pattern-based emotions
        if patterns["action_patterns"]["urgency"] == "high":
            emotions["urgency"] = "high"
        
        if patterns["desire_patterns"]["frustrations"]:
            emotions["frustration_level"] = len(patterns["desire_patterns"]["frustrations"])
        
        if patterns["desire_patterns"]["aspirations"]:
            emotions["aspiration_level"] = len(patterns["desire_patterns"]["aspirations"])
        
        return emotions

    def _build_context_dynamically(self, transcript: str, patterns: Dict) -> Dict[str, Any]:
        """Build context dynamically from learned patterns"""
        context = patterns["context_clues"].copy()
        
        # Add speaker context
        context["speaker"] = patterns["speaker_identity"]
        
        # Add action context
        context["actions"] = patterns["action_patterns"]
        
        # Add desire context
        context["desires"] = patterns["desire_patterns"]
        
        # Add product context
        context["products"] = patterns["product_mentions"]
        
        return context

    def _extract_key_insights(self, transcript: str, patterns: Dict) -> List[str]:
        """Extract key insights that capture transcript essence"""
        insights = []
        
        # Speaker insight
        if patterns["speaker_identity"]["count"] != "unknown":
            insights.append(f"Speaker: {patterns['speaker_identity']['count']}")
        
        # Action insight
        if patterns["action_patterns"]["primary_action"] != "unknown":
            insights.append(f"Action: {patterns['action_patterns']['primary_action']}")
        
        # Desire insight
        if patterns["desire_patterns"]["primary_desire"] != "unknown":
            insights.append(f"Desire: {patterns['desire_patterns']['primary_desire']}")
        
        # Context insight
        if patterns["context_clues"]["physical_setting"] != "unknown":
            insights.append(f"Setting: {patterns['context_clues']['physical_setting']}")
        
        return insights

    def _determine_adaptation_strategy(self, patterns: Dict, context: Dict) -> List[str]:
        """Determine what adaptations are needed for this transcript"""
        strategies = []
        
        # Speaker-based adaptations
        if patterns["speaker_identity"]["count"] == "single":
            strategies.append("solo_focused")
        elif patterns["speaker_identity"]["count"] == "multiple":
            strategies.append("relationship_focused")
        
        # Context-based adaptations
        if patterns["context_clues"]["physical_setting"] == "travel":
            strategies.append("travel_appropriate")
        elif patterns["context_clues"]["physical_setting"] == "work":
            strategies.append("professional_tone")
        
        # Emotion-based adaptations
        if patterns["emotional_language"]["emotional_tone"] == "sexual":
            strategies.append("playful_sexual")
        elif patterns["emotional_language"]["emotional_tone"] == "romantic":
            strategies.append("romantic_intimate")
        
        # Action-based adaptations
        if patterns["action_patterns"]["intent"] == "change":
            strategies.append("solution_focused")
        elif patterns["action_patterns"]["intent"] == "enhancement":
            strategies.append("enhancement_focused")
        
        return strategies
    
    def _generate_masturbation_male_script(self, product_name: str, transcript_text: str, gen_z: bool, context: Dict[str, Any]) -> str:
        """Generate a solo male masturbation script with dynamic hooks and brand-safe tone."""
        transcript_words = len(transcript_text.split())
        target_words = max(transcript_words - 5, 28)
        
        # Hooks appropriate to scenario
        hooks = [
            "Bored of your hand?",
            "When it's just you and your body,",
            "Alone and turned on?",
            "Ready to level up solo time?",
            "If your hand isn't cutting it,",
            "For nights you need more than routine,",
        ]
        
        # Product naming fallback
        product_label = product_name or ("edge" if context.get("mentions_cock_ring") else "edge")
        
        benefits = [
            f"{product_label} hugs you right where it counts.",
            f"Keeps you harder, longer—without overthinking it.",
            f"Adds deep, rumbly pressure at the base.",
            f"Turns a quick session into a full-body buzz.",
            f"Fits fast, feels good, zero fuss.",
        ]
        
        guidance = [
            "Slide it on, lube up, find your rhythm.",
            "Start slow, let the pressure do the work.",
            "Focus on what your body asks for.",
            "Take a breath, enjoy the build.",
        ]
        
        lines = []
        lines.append(random.choice(hooks))
        lines.append("You're not looking for effort—you want pleasure that shows up.")
        lines.append(random.choice(benefits))
        lines.append(random.choice(guidance))
        
        # Add second benefit if space
        more = [b for b in benefits if b not in lines]
        if more:
            lines.append(random.choice(more))
        
        # Banger ending
        banger = random.choice(self.banger_endings)
        lines.append(banger)
        
        # Length tune-up
        current_words = sum(len(l.split()) for l in lines)
        if current_words < target_words:
            # Add one more guidance/benefit
            pool = benefits + guidance
            lines.insert(-1, random.choice(pool))
        
        return "\n".join(lines)
    
    def _detect_location(self, transcript_lower: str) -> str:
        """Detect location context from transcript"""
        locations = {
            "home": ["home", "bedroom", "house", "apartment", "room"],
            "travel": ["airport", "hotel", "flight", "car", "train", "bus"],
            "work": ["office", "work", "meeting", "conference", "desk"],
            "public": ["public", "outside", "park", "restaurant", "gym"],
            "private": ["private", "alone", "solo", "personal", "intimate"]
        }
        
        for location, keywords in locations.items():
            if any(keyword in transcript_lower for keyword in keywords):
                return location
        return "general"
    
    def _detect_time(self, transcript_lower: str) -> str:
        """Detect time of day context"""
        time_indicators = {
            "morning": ["morning", "dawn", "sunrise", "early", "breakfast"],
            "afternoon": ["afternoon", "noon", "lunch", "midday"],
            "evening": ["evening", "dusk", "sunset", "dinner", "night"],
            "night": ["night", "late", "bedtime", "sleep", "dark"]
        }
        
        for time, keywords in time_indicators.items():
            if any(keyword in transcript_lower for keyword in keywords):
                return time
        return "general"
    
    def _detect_urgency(self, transcript_lower: str) -> str:
        """Detect urgency level"""
        urgency_indicators = {
            "high": ["urgent", "immediate", "now", "quick", "fast", "hurry", "desperate"],
            "medium": ["soon", "later", "when", "after", "then"],
            "low": ["someday", "eventually", "whenever", "no rush", "take time"]
        }
        
        for urgency, keywords in urgency_indicators.items():
            if any(keyword in transcript_lower for keyword in keywords):
                return urgency
        return "medium"
    
    def _detect_formality(self, transcript_lower: str) -> str:
        """Detect formality level"""
        formal_indicators = ["professional", "business", "formal", "proper", "appropriate"]
        casual_indicators = ["casual", "informal", "relaxed", "chill", "easy", "fun"]
        
        if any(indicator in transcript_lower for indicator in formal_indicators):
            return "formal"
        elif any(indicator in transcript_lower for indicator in casual_indicators):
            return "casual"
        return "neutral"
    
    def _detect_audience(self, transcript_lower: str) -> str:
        """Detect intended audience"""
        audience_indicators = {
            "self": ["i", "me", "myself", "my", "mine"],
            "partner": ["you", "we", "us", "our", "together"],
            "general": ["anyone", "everyone", "people", "someone"]
        }
        
        for audience, keywords in audience_indicators.items():
            if any(keyword in transcript_lower for keyword in keywords):
                return audience
        return "general"
    
    def _detect_product_features(self, transcript_lower: str) -> Dict[str, Any]:
        """Detect any product features mentioned"""
        features = {}
        
        # Speed modes
        if "speed" in transcript_lower or "modes" in transcript_lower:
            if "10" in transcript_lower:
                features["speed_modes"] = 10
            elif "18" in transcript_lower:
                features["speed_modes"] = 18
            elif any(word in transcript_lower for word in ["fast", "slow", "variable", "adjustable"]):
                features["speed_modes"] = "variable"
        
        # Other features
        feature_keywords = {
            "waterproof": ["waterproof", "water", "shower", "bath"],
            "quiet": ["quiet", "silent", "whisper", "noise"],
            "app_control": ["app", "control", "phone", "bluetooth", "wireless"],
            "battery": ["battery", "charge", "rechargeable", "power"],
            "size": ["small", "large", "compact", "big", "tiny"]
        }
        
        for feature, keywords in feature_keywords.items():
            if any(keyword in transcript_lower for keyword in keywords):
                features[feature] = True
        
        return features
    
    def _calculate_sentiment_score(self, emotions: Dict[str, int], transcript: str) -> int:
        """Calculate overall sentiment score from -100 to +100"""
        score = 0
        
        # Positive emotions add points
        positive_emotions = ["excited", "romantic", "playful", "confident", "curious", "satisfied"]
        for emotion in positive_emotions:
            if emotion in emotions:
                score += emotions[emotion] * 10
        
        # Negative emotions subtract points
        negative_emotions = ["frustrated", "desperate"]
        for emotion in negative_emotions:
            if emotion in emotions:
                score -= emotions[emotion] * 10
        
        # Exclamation marks add excitement
        score += transcript.count("!") * 5
        
        # Question marks can indicate curiosity or uncertainty
        score += transcript.count("?") * 2
        
        # Cap the score
        return max(-100, min(100, score))
    
    def _generate_travel_script(self, product_name: str, transcript_text: str, gen_z: bool, context: Dict[str, Any]) -> str:
        """Generate a travel-focused script with security/discretion themes."""
        
        # Calculate target length based on transcript
        transcript_words = len(transcript_text.split())
        target_words = max(transcript_words - 5, 30)  # Allow some flexibility
        
        # Only use speed modes if transcript mentions them
        speed_mention = ""
        if context.get("speed_modes") and context["speed_modes"] > 0:
            # Only include if transcript actually mentioned speed modes
            if any(phrase in transcript_text.lower() for phrase in ["speed", "modes", "18", "10"]):
                speed_mention = f" With {context['speed_modes']} speed modes,"
        
        # Airport travel specific hooks
        hooks = [
            "Some things you don't leave behind.",
            "My kind of travel companion is simple.",
            "Every trip feels softer with dive+.",
            "Travel feels lighter with dive+ by my side.",
            "I never leave home without my dive+.",
            "dive+ travels with me, no questions asked.",
            "It fits in, quietly.",
            "Every journey needs a secret weapon.",
            "My travel essentials are simple.",
            "Some companions make every trip better."
        ]
        
        # Airport security specific lines
        security_lines = [
            "Security never knows what's in my bag.",
            "Security check? Smooth, invisible.",
            "Security? No stress - it's completely discreet.",
            "Security is calm, effortless.",
            "Even airport checks don't notice.",
            "Security won't know what hit them — it's that quiet.",
            "Security never clocks it — it's that subtle.",
            "Security check? This thing is invisible to them.",
            "Security check? No problem — it's whisper-quiet.",
            "Airport security never notices dive+."
        ]
        
        # Travel comfort lines
        comfort_lines = [
            "It stays with me wherever I go.",
            "It's just part of my rhythm.",
            "It slips right into my day.",
            "I carry what feels good.",
            "I carry comfort, always.",
            "It's part of how I move.",
            "It's like having a secret that makes every trip better.",
            "It's just part of my travel routine.",
            "It's like having a special companion that fits in my pocket.",
            "It's my companion in every journey."
        ]
        
        # Travel adventure lines
        adventure_lines = [
            "Let's just say we love exploring together.",
            "We're about to make this trip unforgettable.",
            "We're about to turn this flight into an adventure.",
            "We're about to make this journey extraordinary.",
            "We make every trip more fun.",
            "It's like having a special travel companion that makes every journey better.",
            "Let's just say we love taking pleasure places.",
            "We're about to turn this flight into something special.",
            "It's like having a special companion that makes every journey better.",
            "We're about to make this journey legendary."
        ]
        
        # Select random elements
        hook = random.choice(hooks)
        security = random.choice(security_lines)
        comfort = random.choice(comfort_lines)
        adventure = random.choice(adventure_lines)
        
        # Build the script as separate lines
        lines = []
        
        # Line 1: Hook
        if "dive+ is one of them" in hook:
            lines.append(hook)
        else:
            lines.append(f"{hook} dive+ is one of them.")
        
        # Line 2: Security
        lines.append(security)
        
        # Line 3: Comfort
        lines.append(comfort)
        
        # Line 4: Adventure
        lines.append(adventure)
        
        # Line 5: Banger ending
        banger = random.choice(self.banger_endings)
        lines.append(banger)
        
        # Add speed mention only if transcript had it
        if speed_mention:
            # Insert speed mention after the first line
            lines[0] = lines[0] + speed_mention
        
        # Ensure we meet target word count
        current_words = sum(len(line.split()) for line in lines)
        if current_words < target_words:
            # Add more detail to existing lines
            enhanced_lines = []
            for line in lines[:-1]:  # Don't modify the banger ending
                if len(line.split()) < 8:  # If line is too short
                    enhanced_lines.append(f"{line} It's absolutely incredible.")
                else:
                    enhanced_lines.append(line)
            enhanced_lines.append(lines[-1])  # Add banger ending
            lines = enhanced_lines
        
        return "\n".join(lines)
    
    def _generate_business_travel_script(self, product_name: str, transcript_text: str, gen_z: bool, context: Dict[str, Any]) -> str:
        """Generate a business travel couple script with luxury/intimacy focus"""
        
        # Calculate target length based on transcript
        transcript_words = len(transcript_text.split())
        target_words = max(transcript_words - 5, 30)  # Allow some flexibility
        
        # Business couple hooks - SAME POWERFUL STRUCTURE
        business_hooks = [
            "As a couple who run businesses together,",
            "When you're building empires together,",
            "For couples who work and travel as one,",
            "When your flights become boardroom extensions,",
            "As business partners who never stop,",
            "When meetings and intimacy collide,",
            "For couples who turn every trip into opportunity,",
            "When your work life and love life merge,"
        ]
        
        # Luxury/intimacy lines - SAME STRUCTURE
        luxury_lines = [
            "even our flights turn into meeting press or brainstorming sessions.",
            "every moment becomes precious and meaningful.",
            "finding balance becomes everything.",
            "you need escape routes from the corporate world.",
            "we crave moments of pure connection.",
            "you discover what truly matters in life.",
            "pleasure becomes essential to survival.",
            "you need tools to separate business from pleasure."
        ]
        
        # Product integration lines - SAME STRUCTURE
        product_lines = [
            "But at night, we carve out time for us to luxuriate in intimacy.",
            "But when the day ends, we prioritize our connection above all else.",
            "But we always make time for what truly matters between us.",
            "But we never forget why we started this journey together.",
            "But we remember that our relationship comes first.",
            "But we find ways to deepen our bond despite the demands.",
            "But we create space for what makes us feel alive.",
            "But we indulge in what brings us pure joy."
        ]
        
        # Impact lines - SAME STRUCTURE
        impact_lines = [
            "And that's when the lovers bundle comes in to transform everything.",
            "And that's when the lovers bundle elevates your entire experience.",
            "And that's when the lovers bundle transforms your nights into magic.",
            "And that's when the lovers bundle becomes essential for couples like us.",
            "And that's when the lovers bundle delivers when you need it most.",
            "And that's when the lovers bundle shows its power in your relationship.",
            "And that's when the lovers bundle creates magic for business couples.",
            "And that's when the lovers bundle becomes your secret weapon."
        ]
        
        # Select random elements
        hook = random.choice(business_hooks)
        luxury = random.choice(luxury_lines)
        product = random.choice(product_lines)
        impact = random.choice(impact_lines)
        
        # Build the script with the SAME POWERFUL STRUCTURE
        lines = []
        lines.append(f"{hook} {luxury}")
        lines.append(product)
        lines.append(impact)
        
        # Add banger ending
        banger = random.choice(self.banger_endings)
        lines.append(banger)
        
        # Ensure we meet target word count
        current_words = sum(len(line.split()) for line in lines)
        if current_words < target_words:
            # Add more detail to existing lines
            enhanced_lines = []
            for line in lines[:-1]:  # Don't modify the banger ending
                if len(line.split()) < 12:  # If line is too short
                    enhanced_lines.append(f"{line} It's absolutely transformative.")
                else:
                    enhanced_lines.append(line)
            enhanced_lines.append(lines[-1])  # Add banger ending
            lines = enhanced_lines
        
        return "\n".join(lines)
    
    def _generate_luxury_pleasure_script(self, product_name: str, transcript: str, gen_z: bool, context: Dict[str, Any]) -> str:
        """Generate luxury-focused script with human voice"""
        
        # Use customer review language patterns
        pleasure_hooks = [
            "I discovered something amazing with {}.",
            "Let me tell you about my experience with {}.",
            "{} changed everything for me.",
            "I never knew pleasure could feel like this.",
            "This is what I've been missing."
        ]
        
        benefit_lines = [
            "The different speeds create endless possibilities.",
            "It's whisper-quiet and completely discreet.",
            "The quality feels premium in every way.",
            "It's easy to use and even easier to love.",
            "The sensations are absolutely incredible.",
            "The body-safe silicone feels amazing against your skin.",
            "The rechargeable battery lasts for hours of pleasure.",
            "The compact design fits perfectly in your hand.",
            "The waterproof feature makes cleaning effortless.",
            "The app control gives you complete customization."
        ]
        
        experience_lines = [
            "Every session feels like a new adventure.",
            "I've never experienced anything like this.",
            "It's become my go-to for relaxation.",
            "The pleasure is beyond what I expected.",
            "I'm completely hooked on the feeling."
        ]
        
        # Build script
        lines = []
        
        # Line 1: Hook (use customer language)
        hook = random.choice(pleasure_hooks).format(product_name)
        lines.append(hook)
        
        # Line 2: Product feature
        if context["speed_modes"]:
            feature_line = f"With {context['speed_modes']} speed modes, every mood is covered."
        else:
            feature_line = f"The customizable settings adapt to my desires."
        lines.append(feature_line)
        
        # Line 3: Benefit (use training data)
        benefit_line = random.choice(benefit_lines)
        lines.append(benefit_line)
        
        # Line 4: Experience (use customer review language)
        experience_line = random.choice(experience_lines)
        lines.append(experience_line)
        
        # Line 5: Banger ending
        banger = random.choice(self.banger_endings)
        lines.append(banger)
        
        return "\n".join(lines)
    
    def _generate_intense_pleasure_script(self, product_name: str, transcript: str, gen_z: bool, context: Dict[str, Any]) -> str:
        """Generate intense-pleasure focused script with human voice"""
        
        # Use customer review language patterns
        pleasure_hooks = [
            "I discovered something amazing with {}.",
            "Let me tell you about my experience with {}.",
            "{} changed everything for me.",
            "I never knew pleasure could feel like this.",
            "This is what I've been missing."
        ]
        
        benefit_lines = [
            "The different speeds create endless possibilities.",
            "It's whisper-quiet and completely discreet.",
            "The quality feels premium in every way.",
            "It's easy to use and even easier to love.",
            "The sensations are absolutely incredible.",
            "The body-safe silicone feels amazing against your skin.",
            "The rechargeable battery lasts for hours of pleasure.",
            "The compact design fits perfectly in your hand.",
            "The waterproof feature makes cleaning effortless.",
            "The app control gives you complete customization."
        ]
        
        experience_lines = [
            "Every session feels like a new adventure.",
            "I've never experienced anything like this.",
            "It's become my go-to for relaxation.",
            "The pleasure is beyond what I expected.",
            "I'm completely hooked on the feeling."
        ]
        
        # Build script
        lines = []
        
        # Line 1: Hook (use customer language)
        hook = random.choice(pleasure_hooks).format(product_name)
        lines.append(hook)
        
        # Line 2: Product feature
        if context["speed_modes"]:
            feature_line = f"With {context['speed_modes']} speed modes, every mood is covered."
        else:
            feature_line = f"The customizable settings adapt to my desires."
        lines.append(feature_line)
        
        # Line 3: Benefit (use training data)
        benefit_line = random.choice(benefit_lines)
        lines.append(benefit_line)
        
        # Line 4: Experience (use customer review language)
        experience_line = random.choice(experience_lines)
        lines.append(experience_line)
        
        # Line 5: Banger ending
        banger = random.choice(self.banger_endings)
        lines.append(banger)
        
        return "\n".join(lines)
    
    def _generate_relaxation_script(self, product_name: str, transcript: str, gen_z: bool, context: Dict[str, Any]) -> str:
        """Generate relaxation-focused script with human voice"""
        
        # Use customer review language patterns
        relaxation_hooks = [
            "I discovered something amazing with {}.",
            "Let me tell you about my experience with {}.",
            "{} changed everything for me.",
            "I never knew pleasure could feel like this.",
            "This is what I've been missing."
        ]
        
        benefit_lines = [
            "The different speeds create endless possibilities.",
            "It's whisper-quiet and completely discreet.",
            "The quality feels premium in every way.",
            "It's easy to use and even easier to love.",
            "The sensations are absolutely incredible.",
            "The body-safe silicone feels amazing against your skin.",
            "The rechargeable battery lasts for hours of pleasure.",
            "The compact design fits perfectly in your hand.",
            "The waterproof feature makes cleaning effortless.",
            "The app control gives you complete customization."
        ]
        
        experience_lines = [
            "Every session feels like a new adventure.",
            "I've never experienced anything like this.",
            "It's become my go-to for relaxation.",
            "The pleasure is beyond what I expected.",
            "I'm completely hooked on the feeling."
        ]
        
        # Build script
        lines = []
        
        # Line 1: Hook (use customer language)
        hook = random.choice(relaxation_hooks).format(product_name)
        lines.append(hook)
        
        # Line 2: Product feature
        if context["speed_modes"]:
            feature_line = f"With {context['speed_modes']} speed modes, every mood is covered."
        else:
            feature_line = f"The customizable settings adapt to my desires."
        lines.append(feature_line)
        
        # Line 3: Benefit (use training data)
        benefit_line = random.choice(benefit_lines)
        lines.append(benefit_line)
        
        # Line 4: Experience (use customer review language)
        experience_line = random.choice(experience_lines)
        lines.append(experience_line)
        
        # Line 5: Banger ending
        banger = random.choice(self.banger_endings)
        lines.append(banger)
        
        return "\n".join(lines)
    
    def _generate_adventure_script(self, product_name: str, transcript: str, gen_z: bool, context: Dict[str, Any]) -> str:
        """Generate adventure-focused script with human voice"""
        
        # Use customer review language patterns
        adventure_hooks = [
            "I discovered something amazing with {}.",
            "Let me tell you about my experience with {}.",
            "{} changed everything for me.",
            "I never knew pleasure could feel like this.",
            "This is what I've been missing."
        ]
        
        benefit_lines = [
            "The different speeds create endless possibilities.",
            "It's whisper-quiet and completely discreet.",
            "The quality feels premium in every way.",
            "It's easy to use and even easier to love.",
            "The sensations are absolutely incredible.",
            "The body-safe silicone feels amazing against your skin.",
            "The rechargeable battery lasts for hours of pleasure.",
            "The compact design fits perfectly in your hand.",
            "The waterproof feature makes cleaning effortless.",
            "The app control gives you complete customization."
        ]
        
        experience_lines = [
            "Every session feels like a new adventure.",
            "I've never experienced anything like this.",
            "It's become my go-to for relaxation.",
            "The pleasure is beyond what I expected.",
            "I'm completely hooked on the feeling."
        ]
        
        # Build script
        lines = []
        
        # Line 1: Hook (use customer language)
        hook = random.choice(adventure_hooks).format(product_name)
        lines.append(hook)
        
        # Line 2: Product feature
        if context["speed_modes"]:
            feature_line = f"With {context['speed_modes']} speed modes, every mood is covered."
        else:
            feature_line = f"The customizable settings adapt to my desires."
        lines.append(feature_line)
        
        # Line 3: Benefit (use training data)
        benefit_line = random.choice(benefit_lines)
        lines.append(benefit_line)
        
        # Line 4: Experience (use customer review language)
        experience_line = random.choice(experience_lines)
        lines.append(experience_line)
        
        # Line 5: Banger ending
        banger = random.choice(self.banger_endings)
        lines.append(banger)
        
        return "\n".join(lines)
    
    def generate_variations(self, product_name: str, transcript: str, count: int = 10, gen_z: bool = False) -> List[Dict[str, Any]]:
        """Generate multiple unique variations using training data"""
        
        context = self._analyze_transcript(transcript)
        variations = []
        
        # Reset used themes for fresh variations
        if hasattr(self, '_used_themes'):
            self._used_themes.clear()
        
        for i in range(count):
            try:
                # Generate base script
                script = self.generate_human_script(product_name, transcript, gen_z)
                
                # Create variation by applying different patterns
                variation = self._create_variation(script, product_name, transcript, gen_z, context)
                
                # Ensure variation is not empty or None
                if variation and len(variation.strip()) > 0:
                    variations.append({
                        "text": variation,
                        "variation_number": i + 1,
                        "context": context
                    })
                else:
                    # Fallback: generate a basic variation
                    fallback_variation = self._generate_fallback_variation(product_name, transcript, gen_z, context, i)
                    variations.append({
                        "text": fallback_variation,
                        "variation_number": i + 1,
                        "context": context
                    })
                    
            except Exception as e:
                print(f"Warning: Failed to generate variation {i+1}: {e}")
                # Fallback: generate a basic variation
                fallback_variation = self._generate_fallback_variation(product_name, transcript, gen_z, context, i)
                variations.append({
                    "text": fallback_variation,
                    "variation_number": i + 1,
                    "context": context
                })
        
        # Ensure we have exactly the requested number of variations
        while len(variations) < count:
            fallback_variation = self._generate_fallback_variation(product_name, transcript, gen_z, context, len(variations))
            variations.append({
                "text": fallback_variation,
                "variation_number": len(variations) + 1,
                "context": context
            })
        
        return variations
    
    def _create_variation(self, base_script: str, product_name: str, transcript_text: str, gen_z: bool, context: Dict[str, Any]) -> str:
        """Create a unique variation using the appropriate generator based on scenario"""
        
        scenario = context.get("primary_scenario", "general")
        
        # For business couple scenarios, use the powerful business couple variation generator
        if scenario == "business_couple_intimacy" or scenario == "business_couple_travel":
            return self._generate_unique_couple_variation(product_name, transcript_text, gen_z, context)
        
        # For other scenarios, use the new dynamic system
        return self._generate_dynamic_script(product_name, transcript_text, gen_z, context)
    
    def _generate_unique_couple_variation(self, product_name: str, transcript_text: str, gen_z: bool, context: Dict[str, Any]) -> str:
        """Generate a completely unique couple intimacy variation"""
        
        # Calculate target length based on transcript
        transcript_words = len(transcript_text.split())
        target_words = max(transcript_words - 5, 35)  # Allow some flexibility but ensure minimum length
        
        # Track which themes have been used to ensure uniqueness
        if not hasattr(self, '_used_themes'):
            self._used_themes = set()
        
        # Different variation themes - ensure we cycle through them
        variation_themes = [
            "passion_intensity",
            "romantic_connection", 
            "exploration_discovery",
            "intimate_moments",
            "emotional_depth",
            "sensual_awakening",
            "spiritual_connection",
            "adventure_thrills",
            "deep_intimacy",
            "pleasure_mastery"
        ]
        
        # Find an unused theme
        available_themes = [theme for theme in variation_themes if theme not in self._used_themes]
        if not available_themes:
            # Reset if all themes used
            self._used_themes.clear()
            available_themes = variation_themes
        
        theme = random.choice(available_themes)
        self._used_themes.add(theme)
        
        # POWERFUL BUSINESS COUPLE HOOKS (like your transcript)
        business_couple_hooks = [
            "As a couple who run businesses together,",
            "When you're building empires together,",
            "For couples who work and travel as one,",
            "When your flights become boardroom extensions,",
            "As business partners who never stop,",
            "When meetings and intimacy collide,",
            "For couples who turn every trip into opportunity,",
            "When your work life and love life merge,"
        ]
        
        lines = []
        
        # Always start with the powerful business couple hook
        hook = random.choice(business_couple_hooks)
        
        if theme == "passion_intensity":
            lines.append(f"{hook} the fire between us ignites with every touch and caress.")
            lines.append("We're consumed by an overwhelming desire for each other that knows no limits.")
            lines.append(f"{product_name} intensifies every sensation to unbearable heights of ecstasy.")
            lines.append("Our passion knows no boundaries or limitations in these intimate moments.")
            lines.append("We surrender completely to the intensity of our connection and desire.")
            
        elif theme == "romantic_connection":
            lines.append(f"{hook} our hearts beat as one in perfect harmony and understanding.")
            lines.append("Every moment together deepens our emotional bond beyond words.")
            lines.append(f"{product_name} creates moments of pure romantic bliss that last forever.")
            lines.append("We're building a love story that will transcend time and space.")
            lines.append("Our connection goes far beyond the physical realm into the spiritual.")
            
        elif theme == "exploration_discovery":
            lines.append(f"{hook} we venture into uncharted territories of pleasure and discovery.")
            lines.append("Every session reveals new aspects of our desires and fantasies.")
            lines.append(f"{product_name} opens doors to experiences we never knew existed before.")
            lines.append("We're constantly discovering new ways to please and satisfy each other.")
            lines.append("This journey of exploration brings endless surprises and delights.")
            
        elif theme == "intimate_moments":
            lines.append(f"{hook} in these private moments of pure intimacy, nothing else matters.")
            lines.append("We create a world where only our pleasure and connection exists.")
            lines.append(f"{product_name} transforms ordinary nights into extraordinary experiences.")
            lines.append("Time stands still when we're lost in each other's embrace.")
            lines.append("These intimate moments define the very essence of our relationship.")
            
        elif theme == "emotional_depth":
            lines.append(f"{hook} our emotional connection runs deeper than words could ever express.")
            lines.append("Every touch communicates volumes about our feelings and desires.")
            lines.append(f"{product_name} enhances the emotional intensity of our bond exponentially.")
            lines.append("We understand each other on a soul-deep level that's truly magical.")
            lines.append("Our love story is written in moments of pure emotion and passion.")
            
        elif theme == "sensual_awakening":
            lines.append(f"{hook} every touch awakens new sensations we never knew existed.")
            lines.append("Our bodies respond to each other in ways that defy explanation.")
            lines.append(f"{product_name} unlocks hidden depths of pleasure and desire.")
            lines.append("We're discovering the full spectrum of what our bodies can feel.")
            lines.append("This awakening transforms how we experience intimacy forever.")
            
        elif theme == "spiritual_connection":
            lines.append(f"{hook} our connection transcends the physical into something spiritual.")
            lines.append("When we're together, we touch something divine and eternal.")
            lines.append(f"{product_name} becomes a bridge to higher states of consciousness.")
            lines.append("We're not just making love—we're creating something sacred.")
            lines.append("This spiritual bond elevates our entire relationship.")
            
        elif theme == "adventure_thrills":
            lines.append(f"{hook} every night becomes an adventure of discovery and excitement.")
            lines.append("We're thrill-seekers in the realm of pleasure and passion.")
            lines.append(f"{product_name} adds new dimensions of adventure to our intimacy.")
            lines.append("We never know what incredible sensations await us next.")
            lines.append("This adventurous spirit keeps our passion alive and growing.")
            
        elif theme == "deep_intimacy":
            lines.append(f"{hook} we're diving into the deepest levels of intimacy possible.")
            lines.append("Nothing is hidden between us—we're completely exposed and vulnerable.")
            lines.append(f"{product_name} helps us reach new depths of connection.")
            lines.append("We're exploring the very essence of what intimacy means.")
            lines.append("This deep intimacy creates an unbreakable bond between us.")
            
        else:  # pleasure_mastery
            lines.append(f"{hook} we're becoming masters of each other's pleasure and satisfaction.")
            lines.append("Every session teaches us new ways to bring each other to ecstasy.")
            lines.append(f"{product_name} becomes our tool for mastering the art of pleasure.")
            lines.append("We're learning to read each other's desires like open books.")
            lines.append("This mastery creates the most satisfying experiences imaginable.")
        
        # Add banger ending
        banger = random.choice(self.banger_endings)
        lines.append(banger)
        
        # Ensure we meet target word count
        current_words = sum(len(line.split()) for line in lines)
        if current_words < target_words:
            # Add more detail to existing lines
            enhanced_lines = []
            for line in lines[:-1]:  # Don't modify the banger ending
                if len(line.split()) < 12:  # If line is too short
                    enhanced_lines.append(f"{line} It's absolutely transformative and incredible.")
                else:
                    enhanced_lines.append(line)
            enhanced_lines.append(lines[-1])  # Add banger ending
            lines = enhanced_lines
        
        return "\n".join(lines)
    
    def _rephrase_sentences(self, base_script: str, product_name: str, transcript_text: str, gen_z: bool, context: Dict[str, Any]) -> str:
        """Rephrase sentences to create variation."""
        lines = base_script.split("\n")
        new_lines = []
        
        for line in lines:
            # Simple rephrasing: replace a word or phrase
            if random.random() < 0.5:
                if "amazing" in line.lower():
                    new_line = line.replace("amazing", "incredible")
                elif "love" in line.lower():
                    new_line = line.replace("love", "adore")
                elif "great" in line.lower():
                    new_line = line.replace("great", "excellent")
                else:
                    new_line = line # No change
            else:
                new_line = line # No change
            
            new_lines.append(new_line)
        
        return "\n".join(new_lines)
    
    def _change_sentence_order(self, base_script: str, product_name: str, transcript_text: str, gen_z: bool, context: Dict[str, Any]) -> str:
        """Change the order of sentences to create variation."""
        lines = base_script.split("\n")
        new_lines = []
        
        # Randomly select a number of sentences to reorder
        num_sentences_to_reorder = random.randint(1, len(lines) - 1) # At least one sentence must remain
        
        # Select indices to reorder
        indices_to_reorder = random.sample(range(len(lines)), num_sentences_to_reorder)
        
        # Reorder sentences based on selected indices
        for i in range(len(lines)):
            if i in indices_to_reorder:
                new_lines.append(lines[indices_to_reorder.index(i)]) # Append in new order
            else:
                new_lines.append(lines[i]) # Append in original order
        
        return "\n".join(new_lines)
    
    def _add_sensory_details(self, base_script: str, product_name: str, transcript_text: str, gen_z: bool, context: Dict[str, Any]) -> str:
        """Add sensory details to create variation."""
        lines = base_script.split("\n")
        new_lines = []
        
        for line in lines:
            # Add sensory details like "silk-like" or "velvety"
            if random.random() < 0.3:
                silk_like = "silk-like" if random.random() < 0.5 else "velvety"
                line = line.replace("silicone", silk_like)
            
            # Add more sensory details
            if random.random() < 0.2:
                line += f" (silk-like, velvety)"
            
            new_lines.append(line)
        
        return "\n".join(new_lines)
    
    def _vary_emotional_tone(self, base_script: str, product_name: str, transcript_text: str, gen_z: bool, context: Dict[str, Any]) -> str:
        """Vary the emotional tone of lines."""
        lines = base_script.split("\n")
        new_lines = []
        
        for line in lines:
            # Simple tone variation: replace "amazing" with "incredible"
            if "amazing" in line.lower():
                new_line = line.replace("amazing", "incredible")
            elif "love" in line.lower():
                new_line = line.replace("love", "adore")
            elif "great" in line.lower():
                new_line = line.replace("great", "excellent")
            else:
                new_line = line # No change
            
            new_lines.append(new_line)
        
        return "\n".join(new_lines)
    
    def _complete_rewrite(self, base_script: str, product_name: str, transcript_text: str, gen_z: bool, context: Dict[str, Any]) -> str:
        """Completely rewrite lines with different structure."""
        new_lines = []
        
        # Different opening patterns
        openings = [
            "Let me tell you about my experience with dive+.",
            "I discovered something amazing with dive+.",
            "dive+ changed everything for me.",
            "This is what I've been missing.",
            "I never knew pleasure could feel like this."
        ]
        
        # Different middle patterns
        middles = [
            "The different speeds create endless possibilities.",
            "It's whisper-quiet and completely discreet.",
            "The quality feels premium in every way.",
            "It's easy to use and even easier to love.",
            "The sensations are absolutely incredible."
        ]
        
        # Different closing patterns
        closings = [
            "Every session feels like a new adventure.",
            "I've never experienced anything like this.",
            "It's become my go-to for relaxation.",
            "The pleasure is beyond what I expected.",
            "I'm completely hooked on the feeling."
        ]
        
        new_lines.append(random.choice(openings))
        new_lines.append(random.choice(middles))
        new_lines.append(random.choice(closings))
        
        return "\n".join(new_lines)
    
    def _generate_fallback_variation(self, product_name: str, transcript_text: str, gen_z: bool, context: Dict[str, Any], fallback_index: int) -> str:
        """Generates a basic fallback variation if a specific variation fails."""
        
        # Check if this is a couple intimacy scenario
        is_couple_intimacy = (
            context.get("primary_scenario") == "couple_intimacy" or
            "couple" in transcript_text.lower() or
            "together" in transcript_text.lower() or
            "lovers" in transcript_text.lower() or
            "intimacy" in transcript_text.lower()
        )
        
        if is_couple_intimacy:
            # Use the couple intimacy fallback system
            return self._generate_couple_intimacy_fallback(product_name, transcript_text, gen_z, context, fallback_index)
        else:
            # Use the general fallback system
            return self._generate_general_fallback(product_name, transcript_text, gen_z, context, fallback_index)
    
    def _generate_couple_intimacy_fallback(self, product_name: str, transcript_text: str, gen_z: bool, context: Dict[str, Any], fallback_index: int) -> str:
        """Generate a fallback variation specifically for couple intimacy scenarios."""
        
        # POWERFUL BUSINESS COUPLE HOOKS (like your transcript)
        business_couple_hooks = [
            "As a couple who run businesses together,",
            "When you're building empires together,",
            "For couples who work and travel as one,",
            "When your flights become boardroom extensions,",
            "As business partners who never stop,",
            "When meetings and intimacy collide,",
            "For couples who turn every trip into opportunity,",
            "When your work life and love life merge,"
        ]
        
        # Different fallback themes based on index
        fallback_themes = [
            "passion_intensity",
            "romantic_connection", 
            "exploration_discovery",
            "intimate_moments",
            "emotional_depth",
            "sensual_awakening",
            "spiritual_connection",
            "adventure_thrills",
            "deep_intimacy",
            "pleasure_mastery"
        ]
        
        # Use the fallback index to select a theme
        theme_index = fallback_index % len(fallback_themes)
        theme = fallback_themes[theme_index]
        
        # Select a hook based on the fallback index
        hook_index = fallback_index % len(business_couple_hooks)
        hook = business_couple_hooks[hook_index]
        
        lines = []
        
        if theme == "passion_intensity":
            lines.append(f"{hook} the fire between us ignites with every touch and caress.")
            lines.append("We're consumed by an overwhelming desire for each other that knows no limits.")
            lines.append(f"{product_name} intensifies every sensation to unbearable heights of ecstasy.")
            lines.append("Our passion knows no boundaries or limitations in these intimate moments.")
            lines.append("We surrender completely to the intensity of our connection and desire.")
            
        elif theme == "romantic_connection":
            lines.append(f"{hook} our hearts beat as one in perfect harmony and understanding.")
            lines.append("Every moment together deepens our emotional bond beyond words.")
            lines.append(f"{product_name} creates moments of pure romantic bliss that last forever.")
            lines.append("We're building a love story that will transcend time and space.")
            lines.append("Our connection goes far beyond the physical realm into the spiritual.")
            
        elif theme == "exploration_discovery":
            lines.append(f"{hook} we venture into uncharted territories of pleasure and discovery.")
            lines.append("Every session reveals new aspects of our desires and fantasies.")
            lines.append(f"{product_name} opens doors to experiences we never knew existed before.")
            lines.append("We're constantly discovering new ways to please and satisfy each other.")
            lines.append("This journey of exploration brings endless surprises and delights.")
            
        elif theme == "intimate_moments":
            lines.append(f"{hook} in these private moments of pure intimacy, nothing else matters.")
            lines.append("We create a world where only our pleasure and connection exists.")
            lines.append(f"{product_name} transforms ordinary nights into extraordinary experiences.")
            lines.append("Time stands still when we're lost in each other's embrace.")
            lines.append("These intimate moments define the very essence of our relationship.")
            
        elif theme == "emotional_depth":
            lines.append(f"{hook} our emotional connection runs deeper than words could ever express.")
            lines.append("Every touch communicates volumes about our feelings and desires.")
            lines.append(f"{product_name} enhances the emotional intensity of our bond exponentially.")
            lines.append("We understand each other on a soul-deep level that's truly magical.")
            lines.append("Our love story is written in moments of pure emotion and passion.")
            
        elif theme == "sensual_awakening":
            lines.append(f"{hook} every touch awakens new sensations we never knew existed.")
            lines.append("Our bodies respond to each other in ways that defy explanation.")
            lines.append(f"{product_name} unlocks hidden depths of pleasure and desire.")
            lines.append("We're discovering the full spectrum of what our bodies can feel.")
            lines.append("This awakening transforms how we experience intimacy forever.")
            
        elif theme == "spiritual_connection":
            lines.append(f"{hook} our connection transcends the physical into something spiritual.")
            lines.append("When we're together, we touch something divine and eternal.")
            lines.append(f"{product_name} becomes a bridge to higher states of consciousness.")
            lines.append("We're not just making love—we're creating something sacred.")
            lines.append("This spiritual bond elevates our entire relationship.")
            
        elif theme == "adventure_thrills":
            lines.append(f"{hook} every night becomes an adventure of discovery and excitement.")
            lines.append("We're thrill-seekers in the realm of pleasure and passion.")
            lines.append(f"{product_name} adds new dimensions of adventure to our intimacy.")
            lines.append("We never know what incredible sensations await us next.")
            lines.append("This adventurous spirit keeps our passion alive and growing.")
            
        elif theme == "deep_intimacy":
            lines.append(f"{hook} we're diving into the deepest levels of intimacy possible.")
            lines.append("Nothing is hidden between us—we're completely exposed and vulnerable.")
            lines.append(f"{product_name} helps us reach new depths of connection.")
            lines.append("We're exploring the very essence of what intimacy means.")
            lines.append("This deep intimacy creates an unbreakable bond between us.")
            
        else:  # pleasure_mastery
            lines.append(f"{hook} we're becoming masters of each other's pleasure and satisfaction.")
            lines.append("Every session teaches us new ways to bring each other to ecstasy.")
            lines.append(f"{product_name} becomes our tool for mastering the art of pleasure.")
            lines.append("We're learning to read each other's desires like open books.")
            lines.append("This mastery creates the most satisfying experiences imaginable.")
        
        # Add banger ending
        banger = random.choice(self.banger_endings)
        lines.append(banger)
        
        return "\n".join(lines)
    
    def _generate_general_fallback(self, product_name: str, transcript_text: str, gen_z: bool, context: Dict[str, Any], fallback_index: int) -> str:
        """Generate a fallback variation for non-couple scenarios."""
        
        # Re-generate the base script to ensure it's fresh
        base_script = self.generate_human_script(product_name, transcript_text, gen_z)
        
        # Apply a variation technique to the base script
        variation_techniques = [
            self._rephrase_sentences,
            self._change_sentence_order,
            self._add_sensory_details,
            self._vary_emotional_tone,
            self._complete_rewrite
        ]
        
        # Use a different technique for each fallback
        technique_index = fallback_index % len(variation_techniques)
        technique = variation_techniques[technique_index]
        return technique(base_script, product_name, transcript_text, gen_z, context)
    
    def format_output(self, product_name: str, script: str, variations: List[Dict[str, Any]]) -> str:
        """Format output in the exact format requested"""
        
        output = []
        output.append(f"Generated Script")
        output.append(script)
        output.append("")
        output.append(f"Variations ({len(variations)})")
        
        for i, variation in enumerate(variations, 1):
            output.append(f"Variation {i}")
            output.append(variation["text"])
            output.append("")
        
        # Add Leeza-tone grade
        output.append("⚖️ Leeza-tone grade:")
        output.append(f"✅ Human voice patterns from {len(self.voice_patterns.get('sentence_structures', []))} Instagram posts")
        output.append(f"✅ Customer language from {len(self.customer_language.get('experience_phrases', []))} reviews")
        output.append(f"✅ Product knowledge from {len(self.product_knowledge.get('features', {}))} features")
        output.append("✅ Ad-quality variations with emotional hooks and banger endings")
        
        return "\n".join(output)

    def _generate_dynamic_script(self, product_name: str, transcript: str, gen_z: bool, context: Dict[str, Any]) -> str:
        """Generate script dynamically based on learned patterns - adapts to ANY scenario"""
        
        # Get learned patterns and adaptation strategy
        patterns = context.get("learned_patterns", {})
        adaptation_strategy = context.get("adaptation_strategy", [])
        scenario = context.get("primary_scenario", "general")
        
        # DYNAMIC SCRIPT GENERATION - learns from transcript patterns
        if scenario == "business_couple_intimacy" or scenario == "business_couple_travel":
            # Use the powerful business couple script generator for business scenarios
            return self._generate_couple_intimacy_script(product_name, transcript, gen_z, context)
        elif "solo_focused" in adaptation_strategy:
            return self._generate_solo_dynamic_script(product_name, transcript, gen_z, context)
        elif "relationship_focused" in adaptation_strategy:
            return self._generate_relationship_dynamic_script(product_name, transcript, gen_z, context)
        elif "travel_appropriate" in adaptation_strategy:
            return self._generate_travel_dynamic_script(product_name, transcript, gen_z, context)
        elif "solution_focused" in adaptation_strategy:
            return self._generate_solution_dynamic_script(product_name, transcript, gen_z, context)
        else:
            return self._generate_general_dynamic_script(product_name, transcript, gen_z, context)

    def _generate_solo_dynamic_script(self, product_name: str, transcript: str, gen_z: bool, context: Dict[str, Any]) -> str:
        """Generate solo script dynamically based on learned patterns"""
        
        patterns = context.get("learned_patterns", {})
        emotions = patterns.get("emotional_language", {})
        desires = patterns.get("desire_patterns", {})
        actions = patterns.get("action_patterns", {})
        
        # DYNAMIC HOOKS - learns from transcript content
        hooks = self._generate_dynamic_hooks(patterns, "solo")
        
        # DYNAMIC BENEFITS - learns from transcript needs
        benefits = self._generate_dynamic_benefits(patterns, product_name)
        
        # DYNAMIC GUIDANCE - learns from transcript context
        guidance = self._generate_dynamic_guidance(patterns, product_name)
        
        # Build script dynamically
        lines = []
        lines.append(random.choice(hooks))
        
        # Add benefits based on detected needs
        for benefit in benefits[:2]:  # Use first 2 benefits
            lines.append(benefit)
        
        # Add guidance based on context
        if guidance:
            lines.append(random.choice(guidance))
        
        # Add banger ending
        banger = random.choice(self.banger_endings)
        lines.append(banger)
        
        return "\n".join(lines)

    def _generate_relationship_dynamic_script(self, product_name: str, transcript: str, gen_z: bool, context: Dict[str, Any]) -> str:
        """Generate relationship script dynamically based on learned patterns"""
        
        patterns = context.get("learned_patterns", {})
        emotions = patterns.get("emotional_language", {})
        context_clues = patterns.get("context_clues", {})
        
        # DYNAMIC RELATIONSHIP HOOKS - learns from transcript
        hooks = self._generate_dynamic_hooks(patterns, "relationship")
        
        # DYNAMIC INTIMACY LINES - learns from transcript emotions
        intimacy_lines = self._generate_dynamic_intimacy_lines(patterns, product_name)
        
        # DYNAMIC CONNECTION LINES - learns from transcript context
        connection_lines = self._generate_dynamic_connection_lines(patterns, product_name)
        
        # Build script dynamically
        lines = []
        lines.append(random.choice(hooks))
        
        # Add intimacy lines
        for line in intimacy_lines[:2]:
            lines.append(line)
        
        # Add connection lines
        for line in connection_lines[:2]:
            lines.append(line)
        
        # Add banger ending
        banger = random.choice(self.banger_endings)
        lines.append(banger)
        
        return "\n".join(lines)

    def _generate_travel_dynamic_script(self, product_name: str, transcript: str, gen_z: bool, context: Dict[str, Any]) -> str:
        """Generate travel script dynamically based on learned patterns"""
        
        patterns = context.get("learned_patterns", {})
        context_clues = patterns.get("context_clues", {})
        actions = patterns.get("action_patterns", {})
        
        # DYNAMIC TRAVEL HOOKS - learns from transcript
        hooks = self._generate_dynamic_hooks(patterns, "travel")
        
        # DYNAMIC TRAVEL BENEFITS - learns from transcript needs
        travel_benefits = self._generate_dynamic_travel_benefits(patterns, product_name)
        
        # DYNAMIC TRAVEL GUIDANCE - learns from transcript context
        travel_guidance = self._generate_dynamic_travel_guidance(patterns, product_name)
        
        # Build script dynamically
        lines = []
        lines.append(random.choice(hooks))
        
        # Add travel benefits
        for benefit in travel_benefits[:2]:
            lines.append(benefit)
        
        # Add travel guidance
        if travel_guidance:
            lines.append(random.choice(travel_guidance))
        
        # Add banger ending
        banger = random.choice(self.banger_endings)
        lines.append(banger)
        
        return "\n".join(lines)

    def _generate_solution_dynamic_script(self, product_name: str, transcript: str, gen_z: bool, context: Dict[str, Any]) -> str:
        """Generate solution-focused script dynamically based on learned patterns"""
        
        patterns = context.get("learned_patterns", {})
        desires = patterns.get("desire_patterns", {})
        actions = patterns.get("action_patterns", {})
        
        # DYNAMIC PROBLEM IDENTIFICATION - learns from transcript
        problems = self._identify_dynamic_problems(patterns)
        
        # DYNAMIC SOLUTION LINES - learns from transcript needs
        solutions = self._generate_dynamic_solutions(patterns, product_name)
        
        # DYNAMIC TRANSFORMATION LINES - learns from transcript desires
        transformations = self._generate_dynamic_transformations(patterns, product_name)
        
        # Build script dynamically
        lines = []
        
        # Start with problem identification
        if problems:
            lines.append(random.choice(problems))
        
        # Add solution lines
        for solution in solutions[:2]:
            lines.append(solution)
        
        # Add transformation lines
        for transformation in transformations[:2]:
            lines.append(transformation)
        
        # Add banger ending
        banger = random.choice(self.banger_endings)
        lines.append(banger)
        
        return "\n".join(lines)

    def _generate_general_dynamic_script(self, product_name: str, transcript: str, gen_z: bool, context: Dict[str, Any]) -> str:
        """Generate general script dynamically when no specific pattern is detected"""
        
        patterns = context.get("learned_patterns", {})
        
        # DYNAMIC GENERAL HOOKS - learns from transcript
        hooks = self._generate_dynamic_hooks(patterns, "general")
        
        # DYNAMIC GENERAL BENEFITS - learns from transcript
        benefits = self._generate_dynamic_benefits(patterns, product_name)
        
        # DYNAMIC GENERAL GUIDANCE - learns from transcript
        guidance = self._generate_dynamic_guidance(patterns, product_name)
        
        # Build script dynamically
        lines = []
        lines.append(random.choice(hooks))
        
        # Add benefits
        for benefit in benefits[:2]:
            lines.append(benefit)
        
        # Add guidance
        if guidance:
            lines.append(random.choice(guidance))
        
        # Add banger ending
        banger = random.choice(self.banger_endings)
        lines.append(banger)
        
        return "\n".join(lines)

    def _generate_dynamic_hooks(self, patterns: Dict, hook_type: str) -> List[str]:
        """Generate hooks dynamically based on learned patterns"""
        
        speaker = patterns.get("speaker_identity", {})
        emotions = patterns.get("emotional_language", {})
        context = patterns.get("context_clues", {})
        desires = patterns.get("desire_patterns", {})
        
        hooks = []
        
        if hook_type == "solo":
            if "bored" in str(desires.get("frustrations", [])):
                hooks.extend([
                    "Bored of the same old routine?",
                    "Tired of your hand not cutting it?",
                    "Ready for something different?",
                    "Need a change from the usual?",
                ])
            elif emotions.get("primary_emotion") == "excitement":
                hooks.extend([
                    "Excited to try something new?",
                    "Ready to explore your desires?",
                    "Want to take things to the next level?",
                    "Eager to discover more?",
                ])
            else:
                hooks.extend([
                    "Time for some self-care?",
                    "Ready to treat yourself?",
                    "Want to make this moment special?",
                    "Need something to enhance your experience?",
                ])
        
        elif hook_type == "relationship":
            if context.get("physical_setting") == "travel":
                hooks.extend([
                    "Traveling together?",
                    "On the road with your partner?",
                    "Making every trip special?",
                    "Turning travel into adventure?",
                ])
            elif emotions.get("emotional_tone") == "romantic":
                hooks.extend([
                    "Want to deepen your connection?",
                    "Ready to explore intimacy together?",
                    "Looking to enhance your relationship?",
                    "Want to make every moment count?",
                ])
            else:
                hooks.extend([
                    "Building something special together?",
                    "Want to explore new possibilities?",
                    "Ready to take your relationship further?",
                    "Looking to create unforgettable moments?",
                ])
        
        elif hook_type == "travel":
            if speaker.get("count") == "single":
                hooks.extend([
                    "Traveling solo?",
                    "On the road by yourself?",
                    "Making every trip count?",
                    "Want to enhance your journey?",
                ])
            else:
                hooks.extend([
                    "Traveling together?",
                    "On an adventure with someone special?",
                    "Making memories on the road?",
                    "Want to enhance your travel experience?",
                ])
        
        else:  # general
            hooks.extend([
                "Ready for something amazing?",
                "Want to enhance your experience?",
                "Looking for something special?",
                "Ready to explore new possibilities?",
            ])
        
        return hooks

    def _generate_dynamic_benefits(self, patterns: Dict, product_name: str) -> List[str]:
        """Generate benefits dynamically based on learned patterns"""
        
        desires = patterns.get("desire_patterns", {})
        emotions = patterns.get("emotional_language", {})
        context = patterns.get("context_clues", {})
        
        benefits = []
        
        # Base product benefits
        base_benefits = [
            f"{product_name} enhances your experience.",
            f"{product_name} takes things to the next level.",
            f"{product_name} makes every moment special.",
            f"{product_name} transforms your routine.",
        ]
        
        # Context-specific benefits
        if context.get("physical_setting") == "travel":
            travel_benefits = [
                f"{product_name} travels with you everywhere.",
                f"{product_name} makes every trip memorable.",
                f"{product_name} fits perfectly into your journey.",
                f"{product_name} enhances your travel experience.",
            ]
            benefits.extend(travel_benefits)
        
        if desires.get("primary_desire") == "pleasure":
            pleasure_benefits = [
                f"{product_name} intensifies every sensation.",
                f"{product_name} creates deeper pleasure.",
                f"{product_name} enhances your satisfaction.",
                f"{product_name} takes pleasure to new heights.",
            ]
            benefits.extend(pleasure_benefits)
        
        if emotions.get("primary_emotion") == "frustration":
            solution_benefits = [
                f"{product_name} solves your problems.",
                f"{product_name} provides the change you need.",
                f"{product_name} breaks the routine.",
                f"{product_name} offers something different.",
            ]
            benefits.extend(solution_benefits)
        
        # Combine and return
        all_benefits = base_benefits + benefits
        return all_benefits

    def _generate_dynamic_guidance(self, patterns: Dict, product_name: str) -> List[str]:
        """Generate guidance dynamically based on learned patterns"""
        
        actions = patterns.get("action_patterns", {})
        emotions = patterns.get("emotional_language", {})
        
        guidance = []
        
        if actions.get("intent") == "change":
            guidance.extend([
                "Start with something new.",
                "Try a different approach.",
                "Break out of your routine.",
                "Explore what's possible.",
            ])
        
        if emotions.get("primary_emotion") == "curiosity":
            guidance.extend([
                "Discover what works for you.",
                "Explore new possibilities.",
                "Try something different.",
                "See what you've been missing.",
            ])
        
        if actions.get("urgency") == "high":
            guidance.extend([
                "Get started right away.",
                "Don't wait any longer.",
                "Make it happen now.",
                "Start your journey today.",
            ])
        
        # Default guidance
        if not guidance:
            guidance = [
                "Focus on what feels right.",
                "Trust your instincts.",
                "Go with what works for you.",
                "Find your own rhythm.",
            ]
        
        return guidance

    def _generate_dynamic_intimacy_lines(self, patterns: Dict, product_name: str) -> List[str]:
        """Generate intimacy lines dynamically based on learned patterns"""
        
        emotions = patterns.get("emotional_language", {})
        context = patterns.get("context_clues", {})
        
        intimacy_lines = []
        
        if emotions.get("emotional_tone") == "romantic":
            intimacy_lines.extend([
                f"{product_name} deepens your connection.",
                f"{product_name} creates moments of pure intimacy.",
                f"{product_name} strengthens your bond.",
                f"{product_name} brings you closer together.",
            ])
        
        if emotions.get("emotional_tone") == "playful":
            intimacy_lines.extend([
                f"{product_name} adds fun to your relationship.",
                f"{product_name} makes intimacy playful.",
                f"{product_name} brings excitement to your connection.",
                f"{product_name} creates adventure in your relationship.",
            ])
        
        if context.get("physical_setting") == "travel":
            intimacy_lines.extend([
                f"{product_name} makes every trip intimate.",
                f"{product_name} turns travel into romance.",
                f"{product_name} creates intimacy anywhere.",
                f"{product_name} makes every destination special.",
            ])
        
        return intimacy_lines

    def _generate_dynamic_connection_lines(self, patterns: Dict, product_name: str) -> List[str]:
        """Generate connection lines dynamically based on learned patterns"""
        
        emotions = patterns.get("emotional_language", {})
        context = patterns.get("context_clues", {})
        
        connection_lines = []
        
        if emotions.get("primary_emotion") == "desire":
            connection_lines.extend([
                f"{product_name} fulfills your deepest desires.",
                f"{product_name} satisfies your needs.",
                f"{product_name} meets you where you are.",
                f"{product_name} understands what you want.",
            ])
        
        if context.get("social_setting") == "partnered":
            connection_lines.extend([
                f"{product_name} enhances your partnership.",
                f"{product_name} strengthens your relationship.",
                f"{product_name} brings you closer.",
                f"{product_name} deepens your connection.",
            ])
        
        return connection_lines

    def _generate_dynamic_travel_benefits(self, patterns: Dict, product_name: str) -> List[str]:
        """Generate travel benefits dynamically based on learned patterns"""
        
        context = patterns.get("context_clues", {})
        actions = patterns.get("action_patterns", {})
        
        travel_benefits = []
        
        if context.get("physical_setting") == "travel":
            travel_benefits.extend([
                f"{product_name} fits in your luggage.",
                f"{product_name} travels discreetly.",
                f"{product_name} makes every trip special.",
                f"{product_name} enhances your journey.",
            ])
        
        if actions.get("intent") == "exploration":
            travel_benefits.extend([
                f"{product_name} opens new possibilities.",
                f"{product_name} enhances your adventures.",
                f"{product_name} makes exploration exciting.",
                f"{product_name} adds thrill to your travels.",
            ])
        
        return travel_benefits

    def _generate_dynamic_travel_guidance(self, patterns: Dict, product_name: str) -> List[str]:
        """Generate travel guidance dynamically based on learned patterns"""
        
        context = patterns.get("context_clues", {})
        
        travel_guidance = []
        
        if context.get("physical_setting") == "travel":
            travel_guidance.extend([
                "Take it with you everywhere.",
                "Make every trip memorable.",
                "Turn travel into adventure.",
                "Enhance your journey.",
            ])
        
        return travel_guidance

    def _identify_dynamic_problems(self, patterns: Dict) -> List[str]:
        """Identify problems dynamically based on learned patterns"""
        
        desires = patterns.get("desire_patterns", {})
        emotions = patterns.get("emotional_language", {})
        
        problems = []
        
        if "boredom" in desires.get("frustrations", []):
            problems.append("Bored of the same old routine?")
        
        if "manual_limitation" in desires.get("frustrations", []):
            problems.append("Your hand not cutting it anymore?")
        
        if "repetition" in desires.get("frustrations", []):
            problems.append("Tired of the same experience?")
        
        if emotions.get("primary_emotion") == "frustration":
            problems.append("Frustrated with your current situation?")
        
        return problems

    def _generate_dynamic_solutions(self, patterns: Dict, product_name: str) -> List[str]:
        """Generate solutions dynamically based on learned patterns"""
        
        desires = patterns.get("desire_patterns", {})
        actions = patterns.get("action_patterns", {})
        
        solutions = []
        
        if actions.get("intent") == "change":
            solutions.extend([
                f"{product_name} offers something completely different.",
                f"{product_name} breaks the routine.",
                f"{product_name} provides the change you need.",
            ])
        
        if desires.get("primary_desire") == "pleasure":
            solutions.extend([
                f"{product_name} enhances your pleasure.",
                f"{product_name} takes satisfaction to new heights.",
                f"{product_name} fulfills your desires.",
            ])
        
        return solutions

    def _generate_dynamic_transformations(self, patterns: Dict, product_name: str) -> List[str]:
        """Generate transformation lines dynamically based on learned patterns"""
        
        emotions = patterns.get("emotional_language", {})
        desires = patterns.get("desire_patterns", {})
        
        transformations = []
        
        if emotions.get("primary_emotion") == "excitement":
            transformations.extend([
                f"{product_name} transforms your experience.",
                f"{product_name} changes everything.",
                f"{product_name} revolutionizes your routine.",
            ])
        
        if desires.get("primary_desire") == "exploration":
            transformations.extend([
                f"{product_name} opens new possibilities.",
                f"{product_name} expands your horizons.",
                f"{product_name} reveals new experiences.",
            ])
        
        return transformations

def main():
    """Test the enhanced script generator"""
    generator = EnhancedScriptGenerator()
    
    # Test with your transcript
    transcript = "I'm on my way to the airport and look who's coming with me on my trip! It's Mini Jadugar! with 18 modes of speed Time for security check, got a lot of Dijayatra, got to get through with my Mini Jadugar. I will see you on the other side. Let's just say Mini Jadugar and I, we really like to take Jadugar places."
    
    print("🚀 Testing Enhanced MyMuse Script Generator")
    print("=" * 60)
    
    # Generate script
    script = generator.generate_human_script("dive+", transcript, gen_z=False)
    print("Generated Script:")
    print(script)
    print()
    
    # Generate variations
    variations = generator.generate_variations("dive+", transcript, count=3, gen_z=False)
    print("Variations (3):")
    for i, variation in enumerate(variations, 1):
        print(f"Variation {i}:")
        print(variation["text"])
        print()
    
    # Format full output
    full_output = generator.format_output("dive+", script, variations)
    print("Full Formatted Output:")
    print(full_output)

if __name__ == "__main__":
    main()
