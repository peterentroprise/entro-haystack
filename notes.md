Hasura resources
======
<a href="https://docs.hasura.io/1.0/graphql/manual/deployment/updating.html#">Latest Version</a>
<br>
<br>

Migration
------
- <a href="https://docs.hasura.io/1.0/graphql/manual/migrations/auto-apply-migrations.html">Auto-apply migrations/metadata when server starts</a>
- <a href="https://github.com/hasura/graphql-engine/blob/master/scripts/cli-migrations/docker-entrypoint.sh">Migrate script on github for reference</a>
- <a href="https://blog.hasura.io/resetting-hasura-migrations/">Resetting hasura migrations</a>
<br>


Auth with secret
------
JWT authentication is skipped when X-Hasura-Admin-Secret header is found in the request and admin access is granted.
If the admin secret is provided the session variables will also be taken straight from the HTTP headers
```
curl 'http://localhost:8080/v1/graphql' \
	-H 'content-type: application/json' \
	-H 'X-Hasura-Admin-Secret: secret' \
	-H 'X-Hasura-Role: anonymous' \
	--data-binary '{"query":"{\n  test {\n    id\n    name\n  }\n}\n","variables":null}'
```
<br>


Auth with JWT
------
- <a href="https://docs.hasura.io/1.0/graphql/manual/auth/authentication/jwt.html#tl-dr">TL;DR</a>
- <a href="https://docs.hasura.io/1.0/graphql/manual/auth/authentication/jwt.html#configuring-jwt-mode">Configuring JWT mode</a>
- <a href="https://docs.hasura.io/1.0/graphql/manual/auth/authentication/jwt.html#auth-jwt-examples">Auth JWT Examples</a>

JWT authentication is enforced when X-Hasura-Admin-Secret header is not found in the request.
Session variables must be store under the claim 'https://hasura.io/jwt/claims'

```
{
    "sub": "1234567890",
    "name": "John Doe",
    "admin": true,
    "iat": 1516239022,
    "https://hasura.io/jwt/claims": {
        "x-hasura-allowed-roles": ["editor","user", "mod"],
        "x-hasura-default-role": "user",
        "x-hasura-user-id": "1234567890",
        "x-hasura-org-id": "123",
        "x-hasura-custom": "custom-value"
    }
}
```
<br>