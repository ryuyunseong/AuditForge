# Report Template Examples

These examples show how AuditForge report wording can be adapted for English and Korean audiences.

All values are fake. Do not copy customer names, private URLs, credentials, tokens, cookies, IP addresses, or confidential evidence into public templates.

These are wording examples only. AuditForge does not include a full template engine yet.

## English Examples

### Finding Title

```text
SQL Injection in Product Search
```

### Evidence Wording

```text
The assessment team submitted a controlled SQL injection test string to https://app.example.test/search.
The response returned fake product records that should require authenticated filtering.
```

### Impact

```text
An attacker may be able to read or modify application data if untrusted input is passed to database queries without parameterization.
```

### Recommendation

```text
Use parameterized queries for all database access paths. Add server-side validation and regression tests for search, filtering, and sorting inputs.
```

## Korean Examples

### Finding Title

```text
상품 검색 기능의 SQL Injection 취약점
```

### Evidence Wording

```text
평가팀은 https://app.example.test/search 경로에 통제된 SQL Injection 테스트 문자열을 입력했습니다.
응답에는 인증된 필터링이 적용되어야 하는 가짜 상품 레코드가 반환되었습니다.
```

### Impact

```text
신뢰할 수 없는 입력값이 파라미터화 없이 데이터베이스 쿼리에 전달되면 공격자가 애플리케이션 데이터를 조회하거나 변경할 수 있습니다.
```

### Recommendation

```text
모든 데이터베이스 접근 경로에 파라미터화된 쿼리를 사용하세요. 검색, 필터링, 정렬 입력값에 대한 서버 측 검증과 회귀 테스트를 추가하세요.
```

## Sample Finding Wording Table

| Field | English | Korean |
| --- | --- | --- |
| Title | Missing Security Headers | 보안 헤더 누락 |
| Evidence | The fake test endpoint did not include Content-Security-Policy or X-Frame-Options headers. | 가짜 테스트 엔드포인트 응답에 Content-Security-Policy 또는 X-Frame-Options 헤더가 포함되어 있지 않았습니다. |
| Impact | Missing browser security headers can increase the impact of clickjacking or script injection attempts. | 브라우저 보안 헤더가 누락되면 클릭재킹 또는 스크립트 삽입 시도의 영향이 커질 수 있습니다. |
| Recommendation | Add a baseline Content-Security-Policy and configure frame-ancestors or X-Frame-Options. | 기본 Content-Security-Policy를 추가하고 frame-ancestors 또는 X-Frame-Options를 설정하세요. |

## Notes for Maintainers

- Keep examples short and vendor-neutral.
- Use `example.test` domains and fake evidence only.
- Prefer wording that describes user-provided assessment results.
- Avoid language that implies AuditForge scans, exploits, probes, or tests live systems.
