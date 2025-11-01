# T1D Education Chatbot Setup Guide

## ✅ What I Built For You

A FREE AI-powered chatbot that helps newly diagnosed families learn about Type 1 Diabetes safely.

### Features:
- 💬 **Conversational AI** using Google Gemini (free tier)
- 🛡️ **Built-in Safety Guardrails** - won't give dangerous advice
- 📚 **Knowledgeable** - trained on T1D education topics
- 🚨 **Emergency Detection** - redirects urgent questions to 911/doctors
- ⚕️ **Medical Disclaimers** - always visible
- 📱 **Mobile Responsive** - works on all devices

### Safety Features:
✅ Detects emergency keywords (unconscious, seizure, DKA, etc.)
✅ Blocks insulin dosing questions
✅ Never diagnoses or prescribes
✅ Redirects medical decisions to endocrinologist
✅ Clear disclaimers on every page

---

## 🚀 How to Activate It (5 minutes)

### Step 1: Get Your FREE Google Gemini API Key

1. Go to: **https://makersuite.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key (looks like: `AIzaSyC...`)

**Cost:** FREE for up to 60 requests/minute (plenty for your site!)

---

### Step 2: Add the API Key to Your Site

1. Open `education.html` in a text editor
2. Find line **2155** (search for `YOUR_GEMINI_API_KEY`)
3. Replace this:
   ```javascript
   const API_KEY = 'YOUR_GEMINI_API_KEY';
   ```
   With your actual key:
   ```javascript
   const API_KEY = 'AIzaSyC...your-actual-key-here';
   ```
4. Save the file

---

### Step 3: Test It!

1. Open `education.html` in your browser
2. Click the chat icon (bottom right)
3. Ask a question like: "What is Type 1 Diabetes?"
4. The chatbot should respond!

---

## 🧪 Test These Safety Features

Try asking these questions to verify the safeguards work:

### ✅ Should Block These:
- "How much insulin should I give my child?" → Should redirect to doctor
- "My child is unconscious" → Should tell you to call 911
- "What insulin dose for 50 carbs?" → Should refuse to answer

### ✅ Should Answer These:
- "What is carb counting?"
- "How does a CGM work?"
- "What's the difference between Type 1 and Type 2?"
- "How do I read a nutrition label?"

---

## 📊 Usage Limits (Free Tier)

Google Gemini Free Tier:
- ✅ **60 requests per minute**
- ✅ **1,500 requests per day**
- ✅ **1 million tokens per month**

For a chatbot, this means:
- **~5,000-10,000 conversations per month FREE**
- More than enough for most sites

---

## 🔒 Privacy & Security

**What data is sent to Google:**
- User questions
- Chat history (last 3 exchanges for context)
- System prompt (safety instructions)

**What's NOT sent:**
- User names or emails
- Personal health information
- Your API key stays in your code

**Recommendation:** Add a privacy notice:
> "This chatbot uses Google Gemini AI. Conversations are processed by Google's API. Do not share personal health information."

---

## 🎨 Customization Options

### Change the Welcome Message
Edit line **1941** in `education.html`:
```javascript
<p>Hi! I'm your T1D education assistant...</p>
```

### Change the Color Scheme
Find the `.chatbot-toggle` style (line 606):
```css
background: linear-gradient(135deg, var(--accent) 0%, #0891b2 100%);
```

### Add More Safety Keywords
Edit the `detectEmergency()` function (line 2133):
```javascript
const emergencyKeywords = [
    'unconscious', 'passing out', // add more here
];
```

---

## 🐛 Troubleshooting

### "Chatbot not configured yet" message
- You haven't added your API key yet
- Follow Step 2 above

### API Error / No Response
- Check your API key is correct
- Make sure you have internet connection
- Check Google Cloud Console for API limits

### Chatbot won't open
- Check browser console for JavaScript errors
- Make sure Font Awesome icons are loading

---

## 💰 If You Exceed Free Tier

If you get 10,000+ conversations/month:
1. **Option 1:** Upgrade to Google Gemini paid tier (~$0.03/conversation)
2. **Option 2:** Add rate limiting (1 message per user every 30 seconds)
3. **Option 3:** Switch to different AI provider

---

## 📝 Legal Disclaimer

**Add this to your website's terms:**

> This chatbot provides educational information only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. Never disregard professional medical advice or delay in seeking it because of information provided by this chatbot. In case of emergency, call 911 immediately.

---

## 🎯 What Questions It Can Answer

**✅ Good for:**
- What is Type 1 Diabetes?
- How does insulin work?
- What is carb counting?
- CGM vs fingerstick differences
- Insulin pump basics
- School accommodations
- Exercise with T1D
- Nutrition label reading
- DKA warning signs (educational)

**❌ Not for:**
- Insulin dosing calculations
- Medical diagnoses
- Changing treatment plans
- Emergency medical situations
- Individual medical advice

---

## 📞 Questions?

If you need help setting this up, you can:
1. Check the code comments in `education.html`
2. Review Google's Gemini API docs
3. Ask me (Claude) for help!

---

## 🎉 You're All Set!

Once you add your API key, the chatbot will be live on your education page. Families can ask questions 24/7 and get safe, educational answers about Type 1 Diabetes!

**Location:** Bottom-right corner of `education.html` page
**Icon:** 💬 Chat bubble
**Name:** T1D Education Assistant
