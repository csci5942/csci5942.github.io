---
title: "Logistics"
permalink: /logistics/
toc: true
toc_label: "On this page"
toc_sticky: true
---

This page summarizes the course syllabus (version of August 12, 2026). Where the
two disagree, the syllabus governs.

## Communication

**This website is the source of truth for the schedule and readings.**

- **Slack** &mdash; announcements and discussion.
- **GitHub** &mdash; assignments are released in the course GitHub organization with starter code.
- **Gradescope** &mdash; assignment submission.

## Prerequisites

CSCI 4622, CSCI 4922.

## Course Structure

### Lectures and Readings

Each lecture has one required paper and possibly a short list of optional ones.
Please spend some time with the required reading before class.

### Participation (Round Robin)

Discussion is Socratic and round robin: one or two students are "on deck" each
meeting and lead the response to discussion questions. Being on deck is scheduled
about one lecture in advance. The questions rarely have a single right answer,
and grading rewards engaged reasoning, not correctness.

### Assignments

Seven graded assignments, roughly biweekly, released on GitHub with
skeleton/starter code. The assignments are constructive: each produces an
artifact (a trained model, an eval harness, a data pipeline) that later lectures
and assignments build on.

| | Assignment |
| :--- | :--- |
| **A0** | Environment setup and Google Cloud credit signup. A1 requires it. |
| **A1** | A decoder-only Transformer from scratch, on Shakespeare, plus a small scaling study. |
| **A2** | Evaluation harness and tracing (Opik) for the A1 model. |
| **A3** | Spark, data lakes, and dataloaders. |
| **A4** | Multi-system training. |
| **A5** | Supervised fine-tuning and PEFT. |
| **A6** | Inference optimizations. |
| **A7** | RLAIF. |

### Quizzes

Each assignment is followed by a short, closed-book, in-class quiz on the
material of that assignment. If you did the assignment yourself, the quiz is
straightforward. Quizzes are written by both instructors and account for 3 of
each assignment's 7 points.

### Mega Assignment (group project)

A semester-long group build in place of an eighth assignment, on a topic you
propose. Deliverables:

- **Concept document (5 pts)** &mdash; what you will build, on what data and compute, and how you will know it worked.
- **Pitch day (5 pts)** &mdash; a short presentation and defense of the plan.
- **Final submission (10 pts)** &mdash; code, README, and results, presented at the poster session on Thursday, December 3.

### Final Exam

In person, written, during the scheduled final slot (Wednesday, December 9).

## Grading

| Component | Points |
| :--- | ---: |
| Assignments (A0 1 pt, then 7 assignments &times; 7 pts; 4 for the assignment, 3 for its quiz) | 50 |
| Participation (round robin) | 10 |
| Mega assignment (5 concept + 5 pitch + 10 final) | 20 |
| Final exam | 20 |

## Late Policy

Each assignment may be submitted up to **two days late without penalty**; beyond
that, 25% per additional day. You only have **five late days** to use through the
semester. Late days are calculated automatically based on submission time.

## Computing

Every assignment runs on hardware you have or credits you are given:

- Google Cloud credits (signup in week 1).
- Course allocations on Chameleon and NSF ACCESS, both with high-bandwidth-memory nodes.
- The course Slurm cluster (4 &times; RTX 8000, 48 GB each), coming online at the end of August.

Where a topic needs frontier-scale numbers, we read the papers of the people who
paid for them. The mega assignment includes deciding, and defending, your own
compute plan.

## Honor Code

All students enrolled in a CU-Boulder course are responsible for knowing and
adhering to the [Honor Code](https://www.colorado.edu/sccr/honor-code).
Violations may include but are not limited to: plagiarism (including use of paper
writing services or technology such as essay bots), cheating, fabrication, lying,
bribery, threat, unauthorized access to academic materials, clicker fraud,
submitting the same or similar work in more than one course without permission
from all course instructors involved, and aiding academic dishonesty.
Understanding the course's syllabus is a vital part of adhering to the Honor
Code. All incidents of academic misconduct will be reported to Student Conduct
&amp; Conflict Resolution.

In this course, please respect the following specific policies:

- **AI Tools:** AI usage is permitted, treated as if the AI were a colleague: you
  may consult it, delegate to it, and learn from it, and you are responsible for
  your work, including its correctness and your understanding of it. The in-class
  quizzes and the in-person final exist so that understanding is checked in
  person. For the mega assignment, AI use is expected; document it as you would
  any collaborator.
- **Collaboration:** Study groups are allowed and encouraged. Each student submits
  their own assignment work and lists study-group members at the top of the
  submission.
- **Quizzes and exam:** Closed book, no devices, no AI.

## Accommodation for Disabilities, Temporary Medical Conditions, and Medical Isolation

If you qualify for accommodations because of a disability, please submit your
accommodation letter from [Disability Services](https://www.colorado.edu/disabilityservices/)
to your faculty member in a timely manner so that your needs can be addressed. If
you have a temporary illness, injury, or required medical isolation for which you
require adjustment, please email me before class starts, ideally the day before.
I cannot accommodate explanations after the fact for the purpose of allocating
your participation. Your email should not include any details but merely state
that you cannot attend due to medical reasons.

## Accommodation for Religious Obligations

Campus policy requires faculty to provide reasonable accommodations for students
who, because of religious obligations, have conflicts with scheduled exams,
assignments, or required attendance. Please provide me notice of the need for a
religious accommodation within the first two weeks of class.

## Preferred Student Names and Pronouns

CU Boulder recognizes that students' legal information does not always align with
how they identify. If you wish to have your preferred name and/or preferred
pronouns appear on your instructors' class rosters and in Canvas, visit the
[Registrar's website](https://www.colorado.edu/registrar/) for instructions.

## Classroom Behavior

Students and faculty are responsible for maintaining an appropriate learning
environment in all instructional settings. Professional courtesy and sensitivity
are especially important with respect to individuals and topics dealing with
race, color, national origin, sex, pregnancy, age, disability, creed, religion,
sexual orientation, gender identity, gender expression, veteran status, marital
status, political affiliation, or political philosophy.

## Sexual Misconduct, Discrimination, Harassment and/or Related Retaliation

CU Boulder is committed to fostering an inclusive and welcoming learning,
working, and living environment. University policy prohibits protected-class
discrimination and harassment, sexual misconduct, intimate partner abuse,
stalking, and related retaliation. Faculty are required to inform the Office of
Institutional Equity and Compliance (OIEC) when they are made aware of incidents
related to these concerns.

## Mental Health and Wellness

If you are struggling with personal stressors, mental health or substance use
concerns that are impacting academic or daily life, please contact Counseling and
Psychiatric Services (CAPS) at (303) 492-2277, 24/7.
