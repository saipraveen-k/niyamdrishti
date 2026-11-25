# Security Testing

## Short Explanation

Automated security testing currently consists of `pip-audit` dependency vulnerability scanning in CI on the `main` branch; dedicated security test suites for RBAC bypass, file upload attacks, SQL/XSS injection, and prompt injection remain to be written.

---

## 1. Current Security Checks

- **CI Dependency Vulnerability Scan (`.github/workflows/ci.yml`)**:
  - Runs on `refs/heads/main` via `pip-audit -r requirements.txt --ignore-vuln GHSA-wfm5-x5h8-xm93`.
- **Upload Magic-Byte Validation (Code-Inspected, Not Unit-Tested)**:
  - `validate_upload()` in `backend/app/modules/documents/service.py` checks file size, MIME allowlist, and binary magic headers (`%PDF`, `PK\x03\x04`, JPEG, PNG, WebP).

---

## 2. Recommended Security Test Cases (Backlog)

1. **RBAC Enforcement**: Verify `student` tokens receive `403` on `/admin/*`, `/documents/upload`, `/reviews/*`, and `POST /policy-comparisons`.
2. **Upload Spoofing**: Verify `.exe` or `.html` files renamed to `.pdf` with `application/pdf` header are rejected with `422`.
3. **Cross-User Isolation**: Verify Student A cannot modify Student B's `StudentApplication` (`PATCH /applications/{id}` filters by `student_id`) or read Student B's `StudentProfile`.
4. **Supabase RLS Verification**: Once SQL RLS policies are committed, test cross-tenant isolation directly against PostgreSQL.
5. **Prompt Injection**: Test `OpenAIProvider.extract_structured()` and `/assistant/chat` against adversarial document text.

---

## Related Documentation

- [Security](../04-technical/SECURITY.md)
- [CI/CD Pipeline](../09-deployment-and-devops/CI_CD_PIPELINE.md)
- [Testing Strategy](TESTING_STRATEGY.md)

