## Screenshots

### 1. Architecture & API Documentation
| | Description |
|---|-------------|
| ![Swagger UI](screenshots/Screenshot%20Linkedin%20Content%20Automation%20Application%20Swagger.png) | FastAPI Swagger UI showing the `/linkedin` endpoint documentation |
| ![Full Workflow](screenshots/Screenshot%20whole-n8n-workflow.png) | Complete n8n workflow with all nodes |
| ![API Test](screenshots/Screenshot%20API-endpoint-test-via-swagger.png) | API endpoint test in Swagger UI |

### 2. n8n Integration & Logging
| | Description |
|---|-------------|
| ![HTTP Request](screenshots/Screenshot%20HTTP%20Request%20Node%20request%20response.png) | n8n HTTP Request node with request/response |
| ![Logging Overview](screenshots/Screenshot%20logs%20are%20stored%20in%20google%20sheets.png) | Google Sheets logging overview |

### 3. Success Path - Auto-Approved Post
| | Description |
|---|-------------|
| ![Approved Workflow](screenshots/Screenshot%20Approved-linkedIn-post-n8n-workflow-and-logged.png) | Successful workflow execution with all green nodes |
| ![Activity Logs](screenshots/Screenshot%20Linkedin%20Post%20Activity%20Logs.png) | LinkedIn Post Activity Log in Google Sheets |
| ![Live Post](screenshots/Screenshot%20Linkedin%20live-automation-post.png) | Live LinkedIn post published to the platform |

### 4. Human Approval Flow
| | Description |
|---|-------------|
| ![Slack Notification](screenshots/Screenshot%20linkedIn%20post-human-appr...message-review-notification-via-Slack.png) | Slack notification for human review |
| ![Approval Form](screenshots/Screenshot%20human-approval-form.png) | Slack approval form with Approve/Revise/Reject options |

### 5. Revision Flow
| | Description |
|---|-------------|
| ![Revision Workflow](screenshots/Screenshot%20linkedIn%20post-revise-n8n-workflow.png) | Revision workflow execution |
| ![Revision Success](screenshots/Screenshot%20content-revise-n8n-workflow-succesful-and-logged.png) | Successful revision with logging |
| ![Revision Logs](screenshots/Screenshot%20Revision%20Request%20Logs.png) | Revision Request Logs in Google Sheets |
| ![Revision Limit](screenshots/Screenshot%20Revise-limit-reach-reject-automatically-and-logged.png) | Auto-reject when revision limit is reached |

### 6. Reject Flow
| | Description |
|---|-------------|
| ![Reject Flow](screenshots/Screenshot%20human-reject-content-flow-and-logged.png) | Rejected post workflow |
| ![Rejection Logs](screenshots/Screenshot%20Human%20Rejection%20Logs.png) | Human Rejection Logs in Google Sheets |

### 7. Error Handling
| | Description |
|---|-------------|
| ![Error Alert](screenshots/Screenshot%20error-alert-n8n-workflow.png) | Error Alert node triggered in n8n |
| ![Slack Error](screenshots/Screenshot%20error-message-received-on-Slack.png) | Slack error alert in #alerts channel |
| ![Error Logs](screenshots/Screenshot%20Response%20Error%20Logs.png) | Error logs in Google Sheets |