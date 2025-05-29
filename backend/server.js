// ===================================================================
// MENTAL HEALTH BURNOUT DETECTION SYSTEM - BACKEND SERVER
// ===================================================================
// This is the main Express.js server that handles all API requests
// for the Mental Health Burnout Detection System as specified in
// the project documentation.
// ===================================================================

// Import required dependencies
const express = require('express');      // Web framework for Node.js
const cors = require('cors');            // Enable Cross-Origin Resource Sharing
const helmet = require('helmet');        // Security middleware for HTTP headers
const morgan = require('morgan');        // HTTP request logger middleware

// Create Express application instance
const app = express();

// Define server port (use environment variable or default to 3000)
const PORT = process.env.PORT || 3000;

// ===================================================================
// MIDDLEWARE CONFIGURATION
// ===================================================================

// Security middleware - adds various HTTP headers for security
app.use(helmet());

// CORS middleware - allows frontend to make requests from different origins
app.use(cors({
    origin: [
        'http://localhost:3000',     // Local development
        'http://127.0.0.1:3000',     // Alternative localhost
        'file://',                   // For file:// protocol (opening HTML directly)
        'http://localhost:8080',     // Alternative frontend port
        'http://localhost:5000'      // Another common development port
    ],
    credentials: true,               // Allow cookies and auth headers
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],  // Allowed HTTP methods
    allowedHeaders: ['Content-Type', 'Authorization']       // Allowed headers
}));

// Body parsing middleware - converts JSON requests to JavaScript objects
app.use(express.json({ limit: '10mb' }));              // Parse JSON bodies
app.use(express.urlencoded({ extended: true }));       // Parse URL-encoded bodies

// Logging middleware - logs all HTTP requests for debugging
app.use(morgan('combined'));

// ===================================================================
// HEALTH CHECK ENDPOINTS
// ===================================================================

// Basic health check endpoint - confirms server is running
app.get('/', (req, res) => {
    res.status(200).json({
        status: 'OK',
        message: 'Mental Health Burnout Detection System Backend is running!',
        timestamp: new Date().toISOString(),
        version: '1.0.0'
    });
});

// Detailed health check endpoint - for monitoring and deployment
app.get('/health', (req, res) => {
    res.status(200).json({
        status: 'healthy',
        service: 'Mental Health Burnout Detection Backend',
        uptime: process.uptime(),
        timestamp: new Date().toISOString(),
        memory: process.memoryUsage(),
        environment: process.env.NODE_ENV || 'development'
    });
});

// ===================================================================
// MAIN API ENDPOINTS
// ===================================================================

// BURNOUT RISK PREDICTION ENDPOINT
// This is the core endpoint that calculates burnout risk based on user input
app.post('/api/predict', (req, res) => {
    try {
        // Extract user data from request body
        const { sleep, work, screen, heartRate, steps } = req.body;
        
        // Input validation - ensure required fields are present and valid
        if (sleep === undefined || work === undefined || screen === undefined) {
            return res.status(400).json({
                error: 'Missing required fields',
                required: ['sleep', 'work', 'screen'],
                received: { sleep, work, screen }
            });
        }

        // Validate that values are positive numbers
        if (sleep < 0 || work < 0 || screen < 0) {
            return res.status(400).json({
                error: 'All values must be positive numbers',
                received: { sleep, work, screen }
            });
        }

        // Validate reasonable ranges
        if (sleep > 24 || work > 24 || screen > 24) {
            return res.status(400).json({
                error: 'Hours cannot exceed 24 per day',
                received: { sleep, work, screen }
            });
        }

        // ===============================================================
        // BURNOUT RISK CALCULATION ALGORITHM
        // ===============================================================
        // This implements a simple risk scoring algorithm based on
        // established burnout research factors:
        // - Sleep deprivation (< 6 hours)
        // - Overwork (> 9 hours)
        // - Excessive screen time (> 6 hours)
        // ===============================================================

        let riskScore = 0.3; // Base risk score (everyone has some baseline risk)

        // Sleep factor - insufficient sleep increases burnout risk
        if (sleep < 4) {
            riskScore += 0.3;        // Severe sleep deprivation
        } else if (sleep < 6) {
            riskScore += 0.2;        // Moderate sleep deprivation
        } else if (sleep < 7) {
            riskScore += 0.1;        // Mild sleep deprivation
        }
        // Optimal sleep (7-9 hours) adds no additional risk

        // Work hours factor - overwork is a primary burnout cause
        if (work > 12) {
            riskScore += 0.3;        // Extreme overwork
        } else if (work > 10) {
            riskScore += 0.2;        // Heavy overwork
        } else if (work > 8) {
            riskScore += 0.1;        // Moderate overwork
        }
        // Normal work hours (≤8) add no additional risk

        // Screen time factor - excessive screen time indicates poor work-life balance
        if (screen > 10) {
            riskScore += 0.2;        // Excessive screen time
        } else if (screen > 8) {
            riskScore += 0.15;       // High screen time
        } else if (screen > 6) {
            riskScore += 0.1;        // Moderate screen time
        }

        // Additional factors (if provided)
        if (heartRate && heartRate > 90) {
            riskScore += 0.05;       // Elevated resting heart rate
        }
        
        if (steps && steps < 3000) {
            riskScore += 0.05;       // Sedentary lifestyle
        }

        // Cap the risk score at 1.0 (100%)
        if (riskScore > 1.0) {
            riskScore = 1.0;
        }

        // Determine risk category based on score
        let category;
        let description;
        let urgency;

        if (riskScore >= 0.8) {
            category = "High";
            description = "Immediate attention needed - high burnout risk detected";
            urgency = "urgent";
        } else if (riskScore >= 0.6) {
            category = "Moderate";
            description = "Some concerning patterns - consider lifestyle adjustments";
            urgency = "moderate";
        } else if (riskScore >= 0.4) {
            category = "Low-Moderate";
            description = "Minor risk factors present - maintain awareness";
            urgency = "low";
        } else {
            category = "Low";
            description = "Good work-life balance - keep up the healthy habits";
            urgency = "none";
        }

        // Log the prediction for monitoring and debugging
        console.log(`[PREDICTION] User data: sleep=${sleep}h, work=${work}h, screen=${screen}h | Risk: ${riskScore.toFixed(3)} (${category})`);

        // Return the prediction results
        res.status(200).json({
            success: true,
            score: riskScore.toFixed(3),     // Risk score (0-1, 3 decimal places)
            category: category,              // Risk category (Low/Moderate/High)
            description: description,        // Human-readable description
            urgency: urgency,               // Urgency level for frontend styling
            factors: {                      // Breakdown of contributing factors
                sleep: sleep < 6 ? 'insufficient' : 'adequate',
                work: work > 9 ? 'excessive' : 'normal',
                screen: screen > 6 ? 'high' : 'normal'
            },
            timestamp: new Date().toISOString(),
            modelVersion: '1.0.0'           // For tracking model versions
        });

    } catch (error) {
        // Handle any unexpected errors
        console.error('[ERROR] Prediction endpoint error:', error);
        res.status(500).json({
            error: 'Internal server error during risk prediction',
            message: error.message,
            timestamp: new Date().toISOString()
        });
    }
});

