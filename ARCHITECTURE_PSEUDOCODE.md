# Architecture & Pseudocode
## Real Estate Lead Management System

---

## 1. System Model
The system is event-driven and reacts to:
- Lead arrival
- Agent actions
- Time passing (SLA)
- Manager actions

---

## 2. Lead Entry

```pseudo
EVENT LeadReceived(inputLead)
```

```pseudo
IF inputLead.phone IS NULL AND inputLead.email IS NULL
    REJECT lead
    EXIT
END IF
```

---

## 3. Normalize Data

```pseudo
lead.name = sanitize(inputLead.name)
lead.phone = normalizePhone(inputLead.phone)
lead.email = normalizeEmail(inputLead.email)
lead.source = inputLead.source
lead.area = inputLead.area
lead.language = inputLead.language
lead.created_at = NOW
```

---

## 4. Duplicate Check

```pseudo
existingLead = FIND Lead WHERE phone == lead.phone OR email == lead.email
```

```pseudo
IF existingLead EXISTS
    LOG duplicate event
    UPDATE existingLead.last_activity
    EXIT
END IF
```

---

## 5. Create Lead

```pseudo
lead.status = NEW
lead.sla_status = PENDING
SAVE lead
CALL AssignLead(lead)
```

---

## 6. Assignment Engine

```pseudo
agents = FIND Agents WHERE
    language MATCHES lead.language
    AND area MATCHES lead.area
    AND availability == ONLINE
```

```pseudo
IF agents IS EMPTY
    NOTIFY manager
    EXIT
END IF
```

```pseudo
agent = agents ORDER BY active_leads ASC LIMIT 1
lead.assigned_agent_id = agent.id
lead.assigned_at = NOW
lead.status = ASSIGNED
agent.active_leads += 1
SAVE lead, agent
```

---

## 7. SLA Timer

```pseudo
lead.sla_deadline = NOW + SLA_DURATION
lead.sla_status = RUNNING
SAVE lead
NOTIFY agent
```

---

## 8. SLA Monitor (Background Job)

```pseudo
CRON every 1 minute:
    FOR lead IN Leads WHERE sla_status == RUNNING
        IF NOW > lead.sla_deadline
            CALL HandleSLABreach(lead)
        ELSE IF time_left < RISK_THRESHOLD
            NOTIFY agent (at risk)
        END IF
    END FOR
```

---

## 9. SLA Breach

```pseudo
FUNCTION HandleSLABreach(lead)
    lead.sla_status = BREACHED
    lead.status = SLA_BREACHED
    SAVE lead
    NOTIFY manager
END FUNCTION
```

---

## 10. Agent Actions

```pseudo
EVENT AgentUpdatesLead(lead, action)
```

```pseudo
IF action == CONTACTED
    lead.contacted_at = NOW
    IF NOW <= lead.sla_deadline
        lead.sla_status = MET
    ELSE
        lead.sla_status = BREACHED
    END IF
    lead.status = CONTACTED
END IF
```

```pseudo
IF action == LOST
    lead.status = LOST
    lead.loss_reason = reason
END IF
```

```pseudo
SAVE lead
LOG event
```

---

## 11. Manager Actions

```pseudo
EVENT ManagerReassignLead(lead, newAgent)
    UPDATE agent loads
    RESET SLA
    SAVE all
```

---

## 12. Dashboard Queries

```pseudo
NewLeads = Leads WHERE status == NEW
AtRisk = Leads WHERE sla_status == AT_RISK
Breached = Leads WHERE sla_status == BREACHED
```

```pseudo
AgentPerformance =
    GROUP BY agent
    CALCULATE avg_response_time, breaches
```

---

## 13. Edge Cases
- No agents available
- Duplicate during SLA
- Agent offline
- Manual override
- Late response

---

## Summary
This document defines the full logical flow, decisions, and SLA handling required to implement the system.
