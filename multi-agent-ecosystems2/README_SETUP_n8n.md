# Setting Up n8n for Class

## What You Need

By the end of this setup, you'll have **n8n** running on your own machine and ready for next week's class.

**Estimated setup time:** 10–15 minutes.

---

# Step 1: Install Docker

Docker is required to run n8n.

## Check if Docker Is Already Installed

Open a terminal and run:

```bash
docker --version
```

If you see a version number, Docker is already installed and you can **skip to Step 2**.

---

## If Docker Is Not Installed

### Windows

1. Download Docker Desktop from:
   - https://www.docker.com/products/docker-desktop
2. Run the installer using the default settings.
3. Restart your computer when prompted.
4. Launch **Docker Desktop** from the Start menu.
5. Wait for the Docker whale icon to stop animating before continuing.

### macOS

1. Download Docker Desktop from:
   - https://www.docker.com/products/docker-desktop
2. Open the downloaded `.dmg` file.
3. Drag Docker into your **Applications** folder.
4. Launch Docker from Applications.
5. Wait for the Docker whale icon to stop animating before continuing.

---

# Step 2: Run n8n

Copy and paste the following command into your terminal (PowerShell, Terminal, or Linux shell):

```bash
docker run -d --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  -e N8N_BLOCK_ENV_ACCESS_IN_NODE=false \
  -e AZURE_OPENAI_API_KEY="REPLACE_WITH_YOUR_KEY" \
  -e AZURE_CHAT_ENDPOINT="REPLACE_WITH_YOUR_ENDPOINT" \
  -e AZURE_OPENAI_LLM_DEPLOYMENT="REPLACE_WITH_YOUR_DEPLOYMENT" \
  -e AZURE_OPENAI_API_VERSION="REPLACE_WITH_YOUR_API_VERSION" \
  --restart unless-stopped \
  n8nio/n8n
```

> **Important:** Replace the placeholder values with your actual Azure OpenAI credentials.

> **Note:** Your credentials will be provided during class. Until then, you can leave the placeholder values in place and still verify that n8n is running correctly.

Wait approximately **30 seconds** for n8n to start.

---

# Step 3: Verify n8n Is Working

## 3.1 Open n8n

Open your browser and go to:

```
http://localhost:5678
```
Note: if there already container running: ```docker rm -f n8n```
You should see the **n8n welcome screen**.

---

## 3.2 Create Your n8n Account

Fill out the registration form:

- **Email:** Any email address (used only for your local installation)
- **First Name:** Your first name
- **Last Name:** Your last name
- **Password:** Create a password you'll use to log in locally

---

## 3.3 Test with a Simple Workflow

### Step 1

Click **Create Workflow**.

### Step 2

Click the **+** button to add a node.

### Step 3

Search for **Set** and select **Edit Fields (Set)**.

### Step 4

Click:

**Add Field → String**

### Step 5

Enter the following values:

| Field | Value |
|--------|-------|
| Name | `message` |
| Value | `n8n is working!` |

### Step 6

Click **Execute Node**.

### Step 7

Check the output. You should see:

```text
message: "n8n is working!"
```

---

# ✅ Success! You're Ready for Class

You now have **n8n** running locally and your Azure credentials are ready to be configured and used during class.

---

# Start and Stop n8n

| Action | Command |
|---------|---------|
| Start n8n (before class) | `docker start n8n` |
| Stop n8n (after class) | `docker stop n8n` |
| Check if running | `docker ps \| grep n8n` |

> **Tip:** n8n uses virtually no resources when stopped. Running `docker stop n8n` after class will free up system memory and CPU.

---

# Troubleshooting

| Issue | Solution |
|------|----------|
| Port 5678 already in use | Change `-p 5678:5678` to `-p 5679:5678` and access `http://localhost:5679` instead. |
| `docker: command not found` | Docker isn't installed. Return to **Step 1** and install Docker Desktop. |
| Docker Desktop isn't running | Launch Docker Desktop and wait for the whale icon to finish starting. |
| Can't access `http://localhost:5678` | Wait 30 seconds for n8n to finish starting, then refresh your browser. |
| Container has stopped | Restart it with `docker start n8n`. |

---

# Need Help?

If you get stuck, reach out before class.

We'll also have time during class to help troubleshoot any setup issues.