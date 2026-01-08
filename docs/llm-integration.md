# LOND-AI — LLM Integration

## Purpose
The LLM is used to generate a structured training plan when a user selects modules and (optionally) uploads documents.

## Environment Variables
- OPENAI_API_KEY (required) — stored in server environment / Azure settings. DO NOT commit real keys to GitHub.
- OPENAI_MODEL (optional) — default: gpt-4.1-mini

Example:
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-4.1-mini

## Endpoint (to implement in backend)
POST /lm/training-plan

### Request body (example)
```json
{
  "user": {
    "role": "Warehouse Operative",
    "learningNeeds": ["Manual handling", "Fire safety"],
    "demographics": {"language":"en"},
    "pastExperience": "New starter"
  },
  "availableModules": [
    {"id":"osha_fire_101","title":"Fire Safety Basics","minutes":20},
    {"id":"osha_manual_201","title":"Manual Handling","minutes":30}
  ],
  "selectedModuleIds": ["osha_fire_101","osha_manual_201"],
  "uploadedDocs": [
    {"docId":"blob://indg163.pdf","title":"HSE INDG163","textExtract":"optional summary text"}
  ],
  "constraints": {"totalMinutesMax": 90, "days": 5}
}


#Response body (required JSON format)
{
  "planTitle": "Week 1 Onboarding",
  "days": [
    {
      "day": 1,
      "items": [
        {
          "moduleId": "osha_fire_101",
          "minutes": 20,
          "objective": "Understand evacuation steps",
          "whyThisNow": "Foundational safety knowledge"
        }
      ]
    }
  ],
  "assessment": {
    "quizTopics": ["Evacuation", "Fire triangle"],
    "riskFlags": ["New starter"]
  }
}
