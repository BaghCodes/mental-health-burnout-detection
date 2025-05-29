# ===================================================================
# MENTAL HEALTH BURNOUT DETECTION SYSTEM - AI TIPS SERVICE (UPDATED)
# ===================================================================
# Modern FastAPI service using Pydantic V2 and lifespan event handlers
# Generates personalized wellness recommendations using OpenAI GPT-4 API
# ===================================================================
from dotenv import load_dotenv
load_dotenv()
import os
print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager
import openai
import logging
import time
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ===================================================================
# GLOBAL VARIABLES AND CONFIGURATION
# ===================================================================

# Service startup time for uptime tracking
SERVICE_START_TIME = time.time()

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USE_OPENAI = bool(OPENAI_API_KEY)

# Cache for tips to reduce API calls
TIPS_CACHE: Dict[str, Dict[str, Any]] = {}
CACHE_DURATION = 300  # 5 minutes

# ===================================================================
# PYDANTIC V2 DATA MODELS
# ===================================================================

class UserData(BaseModel):
    """
    Pydantic V2 model for user's daily health and work data
    Uses modern field_validator instead of deprecated @validator
    """
    # Required fields from burnout risk assessment
    sleep: float = Field(..., ge=0, le=24, description="Sleep hours (0-24)")
    work: float = Field(..., ge=0, le=24, description="Work hours (0-24)")
    screen: float = Field(..., ge=0, le=24, description="Screen time hours (0-24)")
    
    # Risk assessment results from ML service
    score: float = Field(..., ge=0, le=1, description="Burnout risk score (0-1)")
    category: str = Field(..., description="Risk category (Low/Moderate/High)")
    
    # Optional physiological data
    heartRate: Optional[int] = Field(None, ge=40, le=200, description="Average heart rate")
    steps: Optional[int] = Field(None, ge=0, description="Steps taken")
    
    # Optional metadata
    timestamp: Optional[str] = Field(None, description="ISO timestamp")
    urgency: Optional[str] = Field(None, description="Urgency level")
    
    @field_validator('category')
    @classmethod
    def validate_category(cls, v: str, info: ValidationInfo) -> str:
        """Pydantic V2 field validator for risk category validation"""
        allowed_categories = ['Low', 'Moderate', 'High', 'Low-Moderate']
        if v not in allowed_categories:
            raise ValueError(f'Category must be one of: {allowed_categories}')
        return v

class TipsResponse(BaseModel):
    """Response model for AI-generated wellness tips"""
    tips: List[str] = Field(..., description="List of personalized wellness recommendations")
    generated_at: str = Field(..., description="Timestamp when tips were generated")
    model_used: str = Field(..., description="AI model used for generation")
    risk_level: str = Field(..., description="Risk level these tips address")
    confidence: Optional[float] = Field(None, description="Confidence score for recommendations")

class HealthStatus(BaseModel):
    """Model for service health check response"""
    status: str
    service: str
    version: str
    openai_available: bool
    uptime_seconds: float
    timestamp: str

# ===================================================================
# LIFESPAN EVENT HANDLER (MODERN FASTAPI PATTERN)
# ===================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Modern FastAPI lifespan event handler replacing deprecated @app.on_event
    Handles both startup and shutdown events in a single context manager
    """
    # Startup logic
    logger.info("=" * 60)
    logger.info("🤖 MENTAL HEALTH BURNOUT DETECTION - AI TIPS SERVICE")
    logger.info("=" * 60)
    logger.info("🚀 Service starting up...")
    logger.info(f"📊 OpenAI API available: {USE_OPENAI}")
    if USE_OPENAI:
        logger.info("✅ OpenAI API key found - using GPT-4 for tips")
        # Initialize OpenAI client
        openai.api_key = OPENAI_API_KEY
    else:
        logger.warning("⚠️ OPENAI_API_KEY not found. AI tips will use fallback responses.")
    logger.info(f"⏰ Started at: {datetime.now().isoformat()}")
    logger.info("=" * 60)
    
    # Yield control to the application
    yield
    
    # Shutdown logic
    logger.info("👋 AI Tips Service shutting down...")
    logger.info(f"📊 Cache entries at shutdown: {len(TIPS_CACHE)}")
    logger.info("✅ Shutdown complete")

# ===================================================================
# FASTAPI APPLICATION SETUP
# ===================================================================

# Create FastAPI app with modern lifespan handler
app = FastAPI(
    title="Mental Health Burnout Detection - AI Tips Service",
    description="AI-powered wellness recommendations using OpenAI GPT-4",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan  # Modern lifespan handler
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",     # Backend service
        "http://127.0.0.1:3000",     # Alternative localhost
        "http://localhost:8080",     # Frontend development server
        "http://localhost:5000",     # Alternative frontend port
        "file://",                   # For file:// protocol
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# ===================================================================
# HELPER FUNCTIONS
# ===================================================================

def generate_cache_key(user_data: UserData) -> str:
    """Generate cache key to avoid duplicate API calls"""
    key_data = {
        'sleep': round(user_data.sleep, 1),
        'work': round(user_data.work, 1),
        'screen': round(user_data.screen, 1),
        'category': user_data.category
    }
    return json.dumps(key_data, sort_keys=True)

def is_cache_valid(cache_entry: Dict[str, Any]) -> bool:
    """Check if cache entry is still valid"""
    cache_time = cache_entry.get('timestamp', 0)
    return (time.time() - cache_time) < CACHE_DURATION

def build_openai_prompt(user_data: UserData) -> str:
    """Build comprehensive prompt for OpenAI GPT-4"""
    sleep_status = "insufficient" if user_data.sleep < 7 else "adequate"
    work_status = "excessive" if user_data.work > 8 else "normal"
    screen_status = "high" if user_data.screen > 6 else "moderate"
    
    prompt = f"""You are a mental health and wellness expert AI assistant. Based on the following user data, provide 3 specific, actionable wellness recommendations to help prevent burnout.

