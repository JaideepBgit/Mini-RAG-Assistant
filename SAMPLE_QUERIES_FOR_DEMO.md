# Sample Queries for Demo & Testing

## SINGLE-TURN QUERIES

### HR & Leave Policies

**Query 1: Vacation Leave**
```
What is the vacation leave policy?
```
Expected: Should return information about annual leave days, accrual, eligibility

**Query 2: Sick Leave**
```
How many sick days do employees get?
```
Expected: Should return sick leave allowance and usage rules

**Query 3: Leave Request Process**
```
How do I request time off?
```
Expected: Should explain the leave request procedure

**Query 4: Leave Approval**
```
Who approves vacation requests?
```
Expected: Should identify approval authority (manager, HR, etc.)

---

### Remote Work & Flexibility

**Query 5: Remote Work Policy**
```
What is the remote work policy?
```
Expected: Should return remote work eligibility and guidelines

**Query 6: Remote Work Eligibility**
```
Who is eligible for remote work?
```
Expected: Should specify eligibility criteria

**Query 7: Hybrid Schedule**
```
Can I work from home part-time?
```
Expected: Should discuss hybrid work arrangements

---

### Security & Compliance

**Query 8: Data Security**
```
What are the security requirements for handling client data?
```
Expected: Should return data protection and security policies

**Query 9: Password Policy**
```
What is the password policy?
```
Expected: Should explain password requirements and best practices

**Query 10: Confidentiality**
```
What are the confidentiality requirements?
```
Expected: Should discuss confidential information handling

---

### Expenses & Reimbursement

**Query 11: Expense Claims**
```
How do I submit expense claims?
```
Expected: Should explain expense reimbursement process

**Query 12: Reimbursable Expenses**
```
What expenses can I claim?
```
Expected: Should list eligible expenses

**Query 13: Expense Approval**
```
How long does expense approval take?
```
Expected: Should provide timeline for reimbursement

---

### Professional Development

**Query 14: Training Budget**
```
Is there a budget for professional development?
```
Expected: Should discuss training and development funding

**Query 15: Conference Attendance**
```
Can I attend conferences?
```
Expected: Should explain conference attendance policy

---

## MULTI-TURN CONVERSATION SEQUENCES

### Sequence 1: Vacation Leave Deep Dive

**Turn 1:**
```
What is the vacation leave policy?
```

**Turn 2:**
```
How do I request it?
```
(Tests: Does it understand "it" = vacation leave?)

**Turn 3:**
```
What if I need to cancel?
```
(Tests: Does it maintain context about vacation requests?)

**Turn 4:**
```
Can I carry them over to next year?
```
(Tests: Does it understand "them" = vacation days?)

---

### Sequence 2: Remote Work Exploration

**Turn 1:**
```
What is the remote work policy?
```

**Turn 2:**
```
Who is eligible for it?
```
(Tests: "it" = remote work)

**Turn 3:**
```
How do I apply?
```
(Tests: Implicit context - apply for remote work)

**Turn 4:**
```
What equipment will be provided?
```
(Tests: Context about remote work setup)

---

### Sequence 3: Security Requirements

**Turn 1:**
```
What are the security requirements for data handling?
```

**Turn 2:**
```
Who is responsible for enforcing them?
```
(Tests: "them" = security requirements)

**Turn 3:**
```
What happens if they are violated?
```
(Tests: "they" = security requirements)

---

### Sequence 4: Expense Reimbursement

**Turn 1:**
```
How do I submit expense claims?
```

**Turn 2:**
```
What documentation do I need for it?
```
(Tests: "it" = expense claims)

**Turn 3:**
```
How long does the approval take?
```
(Tests: Implicit context - expense approval)

---

### Sequence 5: Professional Development

**Turn 1:**
```
Is there a budget for professional development?
```

**Turn 2:**
```
How much is it?
```
(Tests: "it" = professional development budget)

**Turn 3:**
```
How do I request funding from it?
```
(Tests: "it" = the budget)

---

## EDGE CASE QUERIES

### Ambiguous Questions

**Query 16:**
```
What is the policy?
```
Expected: Should ask for clarification or provide general policy overview

**Query 17:**
```
Tell me about benefits
```
Expected: Should provide overview of employee benefits

---

### Out-of-Scope Questions

**Query 18:**
```
What is the weather today?
```
Expected: Should indicate information not available in documents

**Query 19:**
```
Who is the CEO?
```
Expected: May or may not be in documents - test graceful handling

---

### Complex Questions

**Query 20:**
```
Compare sick leave and vacation leave policies
```
Expected: Should synthesize information from multiple sources

**Query 21:**
```
What are all the leave types available?
```
Expected: Should aggregate information about different leave types

