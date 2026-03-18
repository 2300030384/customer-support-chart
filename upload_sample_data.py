"""
Script to upload sample conversation data from Kaggle to the backend API
Create conversations with sentiment analysis and escalation detection
"""
import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict

API_BASE_URL = "http://localhost:8000"

# Sample customer support conversations (realistic examples)
SAMPLE_CONVERSATIONS = [
    {
        "thread_id": "chat_001",
        "platform": "email",
        "messages": [
            {
                "speaker": "customer",
                "text": "Hi, I ordered item #12345 but it hasn't arrived after 2 weeks. This is unacceptable!",
                "timestamp": "2026-02-15T09:00:00"
            },
            {
                "speaker": "agent",
                "text": "Thank you for contacting us. I sincerely apologize for the delay. Let me check your order status right away.",
                "timestamp": "2026-02-15T09:15:00"
            },
            {
                "speaker": "agent",
                "text": "I see that your package is stuck in transit. The carrier has updated it as delayed. We'll send you a replacement immediately at no charge.",
                "timestamp": "2026-02-15T09:30:00"
            },
            {
                "speaker": "customer",
                "text": "Wow, thank you so much! I really appreciate your quick response and solution. You've made this right!",
                "timestamp": "2026-02-15T09:45:00"
            }
        ]
    },
    {
        "thread_id": "chat_002",
        "platform": "chat",
        "messages": [
            {
                "speaker": "customer",
                "text": "Your product is terrible! It broke after one week.",
                "timestamp": "2026-02-16T14:00:00"
            },
            {
                "speaker": "agent",
                "text": "I'm sorry to hear that. Can you describe what happened?",
                "timestamp": "2026-02-16T14:05:00"
            },
            {
                "speaker": "customer",
                "text": "The screen just went black. This is absolutely ridiculous. I want a refund NOW!",
                "timestamp": "2026-02-16T14:10:00"
            },
            {
                "speaker": "agent",
                "text": "I understand your frustration. We can arrange a return or replacement. Could you provide your order number?",
                "timestamp": "2026-02-16T14:15:00"
            },
            {
                "speaker": "customer",
                "text": "Fine. It's ORD-98765432. But I'm seriously considering reporting this to consumer protection.",
                "timestamp": "2026-02-16T14:20:00"
            },
            {
                "speaker": "agent",
                "text": "Thank you. I'm escalating this to our manager who will contact you within 24 hours with a full resolution.",
                "timestamp": "2026-02-16T14:25:00"
            }
        ]
    },
    {
        "thread_id": "chat_003",
        "platform": "twitter",
        "messages": [
            {
                "speaker": "customer",
                "text": "Just got my new purchase today and I'm loving it! The quality is amazing!",
                "timestamp": "2026-02-17T10:00:00"
            },
            {
                "speaker": "agent",
                "text": "That's wonderful to hear! Thank you for choosing us. Your satisfaction is our priority.",
                "timestamp": "2026-02-17T10:10:00"
            },
            {
                "speaker": "customer",
                "text": "Definitely recommending you guys to all my friends. Best purchase ever!",
                "timestamp": "2026-02-17T10:20:00"
            }
        ]
    },
    {
        "thread_id": "chat_004",
        "platform": "phone",
        "messages": [
            {
                "speaker": "customer",
                "text": "I can't figure out how to use this feature. The instructions are confusing.",
                "timestamp": "2026-02-18T11:00:00"
            },
            {
                "speaker": "agent",
                "text": "No problem! I'm happy to help walk you through it. Let me explain step by step.",
                "timestamp": "2026-02-18T11:05:00"
            },
            {
                "speaker": "agent",
                "text": "First, go to settings, then select 'features', and you'll see the option there.",
                "timestamp": "2026-02-18T11:10:00"
            },
            {
                "speaker": "customer",
                "text": "Oh wow, that was easy! Thanks for your patience. Much clearer now!",
                "timestamp": "2026-02-18T11:15:00"
            }
        ]
    },
    {
        "thread_id": "chat_005",
        "platform": "email",
        "messages": [
            {
                "speaker": "customer",
                "text": "Your customer service is the worst I've ever experienced. I've been waiting for a response for 3 days!",
                "timestamp": "2026-02-19T08:00:00"
            },
            {
                "speaker": "agent",
                "text": "I sincerely apologize for the delayed response. This is not the standard we strive for.",
                "timestamp": "2026-02-19T08:30:00"
            },
            {
                "speaker": "customer",
                "text": "I'm extremely frustrated. I need immediate assistance or I'm canceling my account!",
                "timestamp": "2026-02-19T08:45:00"
            },
            {
                "speaker": "agent",
                "text": "I completely understand your frustration. I'm personally taking over your case. What can I resolve for you immediately?",
                "timestamp": "2026-02-19T09:00:00"
            },
            {
                "speaker": "customer",
                "text": "I need a full refund for the service fee charged due to the poor support.",
                "timestamp": "2026-02-19T09:15:00"
            },
            {
                "speaker": "agent",
                "text": "I've processed a full refund to your account. It will appear within 24-48 hours. I apologize again for the experience.",
                "timestamp": "2026-02-19T09:30:00"
            }
        ]
    },
    {
        "thread_id": "chat_006",
        "platform": "chat",
        "messages": [
            {
                "speaker": "customer",
                "text": "Hi! I have a quick question about a product.",
                "timestamp": "2026-02-20T13:00:00"
            },
            {
                "speaker": "agent",
                "text": "Hello! I'd be happy to help. What's your question?",
                "timestamp": "2026-02-20T13:05:00"
            },
            {
                "speaker": "customer",
                "text": "Is this product available in black color?",
                "timestamp": "2026-02-20T13:10:00"
            },
            {
                "speaker": "agent",
                "text": "Yes, it comes in black, white, and silver. We have all colors in stock!",
                "timestamp": "2026-02-20T13:15:00"
            },
            {
                "speaker": "customer",
                "text": "Great! I'll order the black one. Thanks for the quick help!",
                "timestamp": "2026-02-20T13:20:00"
            }
        ]
    },
    {
        "thread_id": "chat_007",
        "platform": "email",
        "messages": [
            {
                "speaker": "customer",
                "text": "I'm very disappointed with my purchase. The quality is below expectation.",
                "timestamp": "2026-02-20T15:00:00"
            },
            {
                "speaker": "agent",
                "text": "I'm sorry to hear that. We pride ourselves on quality. Can you tell us what specifically fell short?",
                "timestamp": "2026-02-20T15:20:00"
            },
            {
                "speaker": "customer",
                "text": "The stitching is coming apart on the seams. This is unacceptable for the price I paid.",
                "timestamp": "2026-02-20T15:40:00"
            },
            {
                "speaker": "agent",
                "text": "That's definitely not up to our standards. I'd like to make this right. We can replace it or issue a refund.",
                "timestamp": "2026-02-20T16:00:00"
            },
            {
                "speaker": "customer",
                "text": "A replacement would be nice. I hope the next one is better quality.",
                "timestamp": "2026-02-20T16:20:00"
            }
        ]
    },
    {
        "thread_id": "chat_008",
        "platform": "chat",
        "messages": [
            {
                "speaker": "customer",
                "text": "HELP! I CANNOT ACCESS MY ACCOUNT AND I HAVE A MEETING IN 10 MINUTES!!!",
                "timestamp": "2026-02-21T08:00:00"
            },
            {
                "speaker": "agent",
                "text": "I understand this is urgent! Let me help you immediately. What's your account email?",
                "timestamp": "2026-02-21T08:02:00"
            },
            {
                "speaker": "customer",
                "text": "It's user@example.com. Please hurry, I need access NOW!",
                "timestamp": "2026-02-21T08:03:00"
            },
            {
                "speaker": "agent",
                "text": "I'm resetting your password now. Check your email in 30 seconds. You should be able to access immediately.",
                "timestamp": "2026-02-21T08:04:00"
            },
            {
                "speaker": "customer",
                "text": "YES! It worked! Thank you so much for the instant help! You're a lifesaver!",
                "timestamp": "2026-02-21T08:05:00"
            }
        ]
    }
]