USER DATA:
- Sleep: {user_data.sleep} hours ({sleep_status})
- Work: {user_data.work} hours ({work_status})
- Screen time: {user_data.screen} hours ({screen_status})
- Burnout risk score: {user_data.score}/1.0 ({user_data.category} risk)"""

    if user_data.heartRate:
        hr_status = "elevated" if user_data.heartRate > 80 else "normal"
        prompt += f"\n- Heart rate: {user_data.heartRate} bpm ({hr_status})"
    
    if user_data.steps:
        activity_status = "low" if user_data.steps < 5000 else "good"
        prompt += f"\n- Daily steps: {user_data.steps} ({activity_status} activity level)"

    if user_data.category == "High":
        prompt += """

URGENCY: This user has HIGH burnout risk. Focus on immediate, practical interventions.

Please provide 3 specific recommendations that:
1. Address the most critical risk factors (sleep/work/screen time)
2. Can be implemented immediately (today/tomorrow)
3. Are realistic and not overwhelming
4. Include specific time frames or measurements

Format each tip as a complete sentence starting with an action verb."""

    elif user_data.category == "Moderate":
        prompt += """

This user has MODERATE burnout risk. Focus on preventive measures and lifestyle adjustments.

Please provide 3 specific recommendations that:
1. Help prevent escalation to high risk
2. Address the concerning patterns in their data
3. Are sustainable long-term changes
4. Include specific, measurable goals

Format each tip as a complete sentence starting with an action verb."""

    else:  # Low risk
        prompt += """

This user has LOW burnout risk. Focus on maintaining good habits and optimization.

Please provide 3 specific recommendations that:
1. Help maintain their current healthy patterns
2. Optimize their existing routines
3. Build resilience for future stress
4. Are enhancement-focused rather than corrective

Format each tip as a complete sentence starting with an action verb."""

    return prompt

def get_fallback_tips(user_data: UserData) -> List[str]:
    """Provide evidence-based fallback tips when OpenAI is unavailable"""
    if user_data.category == "High":
        return [
            "Prioritize getting 7-8 hours of sleep tonight by setting a firm bedtime and avoiding screens 1 hour before.",
            "Take a 15-minute break every 2 hours during work to reduce stress and prevent mental fatigue.",
            "Limit recreational screen time to 2 hours today to give your mind time to rest and recover."
        ]
    elif user_data.category == "Moderate":
        return [
            "Establish a consistent sleep schedule by going to bed and waking up at the same time each day.",
            "Set boundaries around work hours by defining a clear end time and sticking to it.",
            "Practice the 20-20-20 rule: every 20 minutes, look at something 20 feet away for 20 seconds."
        ]
    else:  # Low risk
        return [
            "Continue your healthy sleep routine and consider adding a brief meditation before bed to enhance sleep quality.",
            "Maintain your work-life balance by scheduling regular breaks and leisure activities throughout the week.",
            "Use your current stability to build resilience through regular exercise or stress-management techniques."
        ]

# ===================================================================
# API ENDPOINTS
# ===================================================================

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint confirming service is running"""
    return {
        "service": "Mental Health Burnout Detection - AI Tips Service",
        "status": "running",
        "version": "1.0.0",
        "description": "AI-powered wellness recommendations",
        "endpoints": {
            "health": "/health",
            "tips": "/tips",
            "docs": "/docs"
        }
    }

