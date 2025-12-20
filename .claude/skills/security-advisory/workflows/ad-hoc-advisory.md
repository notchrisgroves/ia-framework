# Ad-Hoc Advisory Workflow

**Mode 2: Quick security guidance and best practices**

---

## Advisory Approach

**Response Pattern:**
1. Understand the question/scenario
2. Research if needed (WebSearch for latest best practices)
3. Provide clear, actionable guidance
4. Include references/sources
5. Suggest follow-up if complex

**Common Advisory Topics:**
- Security architecture decisions
- Tool selection and evaluation
- Threat intelligence and analysis
- Compliance requirements
- Policy development
- Incident response guidance
- Security best practices
- Technology security assessment

**Output Directory:** `output/engagements/ad-hoc-advisory/[YYYY-MM-DD]-[topic-slug]/`

---

## Output Structure (MANDATORY Documentation)

Auto-create session directory with professional documentation:

```
[YYYY-MM-DD]-[topic-slug]/
├── request.md              # Original question/scenario (Required)
├── research.md             # OSINT/threat intel performed (Required)
├── recommendations.md      # Primary guidance provided (Required)
├── references.md           # Sources and citations (Required)
└── action-items.md         # Next steps (Optional)
```

---

## File Descriptions

### 1. request.md (Required)
- Capture original question and context
- Document stakeholders and constraints
- Define success criteria
- Include: Date, requestor name/title, organization

### 2. research.md (Required)
- Document threat intelligence gathered
- Best practices and standards reviewed
- Competitive analysis performed
- Multi-location reference search results

### 3. recommendations.md (Required)
- Primary recommendation with rationale
- Alternative approaches
- Implementation guidance
- Risk considerations
- Resource requirements

### 4. references.md (Required)
- Framework citations (NIST, CIS, ISO, OWASP)
- Threat reports and advisories
- Industry research and whitepapers
- Technical documentation

### 5. action-items.md (Optional)
- Immediate actions (0-7 days)
- Short-term tasks (1-30 days)
- Long-term considerations (90+ days)
- Follow-up meetings

---

## Benefits

**Professional audit trail for all guidance provided (Critical Rule #2):**
- Client deliverable for stakeholder sharing
- Searchable knowledge base for future reference
- Continuity for follow-up engagements
- Billing support for consulting work
- Compliance with professional documentation standards

---

## Template

**Use `output/engagements/ad-hoc-advisory/_TEMPLATE/` as starting point**

---

**See Also:**
- `../reference/README.md` - Multi-location reference search pattern
- `../templates/README.md` - Policy templates library
- `risk-assessment.md` - Formal assessment workflow
