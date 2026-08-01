{
  "name": "v2-VLT-Demo-1-REFACTORED-STUDENT",
  "nodes": [
    {
      "parameters": {
        "pollTimes": {
          "item": [
            {
              "mode": "everyMinute"
            }
          ]
        },
        "filters": {}
      },
      "type": "n8n-nodes-base.gmailTrigger",
      "typeVersion": 1.4,
      "position": [
        512,
        -240
      ],
      "id": "22a5991f-0bd9-4871-86eb-19d0e7e7877e",
      "name": "Gmail Trigger",
      "credentials": {
        "gmailOAuth2": {
          "id": "eaHDkc3KGa3ONFvL",
          "name": "Gmail account"
        }
      }
    },
    {
      "parameters": {
        "jsCode": "const r = $json || {};\n\n// Get full body from payload if available\nlet fullBody = \"\";\nif (r.payload && r.payload.parts) {\n  for (const part of r.payload.parts) {\n    if (part.mimeType === \"text/plain\" && part.body && part.body.data) {\n      fullBody = Buffer.from(part.body.data, 'base64').toString('utf-8');\n      break;\n    }\n  }\n}\n\n// Fallback: use snippet if full body not available\nconst body = fullBody || r.snippet || \"\";\n\nconst sender = r.From || \"\";\nconst subject = r.Subject || \"\";\n\n// Priority rules\nconst text = (subject + \" \" + body).toLowerCase();\nlet priority = \"Low\";\n\nif (/urgent|critical|immediately|down/i.test(text)) {\n  priority = \"High\";\n} else if (/issue|problem|error|delay/i.test(text)) {\n  priority = \"Medium\";\n}\n\nreturn [{\n  json: {\n    timestamp: new Date().toISOString(),\n    sender: sender,\n    subject: subject,\n    body: body.substring(0, 500),  // Truncate to avoid huge payloads\n    priority: priority\n  }\n}];"
      },
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        720,
        -240
      ],
      "id": "f9893e47-9619-48d1-a8ab-72f1745900c9",
      "name": "Parse & Prioritize"
    },
    {
      "parameters": {
        "operation": "append",
        "documentId": {
          "__rl": true,
          "value": "1DzaAMdVCjeivFtjnPIyNVmmHdNfqr11zvRENELnoGD8",
          "mode": "list",
          "cachedResultName": "Ticket Log",
          "cachedResultUrl": "https://docs.google.com/spreadsheets/d/1DzaAMdVCjeivFtjnPIyNVmmHdNfqr11zvRENELnoGD8/edit?usp=drivesdk"
        },
        "sheetName": {
          "__rl": true,
          "value": "gid=0",
          "mode": "list",
          "cachedResultName": "Sheet1",
          "cachedResultUrl": "https://docs.google.com/spreadsheets/d/1MJc2p2o2xDS6SbzxF5DwFZGUz4YRRS_PrQXmCtO8vYA/edit#gid=0"
        },
        "columns": {
          "mappingMode": "defineBelow",
          "value": {
            "sender": "={{$json.sender}}",
            "subject": "={{$json.subject}}",
            "priority": "={{$json.priority}}",
            "status": "Logged",
            " timestamp": "={{ $now.toFormat('yyyy-MM-dd HH:mm:ss') }}"
          },
          "matchingColumns": [],
          "schema": [
            {
              "id": " timestamp",
              "displayName": " timestamp",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true,
              "removed": false
            },
            {
              "id": "sender",
              "displayName": "sender",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true,
              "removed": false
            },
            {
              "id": "subject",
              "displayName": "subject",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true,
              "removed": false
            },
            {
              "id": "priority",
              "displayName": "priority",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true,
              "removed": false
            },
            {
              "id": "status",
              "displayName": "status",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true,
              "removed": false
            }
          ],
          "attemptToConvertTypes": false,
          "convertFieldsToString": false
        },
        "options": {}
      },
      "type": "n8n-nodes-base.googleSheets",
      "typeVersion": 4.7,
      "position": [
        928,
        -240
      ],
      "id": "81a3b70a-c5ee-44ff-b468-3ce9cb79fdc7",
      "name": "Append row in sheet",
      "credentials": {
        "googleSheetsOAuth2Api": {
          "id": "llpwz1aBfiv7l3MN",
          "name": "Google Sheets account"
        }
      }
    }
  ],
  "pinData": {},
  "connections": {
    "Gmail Trigger": {
      "main": [
        [
          {
            "node": "Parse & Prioritize",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Parse & Prioritize": {
      "main": [
        [
          {
            "node": "Append row in sheet",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": false,
  "settings": {
    "executionOrder": "v1",
    "binaryMode": "separate"
  },
  "versionId": "904b0966-2ffb-4c0d-aebd-671887dd96ee",
  "meta": {
    "templateCredsSetupCompleted": true,
    "instanceId": "bc8d23ff8aa9d1f20b0aae6ad87c8a06cbeef514e70c18e0bfc99a1e51385e73"
  },
  "nodeGroups": [],
  "id": "jfrnAaL42L6ZUjHo",
  "tags": []
}