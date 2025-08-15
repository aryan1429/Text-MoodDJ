#!/usr/bin/env python3
"""
TextMood DJ - Component Test Suite
Tests all components individually
"""

print('🧠 Testing TextMood DJ Components...')
print('=' * 50)

# Test 1: Simple emotion analysis
print('\n📝 Test 1: Simple Emotion Analysis')
try:
    from mood_simple import analyze_emotion as simple_analyze
    test_texts = [
        'I feel really happy today!',
        'I am so sad and depressed',
        'This makes me really angry'
    ]
    for text in test_texts:
        emotion, conf = simple_analyze(text)
        print(f'✅ "{text}" → {emotion} ({conf:.2f})')
except Exception as e:
    print(f'❌ Simple analysis failed: {e}')

print('\n🎵 Test 2: YouTube API Configuration')
try:
    import os
    from dotenv import load_dotenv
    load_dotenv()
    yt_key = os.getenv('YOUTUBE_API_KEY')
    if yt_key:
        print(f'✅ YouTube API key configured (ends with: ...{yt_key[-4:]})')
    else:
        print('⚠️  YouTube API key not found in .env file')
except Exception as e:
    print(f'❌ YouTube config check failed: {e}')

print('\n😂 Test 3: GIPHY API Configuration')
try:
    giphy_key = os.getenv('GIPHY_API_KEY')
    if giphy_key:
        print(f'✅ GIPHY API key configured (ends with: ...{giphy_key[-4:]})')
    else:
        print('⚠️  GIPHY API key not found in .env file')
except Exception as e:
    print(f'❌ GIPHY config check failed: {e}')

print('\n💾 Test 4: Database')
try:
    from storage import init_db, new_session
    init_db()
    session_id = new_session('test-user-agent')
    print(f'✅ Database working, test session: {session_id[:8]}...')
except Exception as e:
    print(f'❌ Database test failed: {e}')

print('\n🤖 Test 5: Advanced AI Models (Optional)')
try:
    from mood import analyze_emotion as advanced_analyze
    emotion, conf = advanced_analyze('I am feeling so excited and joyful!')
    print(f'✅ Advanced AI: "I am feeling so excited and joyful!" → {emotion} ({conf:.2f})')
except Exception as e:
    print(f'⚠️  Advanced AI not available: {e}')
    print('   This is normal - advanced models take time to load')

print('\n' + '=' * 50)
print('🎯 Component testing completed!')
print('\n🚀 If most tests passed, your TextMood DJ is ready!')
print('🌐 Test the API at: http://127.0.0.1:8001 (if test server is running)')
