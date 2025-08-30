## Kibana Sourcemaps Upload

Uploads Next.js sourcemaps to Kibana/Elastic APM and optionally deletes existing artifacts that match `<service_name>-<service_version>` prior to upload. Implemented with curl and Node core modules (no extra npm deps).

### Inputs

- kibana-url: Kibana APM sourcemaps API URL. Default: `https://kibana.onemindservices.com/api/apm/sourcemaps`.
- kibana-api-key: API key for Kibana/Elastic; used in `Authorization: ApiKey <key>`.
- base-url: Public base URL to `_next/static`, e.g. `https://example.com/_next/static`.
- build-dir: Repo-relative path to the Next.js static dir. Default: `.next/static`.
- working-directory: Project directory (contains `package.json`). Default: `.`.
- service-name: Override service name (defaults to `package.json` name).
- service-version: Override version (defaults to `package.json` version).
- delete-existing: Delete existing sourcemaps matching the identifier. Default: `true`.
- chunks-dirs: Comma-separated list of subdirs to scan for `.js.map`. Default: `chunks`.
- retries: Upload retries per file. Default: `3`.

### Behavior

- Deletes existing sourcemaps by calling `GET /api/apm/sourcemaps` and `DELETE /api/apm/sourcemaps/{id}` for artifacts whose `identifier` starts with `<name>-<version>`.
- Recursively finds `.js.map` files under `build-dir/chunks` by default (e.g., `chunks/app/about-us/...`).
- Computes `bundle_filepath` by stripping `.map` and prefixing with `base-url`.
- Uploads via `multipart/form-data` fields: `service_name`, `service_version`, `bundle_filepath`, and file field `sourcemap`.

### Example

```yaml
- name: Upload sourcemaps
  uses: Onemind-Services-LLC/actions/actions/kibana-sourcemaps-upload@master
  with:
    kibana-url: https://kibana.onemindservices.com/api/apm/sourcemaps
    kibana-api-key: ${{ secrets.KIBANA_API_KEY }}
    base-url: https://cloudmylab.com/_next/static
    build-dir: .next/static
    # Optional overrides
    # service-name: my-service
    # service-version: 1.2.3
    delete-existing: 'true'
```