// ===================================================================
// USER SETTINGS ENDPOINT (for future expansion)
// ===================================================================

// Get user settings (placeholder for future database integration)
app.get('/api/settings', (req, res) => {
    res.status(200).json({
        thresholds: {
            low: 0.3,
            moderate: 0.6,
            high: 0.8
        },
        notifications: {
            email: true,
            push: false,
            inApp: true
        },
        preferences: {
            dataRetention: 90,
            timezone: 'UTC'
        }
    });
});

// Update user settings (placeholder for future database integration)
app.post('/api/settings', (req, res) => {
    const { thresholds, notifications, preferences } = req.body;
    
    // In a real implementation, this would update the database
    console.log('[SETTINGS] Updated user settings:', { thresholds, notifications, preferences });
    
    res.status(200).json({
        success: true,
        message: 'Settings updated successfully',
        timestamp: new Date().toISOString()
    });
});

// ===================================================================
// ERROR HANDLING MIDDLEWARE
// ===================================================================

// Handle 404 errors - when no route matches the request
// ✅ This fixes the error
app.use('/*path', (req, res) => {
    res.status(404).json({
        error: 'Route not found',
        message: `The endpoint ${req.method} ${req.originalUrl} does not exist`,
        availableEndpoints: [
            'GET /',
            'GET /health', 
            'POST /api/predict',
            'GET /api/settings',
            'POST /api/settings'
        ],
        timestamp: new Date().toISOString()
    });
});


// Global error handler - catches any unhandled errors
app.use((error, req, res, next) => {
    console.error('[GLOBAL ERROR]', error);
    
    res.status(500).json({
        error: 'Internal server error',
        message: process.env.NODE_ENV === 'development' ? error.message : 'Something went wrong',
        timestamp: new Date().toISOString()
    });
});

// ===================================================================
// SERVER STARTUP
// ===================================================================

// Start the server and listen on the specified port
app.listen(PORT, () => {
    console.log('='.repeat(60));
    console.log('🧠 MENTAL HEALTH BURNOUT DETECTION SYSTEM');
    console.log('='.repeat(60));
    console.log(`🚀 Server running on http://localhost:${PORT}`);
    console.log(`📊 Environment: ${process.env.NODE_ENV || 'development'}`);
    console.log(`⏰ Started at: ${new Date().toISOString()}`);
    console.log('='.repeat(60));
    console.log('📋 Available endpoints:');
    console.log(`   GET  http://localhost:${PORT}/`);
    console.log(`   GET  http://localhost:${PORT}/health`);
    console.log(`   POST http://localhost:${PORT}/api/predict`);
    console.log(`   GET  http://localhost:${PORT}/api/settings`);
    console.log(`   POST http://localhost:${PORT}/api/settings`);
    console.log('='.repeat(60));
});

// Handle graceful shutdown
process.on('SIGTERM', () => {
    console.log('👋 Received SIGTERM, shutting down gracefully...');
    process.exit(0);
});

process.on('SIGINT', () => {
    console.log('👋 Received SIGINT, shutting down gracefully...');
    process.exit(0);
});

// Export the app for testing purposes
module.exports = app;
