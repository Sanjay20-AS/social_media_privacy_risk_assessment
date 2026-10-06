# Security Checklist for a Production Version

This student version intentionally keeps the architecture simple. Before production deployment:

- [ ] Replace Flask development secret with a random environment secret.
- [ ] Disable Flask debug mode.
- [ ] Add CSRF protection.
- [ ] Add secure cookie flags.
- [ ] Add Content Security Policy and other security headers.
- [ ] Validate all form inputs server-side.
- [ ] Add rate limiting if authentication is introduced.
- [ ] Minimize and anonymize stored assessment data.
- [ ] Add a clear retention/deletion policy.
- [ ] Do not store passwords, private messages, or social-media credentials.
- [ ] Add automated dependency scanning.
- [ ] Run Bandit/Ruff and unit tests in CI.
- [ ] Add logging that excludes sensitive user inputs.
- [ ] Add accessibility testing.
- [ ] Conduct a privacy impact assessment before storing any user data.
