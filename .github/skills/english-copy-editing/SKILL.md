---
name: english-copy-editing
description: Write and edit a CV in clear, idiomatic professional English while preserving the candidate's verified facts.
---

# Professional English copy editing

Apply this skill when the job advertisement is primarily in English.

## Editing workflow

1. Read the job advertisement and source profile before revising the summary, experience descriptions, or CV labels.
2. Use concise, natural professional English. Avoid literal translations, inflated claims, filler, unexplained jargon, repetition, and overly long sentences.
3. Correct grammar, syntax, spelling, tense, punctuation, and consistency. Follow the spelling convention used by the advertisement (British or American); if unclear, use consistent international English.
4. Choose precise action verbs supported by the source profile. Preserve verified job titles, dates, qualifications, tools, and responsibilities.
5. Improve readability without adding achievements, metrics, responsibilities, or proficiency levels that the source does not support.
6. Use consistent English for visible template labels and prose. Keep official company and technology names unchanged.
7. Never add a generation date, automated signature, or a parenthetical label such as “(target role)” or “(position sought)”.
8. Make the headline a natural professional title, not an awkward concatenation of the candidate's current and target roles. Keep the target title concise and let the summary explain the candidate's background.

## Summary: soft skills and interest in the role

- Lead with one or two role-relevant, evidence-backed soft skills, then express the candidate's personal motivation if they supplied or confirmed it. Use hard skills as supporting evidence rather than turning the summary into a technical inventory.
- Compare the employer's requested qualities with the candidate's explicit statements and concrete actions in the profile. Job requirements and public research about the employer provide context; they do not prove qualities about the candidate.
- Do not infer leadership, communication, organization, adaptability, or motivation from a job title, technology, or hobby. If evidence is missing, ask the user which qualities they want to emphasize and what attracts them to the role; wait for confirmation before including those claims.
- If the user does not provide a motivation, keep the summary factual and tell the orchestrator that personal motivation could not be established.

## Scenario: tailor a DevOps experience to an English offer

Given source facts such as “Created CI/CD models. Automated business processes. Set up observability standards,” produce concise and grammatical text while preserving the same claims, for example:

> Built CI/CD templates, automated business processes, and helped establish observability standards.

Do not add quantified impact, tools, or leadership claims unless the profile provides evidence.

## Output

Edit text fields in `.cv-work/cv_profile.json` and visible interface text in `.cv-work/cv_template.html`. Tell the HTML Builder when the files are ready to render and summarize material editorial decisions.