---

## QUERIES FOR HIGHLIGHTING DEMO

These queries work well for showing text highlighting:

**Query 22:**
```
What is the vacation leave accrual rate?
```
Expected: Should highlight "vacation leave" and "accrual" in sources

**Query 23:**
```
What are the password requirements?
```
Expected: Should highlight "password" and related security terms

**Query 24:**
```
How do I request remote work?
```
Expected: Should highlight "remote work" and "request" process

---

## QUERIES BY CONFIDENCE LEVEL

### High Confidence Expected (90-100%)

```
What is the vacation leave policy?
How many sick days do employees get?
What is the remote work policy?
```

### Medium Confidence Expected (70-89%)

```
Can I work from home part-time?
What expenses can I claim?
How long does expense approval take?
```

### Lower Confidence Expected (50-69%)

```
What is the policy for sabbatical leave?
Can I transfer to another department?
What is the dress code?
```
(These may not be in your documents)

---

## TESTING CHECKLIST

Use this to systematically test your system:

### Basic Functionality
- [ ] Single query returns answer
- [ ] Confidence score displayed (0-100%)
- [ ] Sources shown with relevance scores
- [ ] Source content expandable
- [ ] Document names visible

### Multi-Turn Context
- [ ] Enable multi-turn toggle
- [ ] Ask follow-up with pronoun ("it", "that", "them")
- [ ] Verify context is maintained
- [ ] Try 3-4 turns in sequence
- [ ] Disable toggle and verify independent queries

### Text Highlighting
- [ ] Expand source content
- [ ] Verify yellow highlights (exact matches)
- [ ] Verify green highlights (semantic matches)
- [ ] Check multiple sources

### Provider Switching
- [ ] Switch from OpenAI to Ollama (or vice versa)
- [ ] Ask same question
- [ ] Verify different vector store used
- [ ] Compare response quality

### Edge Cases
- [ ] Ask out-of-scope question
- [ ] Ask ambiguous question
- [ ] Ask very long question
- [ ] Ask question with typos

---

## DEMO SCRIPT QUERIES

For your 3-minute video, use these:

**Main Demo Query:**
```
What is the vacation leave policy?
```

**Multi-Turn Sequence:**
```
1. What is the vacation leave policy?
2. How do I request it?
3. What if I need to cancel?
```

**Alternative if time permits:**
```
What are the security requirements for data handling?
```

---

## INTERVIEW PREPARATION QUERIES

If asked to demo live in interview, have these ready:

**Safe Queries (guaranteed to work):**
- "What is the vacation leave policy?"
- "How many sick days do employees get?"
- "What is the remote work policy?"

**Impressive Queries (show advanced features):**
- Multi-turn sequence about vacation leave
- Complex query: "Compare sick leave and vacation leave"
- Edge case: "What is the weather today?" (shows graceful handling)

---

## QUERY VARIATIONS

Same question, different phrasings (test robustness):

**Vacation Leave:**
- "What is the vacation leave policy?"
- "Tell me about vacation days"
- "How much vacation time do I get?"
- "What's the PTO policy?"
- "How many days off can I take?"

**Remote Work:**
- "What is the remote work policy?"
- "Can I work from home?"
- "What's the WFH policy?"
- "Is remote work allowed?"
- "Tell me about telecommuting"

---

## PERFORMANCE BENCHMARKS

Track these metrics during testing:

| Metric | Target | Your Result |
|--------|--------|-------------|
| Response Time (OpenAI) | 2-5 sec | ___ sec |
| Response Time (Ollama) | 5-10 sec | ___ sec |
| Confidence Score (avg) | >70% | ___% |
| Relevance Score (avg) | >80% | ___% |
| Multi-turn Success | 100% | ___% |

---

## TROUBLESHOOTING QUERIES

If something seems wrong, test with these:

**Test Retrieval:**
```
vacation
```
(Single word - should still retrieve relevant docs)

**Test Generation:**
```
What is in the documents?
```
(Should provide overview)

**Test Confidence:**
```
What is the company's mission statement?
```
(Likely not in docs - should have low confidence)

---

## FINAL TIPS

### For Demo Video:
- Use **Query 1** (vacation leave) for main demo
- Use **Sequence 1** for multi-turn demo
- Keep queries simple and clear
- Avoid queries that might fail

### For Live Demo:
- Have 3-4 backup queries ready
- Test all queries before demo
- Know which queries show highlighting well
- Have edge case query ready if asked

### For Testing:
- Test all single-turn queries first
- Then test multi-turn sequences
- Test edge cases last
- Document any failures for discussion

---

Good luck! These queries should cover all your demo and testing needs. 🎯
