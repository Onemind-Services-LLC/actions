"""Keep approved runner defaults, caller routing, and mirrored build-tool images."""

from pathlib import Path
import unittest

import yaml


class ExecutionPolicyTests(unittest.TestCase):
    def test_workflows_keep_runner_policy_and_configurable_defaults(self):
        configurable_workflows = {'netbox-plugin-tests.yml', 'pre-commit.yml'}
        for path in Path('.github/workflows').glob('*.yml'):
            workflow = yaml.safe_load(path.read_text())
            for job in workflow.get('jobs', {}).values():
                if 'runs-on' in job:
                    if path.name in configurable_workflows:
                        self.assertEqual(job['runs-on'], '${{ inputs.runs-on }}', str(path))
                        inputs = workflow[True]['workflow_call']['inputs']
                        self.assertEqual(inputs['runs-on']['default'], 'ubuntu-22.04-sh', str(path))
                    else:
                        self.assertEqual(job['runs-on'], 'ubuntu-22.04-sh', str(path))

    def test_artifact_builds_authenticate_before_starting_mirrored_buildkit(self):
        for name, job_name in [('ci.yml', 'artifact_contract'), ('container-build.yml', 'build')]:
            workflow = yaml.safe_load((Path('.github/workflows') / name).read_text())
            steps = workflow['jobs'][job_name]['steps']
            login = next(i for i, step in enumerate(steps) if step.get('uses', '').startswith('docker/login-action@'))
            buildx = next(i for i, step in enumerate(steps) if step.get('uses', '').startswith('docker/setup-buildx-action@'))
            self.assertLess(login, buildx, name)
            self.assertTrue(steps[buildx]['with']['driver-opts'].startswith('image=registry.onemindservices.com/docker.io/'))
            build = next(step for step in steps if step.get('uses', '').startswith('docker/build-push-action@'))
            self.assertTrue(build['with']['sbom'].startswith('generator=registry.onemindservices.com/docker.io/'))


if __name__ == '__main__':
    unittest.main()