@app.get("/health", response_model=HealthStatus)
async def health_check():
    """Health check endpoint for monitoring"""
    uptime = time.time() - SERVICE_START_TIME
    
    return HealthStatus(
        status="healthy",
        service="AI Tips Service",
        version="1.0.0",
        openai_available=USE_OPENAI,
        uptime_seconds=round(uptime, 2),
        timestamp=datetime.now().isoformat()
    )

@app.post("/tips", response_model=TipsResponse)
async def generate_wellness_tips(user_data: UserData):
    """
    Main endpoint for generating personalized wellness tips
    Uses modern async/await patterns and proper error handling
    """
    try:
        logger.info(f"Generating tips for user with {user_data.category} risk level")
        
        # Check cache first
        cache_key = generate_cache_key(user_data)
        if cache_key in TIPS_CACHE and is_cache_valid(TIPS_CACHE[cache_key]):
            logger.info("Returning cached tips")
            cached_response = TIPS_CACHE[cache_key]['response']
            cached_response.generated_at = datetime.now().isoformat()
            return cached_response
        
        tips = []
        model_used = "fallback"
        
        # Try OpenAI if available
        if USE_OPENAI:
            try:
                prompt = build_openai_prompt(user_data)
                
                # Modern OpenAI API call
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are a mental health and wellness expert. Provide specific, actionable advice."
                        },
                        {
                            "role": "user", 
                            "content": prompt
                        }
                    ],
                    max_tokens=300,
                    temperature=0.7,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                
                ai_response = response.choices[0].message.content.strip()
                
                # Parse response into tips
                tips = [tip.strip() for tip in ai_response.split('\n') if tip.strip() and not tip.strip().isdigit()]
                
                # Clean up tips
                cleaned_tips = []
                for tip in tips:
                    cleaned_tip = tip.lstrip('0123456789.-* ').strip()
                    if len(cleaned_tip) > 10:
                        cleaned_tips.append(cleaned_tip)
                
                tips = cleaned_tips[:3]
                model_used = "gpt-4"
                
                logger.info(f"Successfully generated {len(tips)} tips using OpenAI")
                
            except Exception as openai_error:
                logger.error(f"OpenAI API error: {openai_error}")
                tips = get_fallback_tips(user_data)
                model_used = "fallback"
        
        # Use fallback if needed
        if not tips:
            tips = get_fallback_tips(user_data)
            model_used = "fallback"
        
        # Ensure exactly 3 tips
        if len(tips) < 3:
            generic_tips = [
                "Take deep breaths and practice mindfulness for 5 minutes to reduce stress.",
                "Stay hydrated by drinking water regularly throughout the day.",
                "Connect with a friend or family member for social support."
            ]
            tips.extend(generic_tips[:3-len(tips)])
        
        tips = tips[:3]
        
        # Create response
        response = TipsResponse(
            tips=tips,
            generated_at=datetime.now().isoformat(),
            model_used=model_used,
            risk_level=user_data.category,
            confidence=0.9 if model_used == "gpt-4" else 0.7
        )
        
        # Cache response
        TIPS_CACHE[cache_key] = {
            'response': response,
            'timestamp': time.time()
        }
        
        logger.info(f"Successfully generated tips using {model_used}")
        return response
        
    except Exception as e:
        logger.error(f"Error generating tips: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate wellness tips: {str(e)}"
        )

@app.get("/cache/stats")
async def get_cache_stats():
    """Admin endpoint to monitor cache performance"""
    valid_entries = sum(1 for entry in TIPS_CACHE.values() if is_cache_valid(entry))
    
    return {
        "total_entries": len(TIPS_CACHE),
        "valid_entries": valid_entries,
        "cache_hit_rate": f"{(valid_entries / max(len(TIPS_CACHE), 1)) * 100:.1f}%",
        "cache_duration_seconds": CACHE_DURATION
    }

# ===================================================================
# ERROR HANDLERS
# ===================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors"""
    logger.error(f"Unhandled exception: {exc}")
    return {
        "error": "Internal server error",
        "message": "An unexpected error occurred while processing your request",
        "timestamp": datetime.now().isoformat()
    }

# ===================================================================
# MAIN ENTRY POINT
# ===================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app:app",  # "filename:fastapi_instance"
        host="127.0.0.1",
        port=5001,
        reload=True,
        log_level="info"
    )
