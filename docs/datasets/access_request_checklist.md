# Official dataset access checklist

Status 2026-09-12: no authorized SCface or AgeDB access is available. This is a preparation checklist only; no request has been sent or agreement signed by the assistant. FEI is already complete and is the first additional dataset beyond MOBIO/LFW.

## SCface: primary next dataset

Official [dataset page](https://www.scface.org/) and [release agreement](https://www.scface.org/SCface_release_agreement.pdf). Recheck the current agreement and contact details before sending.

- [ ] Sani confirms dataset scope and the responsible institution.
- [ ] A full-time staff member prepares an institutional-letterhead cover letter and signs the release agreement. A student signature is insufficient.
- [ ] State the non-commercial research question, institution, named collaborators, intended storage/processing machines, and requested duration.
- [ ] Ask explicitly whether the agreement permits each collaborator, cross-institution access, local processing and aggregate/derived-result publication. Do not assume one person's permission covers the whole team.
- [ ] Submit via the official contact and retain the approval privately. Do not put signatures or personal contact details in Git.
- [ ] Download only after approval; record archive hashes privately and prohibit redistribution. Keep all face photographs out of this project's slides unless separate permission is verified.

## AgeDB: contingency

Official [iBUG dataset page](https://ibug.doc.ic.ac.uk/resources/agedb/). Use its current maintainer contact; do not use third-party archive passwords.

- [ ] Confirm academic affiliation, non-commercial purpose and collaborator/site scope.
- [ ] Request authorized archive access by academic email, explaining identity-disjoint leakage evaluation and publication of aggregate statistics only.
- [ ] Clarify the restrictions on annotations, derived data, collaborators and publication before processing or sharing.
- [ ] Receive and store the password privately. Type secrets directly into the local terminal when needed, never into assistant chat or Git.
- [ ] Download from the official authorized source and hash locally.

## Acceptance after access

- [ ] Freeze image selection and identity splits before attack results are inspected.
- [ ] Require a held-out gallery image plus at least ten valid source embeddings per included identity; publish aggregate eligibility and detector-failure counts.
- [ ] Audit duplicates, identities, key separation and authorized storage.
- [ ] Validate unprotected ArcFace signal before attributing low attack performance to protection.
- [ ] Record demographic/capture limitations and possible face-model training overlap. AgeDB celebrity overlap is unresolved.
- [ ] Obtain a new compute authorization and freeze the pilot protocol. Access alone does not authorize the full confirmation matrix.

See the [source review](candidate_selection_2026-09-10.md) for dataset facts and limitations. Do not bypass unavailable access with mirrors or borrowed credentials.