def upload_conversations():
    """Upload all sample conversations to the backend"""
    print("[*] Starting to upload sample conversations...\n")
    
    successful = 0
    failed = 0
    
    for conv_data in SAMPLE_CONVERSATIONS:
        try:
            # Make API request
            response = requests.post(
                f"{API_BASE_URL}/conversations/upload-thread",
                json=conv_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"[OK] {conv_data['thread_id']} - Uploaded successfully")
                print(f"   Sentiment: {result.get('overall_sentiment', 'N/A'):.2f}")
                print(f"   Escalation: {result.get('escalation_detected', False)}")
                print(f"   Outcome: {result.get('final_outcome', 'N/A')}")
                print()
                successful += 1
            else:
                print(f"[FAIL] {conv_data['thread_id']} - Failed with status {response.status_code}")
                print(f"   Error: {response.text}\n")
                failed += 1
        
        except requests.exceptions.ConnectionError:
            print(f"[FAIL] {conv_data['thread_id']} - Could not connect to API")
            print(f"   Make sure backend is running on {API_BASE_URL}\n")
            failed += 1
        except Exception as e:
            print(f"[FAIL] {conv_data['thread_id']} - Error: {str(e)}\n")
            failed += 1
    
    # Summary
    print("\n" + "="*60)
    print(f"[SUMMARY] Upload Results")
    print("="*60)
    print(f"[OK] Successful: {successful}/{len(SAMPLE_CONVERSATIONS)}")
    print(f"[FAIL] Failed: {failed}/{len(SAMPLE_CONVERSATIONS)}")
    print("="*60)


def get_analytics():
    """Retrieve analytics after uploading"""
    try:
        response = requests.get(f"{API_BASE_URL}/analytics/overview", timeout=10)
        if response.status_code == 200:
            print("\n[ANALYTICS] Overview Report")
            print("="*60)
            data = response.json()
            print(f"Total Threads: {data.get('total_threads', 0)}")
            print(f"Escalated: {data.get('escalated_threads', 0)}")
            print(f"Resolved: {data.get('resolved_threads', 0)}")
            print(f"Unresolved: {data.get('unresolved_threads', 0)}")
            print(f"Escalation Rate: {data.get('escalation_rate', 0):.1f}%")
            print(f"Avg Sentiment: {data.get('avg_sentiment', 0):.2f}")
            print("="*60 + "\n")
    except Exception as e:
        print(f"Could not retrieve analytics: {e}\n")


if __name__ == "__main__":
    upload_conversations()
    get_analytics()
    print("[INFO] Go to http://localhost:5174 to view the dashboard with the uploaded data!")
