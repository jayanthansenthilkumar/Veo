"""
Run script for Gen AI Platform
Simple script to start the Flask application
"""

import os
from app import app

if __name__ == '__main__':
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"""
    ╔═══════════════════════════════════════════════╗
    ║     Gen AI Platform - Starting Server         ║
    ╠═══════════════════════════════════════════════╣
    ║  Server: http://{host}:{port}                ║
    ║  Environment: {os.environ.get('FLASK_ENV', 'development')}                     ║
    ╚═══════════════════════════════════════════════╝
    """)
    
    # Run the application
    app.run(
        host=host,
        port=port,
        debug=os.environ.get('FLASK_DEBUG', '1') == '1'
    )
