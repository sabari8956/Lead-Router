# Product Requirements Document (PRD)
## Real Estate Lead Management & SLA System

---

## 1. Overview
This system manages real estate leads from multiple sources, automatically assigns them to agents, enforces response-time SLAs, and provides full visibility to managers.

The platform is custom-built (no third-party automation tools) and fully owned end-to-end.

---

## 2. Goals
- Centralize all leads
- Prevent duplicate leads
- Auto-assign leads to agents
- Enforce SLA response times
- Track agent performance
- Give managers real-time visibility

---

## 3. User Roles

### Admin
- Configure SLA rules
- Configure assignment rules
- Manage agents and permissions

### Manager
- Monitor dashboards
- View SLA breaches
- Reassign leads
- Analyze performance

### Agent
- Receive leads
- Contact customers
- Update lead status
- Add notes

---

## 4. Lead Sources
- Facebook Lead Ads
- Bayut
- Property Finder
- Website forms
- WhatsApp
- Phone calls (manual entry)

All leads enter through a single ingestion point.

---

## 5. Application Flow

### Step 1: Lead Comes In
A lead arrives from any source with phone/email.

### Step 2: System Captures Lead
- Lead is stored instantly
- System checks for duplicates (phone/email)
- Duplicate → update existing lead
- New → create lead

### Step 3: Automatic Assignment
Lead is assigned based on:
- Language
- Area
- Availability
- Workload

SLA timer (e.g. 10 minutes) starts.

### Step 4: Agent Notification
Agent receives:
- Dashboard task
- WhatsApp/Slack alert
- SLA countdown

### Step 5: Agent Action
Agent:
- Contacts lead
- Updates status
- Adds notes

All actions are logged.

### Step 6: Outcomes
- Responded on time → SLA met
- Missed deadline → SLA breached, manager alerted
- Lead lost → reason captured

### Step 7: Manager Dashboard
Shows:
- New leads
- At-risk leads
- Breached leads
- Daily conversion stats

Managers can reassign leads and view full history.

---

## 6. Core Features
- Central inbox
- Deduplication
- Auto assignment
- SLA enforcement
- Notifications
- Audit logs
- Live dashboards

---

## 7. Success Metrics
- Faster response times
- Fewer SLA breaches
- Higher conversion rate
- Clear accountability

---

## 8. Out of Scope (Initial)
- Built-in calling
- Payments
- AI scoring

---

## 9. Tech Direction
- Custom backend & frontend
- Event-driven architecture
- Scalable and extensible
