# 🔄 Automatic Provider Switching Guide

**Author: Dippu Kumar**

## Overview

The Universal Chatbot now includes intelligent automatic provider switching that seamlessly transitions between AI providers when quota limits are reached, ensuring uninterrupted conversations.

## 🚀 Features

### ✅ Automatic Quota Detection
- Detects quota/rate limit errors (429 status codes)
- Recognizes various quota-related error messages:
  - "exceeded your current quota"
  - "rate limit"
  - "requests per day"
  - "free tier"
  - "billing details"

### ✅ Smart Provider Fallback
- **Priority Order**: OpenAI → Claude → Gemini
- **Excludes Failed Provider**: Won't retry the provider that just failed
- **Validates Success**: Ensures new provider is actually working before committing
- **Maximum Retries**: Attempts up to 3 provider switches per message

### ✅ Conversation Preservation
- **History Maintained**: Your conversation history is preserved during switches
- **Seamless Experience**: User doesn't lose context or need to restart
- **Real-time Notifications**: Clear visual feedback about what's happening

## 🛠 How It Works

### 1. Quota Error Detection
```python
def is_quota_error(self, error_message: str) -> bool:
    """Check if an error is a quota/rate limit error"""
    error_lower = error_message.lower()
    quota_indicators = [
        "quota", "rate limit", "429", 
        "exceeded your current quota",
        "requests per day", "free tier",
        "billing details"
    ]
    return any(indicator in error_lower for indicator in quota_indicators)
```

### 2. Automatic Switching Process
When a quota error is detected:

1. **Identify Available Providers**
   - Get all installed/configured providers
   - Exclude the failed provider
   - Sort by priority (OpenAI → Claude → Gemini)

2. **Attempt Provider Switch**
   - Update configuration with new provider
   - Reinitialize the AI model
   - Verify the switch was successful

3. **Retry Original Request**
   - Use new provider to process the user's message
   - Preserve conversation history
   - Continue seamlessly

4. **User Notification**
   - Display beautiful panel showing the switch
   - Indicate which providers were involved
   - Confirm conversation history preservation

### 3. Error Handling
- **Validation**: Each provider switch is validated before proceeding
- **Fallback Chain**: If one provider fails, tries the next one
- **Graceful Degradation**: If all providers fail, shows helpful guidance
- **Reset Protection**: Failed switches don't permanently change configuration

## 🎯 User Experience

### What You'll See

When a quota limit is reached:

```
┌─────────────────── 🔄 Provider Auto-Switch ───────────────────┐
│ ⚠️ Quota limit reached for Gemini                            │
│                                                              │
│ ✅ Automatically switched to OpenAI                          │
│                                                              │
│ 💬 Your conversation history has been preserved              │
└──────────────────────────────────────────────────────────────┘
```

### Enhanced Error Messages
For quota errors that can't be auto-resolved:

```
┌─────────────────── 🚫 Quota Exceeded ─────────────────────┐
│ ❌ Quota Limit Reached: [error details]                   │
│                                                           │
│ ⚠️ All available providers have reached their quota       │
│ limits.                                                   │
│                                                           │
│ 💡 Suggestions:                                           │
│ • Wait for quota reset (usually 24 hours)                │
│ • Upgrade to paid plans for higher limits                │
│ • Use /providers to check provider status                │
│ • Use /switch to manually try a different provider       │
└───────────────────────────────────────────────────────────┘
```

## 🔧 Configuration

### Provider Priority
The default priority order is:
1. **OpenAI** - Generally most reliable
2. **Claude** - Good backup option  
3. **Gemini** - Fallback choice

### Retry Limits
- **Maximum Retries**: 3 attempts per message
- **Provider Exclusion**: Failed providers are excluded from retry attempts
- **Validation**: Each switch is verified before proceeding

## 📋 Commands

The chatbot includes several commands to help you manage providers:

- `/providers` - Show available AI providers and their status
- `/switch` - Manually switch AI provider/model
- `/help` - Shows information about automatic switching
- `/config` - Display current configuration

## 🏗 Technical Implementation

### Key Methods Added

1. **`auto_switch_provider(exclude_provider=None)`**
   - Automatically switches to next available provider
   - Excludes failed providers
   - Returns success/failure status

2. **`is_quota_error(error_message)`**
   - Detects quota-related errors
   - Uses comprehensive keyword matching
   - Case-insensitive detection

3. **Enhanced Chat Loop**
   - Wraps model invocation with retry logic
   - Preserves conversation history during switches
   - Provides detailed error feedback

### Integration Points

- **Model Factory**: Uses existing provider infrastructure
- **Configuration System**: Leverages current config management
- **Error Handling**: Enhances existing exception handling
- **User Interface**: Integrates with Rich console styling

## 🔬 Testing

The implementation includes comprehensive error detection testing and provider switching validation. All functionality is verified to work correctly with various quota error scenarios.

## 💡 Benefits

1. **Uninterrupted Conversations**: Never lose your chat flow due to quota limits
2. **Zero Configuration**: Works automatically without user intervention
3. **Transparent Process**: Clear feedback about what's happening
4. **History Preservation**: Conversation context is always maintained
5. **Intelligent Fallback**: Tries providers in order of reliability
6. **Graceful Degradation**: Helpful guidance when all options are exhausted

---

This feature ensures that quota limits never interrupt your AI conversations, providing a seamless and robust chatbot experience!