import streamlit as st

st.set_page_config(
    page_title="Deal Workshop Scorecard",
    page_icon="🎯",
    layout="wide",
)

PUSHBACK_QUESTIONS = {
    "Problem Conviction": [
        "What happens if this problem remains unsolved for another six months?",
        "How is the current situation affecting your team’s goals, KPIs, customers, or revenue today?",
        "What is the financial, operational, or personal cost of doing nothing?",
        "What would have to change for this to become a genuine priority?",
    ],
    "Evaluation Clarity": [
        "What does success look like in concrete, measurable terms?",
        "How will you decide whether this initiative delivered value 90 days after implementation?",
        "Which evaluation criteria are non-negotiable, and which are simply nice to have?",
        "Who else will influence the decision, and what does each person need to see?",
    ],
    "Outcome Confidence": [
        "What would need to be true for you to feel fully confident moving forward?",
        "What is the biggest risk you see in choosing a solution, and how could we reduce it?",
        "Would a pilot, phased rollout, or proof of concept make the decision safer?",
        "What evidence—customer references, data, implementation plan, or guarantee—would build confidence?",
    ],
    "Organizational Readiness": [
        "Which internal stakeholders must align before this can move ahead?",
        "What needs to happen internally for the rollout to succeed?",
        "Are budget, resources, ownership, and executive sponsorship in place?",
        "What is the decision timeline, and what could realistically delay it?",
    ],
}

DIMENSIONS = [
    (
        "Problem Conviction",
        "How strongly does the buyer believe the current problem is urgent and worth solving?",
    ),
    (
        "Evaluation Clarity",
        "How clear is the buyer on success criteria and how they will evaluate options?",
    ),
    (
        "Outcome Confidence",
        "How confident is the buyer that a solution can produce the outcome they want?",
    ),
    (
        "Organizational Readiness",
        "Is the organization able and prepared to make, implement, and sustain the change?",
    ),
]

st.title("🎯 Deal Workshop Scorecard")
st.write(
    "Score buyer readiness across four dimensions, reveal the gaps, and use the "
    "scripted questions to challenge a stalled deal constructively."
)

st.info(
    "Score each dimension from 1 to 10. A score of 1 means there is little evidence "
    "of readiness; 10 means the buyer has clear, demonstrated readiness."
)

scores = {}

for dimension, description in DIMENSIONS:
    st.subheader(dimension)
    st.caption(description)

    scores[dimension] = st.slider(
        f"{dimension} score",
        min_value=1,
        max_value=10,
        value=5,
        key=dimension,
    )

    if scores[dimension] <= 6:
        st.warning(f"Gap identified: {dimension} is {scores[dimension]}/10.")
        st.markdown("**Scripted push-back questions**")
        for question in PUSHBACK_QUESTIONS[dimension]:
            st.markdown(f'- “{question}”')

    st.divider()

st.header("📊 Scoring and Recommendation")

problem = scores["Problem Conviction"]
evaluation = scores["Evaluation Clarity"]
outcome = scores["Outcome Confidence"]
organization = scores["Organizational Readiness"]

average_score = sum(scores.values()) / len(scores)

# A high value represents a meaningful barrier to moving forward.
status_quo_preference = 10 - problem
fomu = 10 - outcome
decision_readiness_gap = 10 - min(evaluation, organization)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Average readiness", f"{average_score:.1f}/10")
col2.metric("Status quo preference", f"{status_quo_preference}/10")
col3.metric("FOMU", f"{fomu}/10")
col4.metric("Decision-readiness gap", f"{decision_readiness_gap}/10")

st.caption(
    "Status quo preference rises when Problem Conviction is low. "
    "FOMU (fear of messing up) rises when Outcome Confidence is low. "
    "Decision readiness reflects unclear evaluation or weak organizational ability to act."
)

st.subheader("What the gaps mean")

if status_quo_preference > fomu:
    st.write(
        "The larger obstacle is **status quo preference**: the buyer is more comfortable "
        "with inaction than with changing. Rebuild urgency using the cost, risk, and "
        "consequences of staying where they are."
    )
elif fomu > status_quo_preference:
    st.write(
        "The larger obstacle is **FOMU**: the buyer may see the problem but fears making "
        "a poor decision. De-risk the path with proof, references, a pilot, a phased plan, "
        "and a clear implementation approach."
    )
else:
    st.write(
        "Status quo preference and FOMU are equally important. Address both the cost of "
        "inaction and the safety of taking action."
    )

st.subheader("Recommendation")

lowest_dimension = min(scores, key=scores.get)
lowest_score = scores[lowest_dimension]

if min(scores.values()) <= 3 or average_score < 4.5:
    st.error(
        f"**KILL / PARK THE DEAL.** The buyer is not ready enough for an active sales pursuit. "
        f"The biggest gap is {lowest_dimension} ({lowest_score}/10). Agree a re-entry trigger, "
        f"then move the opportunity to nurture rather than continuing to spend active selling time."
    )
elif average_score < 6.5 or min(scores.values()) <= 5:
    st.warning(
        f"**NURTURE WITH A SPECIFIC PLAN.** Do not forecast this as near-term. "
        f"Prioritize the biggest gap—{lowest_dimension} ({lowest_score}/10)—and use the questions "
        f"above to earn evidence of change before advancing the deal."
    )
elif average_score < 8 or min(scores.values()) <= 6:
    st.info(
        f"**ACTIVE NURTURE / QUALIFY FURTHER.** There is potential, but the deal has a meaningful "
        f"gap in {lowest_dimension} ({lowest_score}/10). Set a clear mutual next step that closes it "
        f"before treating the opportunity as commit-worthy."
    )
else:
    st.success(
        "**PURSUE.** Buyer readiness is consistently strong. Confirm the decision process, commercial "
        "path, stakeholders, and mutual action plan—then progress the deal actively."
    )

st.subheader("Quick rubric")
st.markdown(
    """
- **Pursue:** Average is at least 8 and every dimension is at least 7.
- **Active nurture / qualify further:** Average is 6.5–7.9, or one dimension is 6.
- **Nurture with a plan:** Average is 4.5–6.4, or any dimension is 4–5.
- **Kill / park:** Average is below 4.5, or any dimension is 1–3.
"""
)

st.caption(
    "This is a coaching and qualification aid, not a substitute for evidence. "
    "Score from observable buyer behavior, not optimistic assumptions."
)
