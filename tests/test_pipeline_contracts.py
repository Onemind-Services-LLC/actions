"""Execute security-sensitive composite steps against controlled commands."""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


def step(action, name):
    data = yaml.safe_load((ROOT / "actions" / action / "action.yml").read_text())
    return next(item for item in data["runs"]["steps"] if item["name"] == name)


class PipelineContractTests(unittest.TestCase):
    def test_coverage_failure_is_blocking_without_reporter(self):
        gate = step("django-test-runner", "Enforce coverage threshold")
        self.assertFalse(gate.get("continue-on-error", False))
        with tempfile.TemporaryDirectory() as directory:
            coverage = Path(directory) / "coverage"
            coverage.write_text('#!/bin/sh\n[ "$1" = report ] && [ "$2" = --fail-under=100 ] && exit 2\nexit 99\n')
            coverage.chmod(0o755)
            env = dict(os.environ, PATH=directory + os.pathsep + os.environ["PATH"], COVERAGE_MINIMUM="100")
            result = subprocess.run(["bash", "-e", "-o", "pipefail", "-c", gate["run"]], env=env)
            self.assertEqual(result.returncode, 2)

    def test_dependency_authentication_never_updates_global_git_configuration(self):
        install = step("python-setup-install", "Install From requirements.txt")
        with tempfile.TemporaryDirectory() as directory:
            fake_python = Path(directory) / "python"
            fake_python.write_text('''#!/bin/sh
[ "$GIT_CONFIG_COUNT" = 1 ] || exit 91
[ "$GIT_CONFIG_KEY_0" = 'url.https://x-access-token:synthetic-ci-token@github.com/.insteadOf' ] || exit 92
[ "$GIT_CONFIG_VALUE_0" = 'https://github.com/' ] || exit 93
[ "$1 $2 $3 $4 $5" = '-m pip install -r requirements.txt' ] || exit 94
''')
            fake_python.chmod(0o755)
            config = Path(directory) / "global.gitconfig"
            config.write_text("[user]\n    name = Existing User\n")
            before = config.read_bytes()
            env = dict(os.environ, PATH=directory + os.pathsep + os.environ["PATH"],
                       DEPENDENCY_TOKEN="synthetic-ci-token", GIT_CONFIG_GLOBAL=str(config))
            subprocess.run(["bash", "-e", "-o", "pipefail", "-c", install["run"]], env=env, check=True)
            self.assertEqual(config.read_bytes(), before)

    def test_settings_reject_environment_file_injection(self):
        export = step("django-test-runner", "Export Django settings to env")
        for key, module in [("DJANGO_SETTINGS_MODULE", "zeus.settings\nINJECTED=yes"),
                            ("PATH", "zeus.settings"), ("DJANGO_SETTINGS_MODULE", "$(touch injected)")]:
            with self.subTest(key=key, module=module), tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / "github-env"
                env = dict(os.environ, SETTINGS_KEY=key, SETTINGS_MODULE=module, GITHUB_ENV=str(output))
                result = subprocess.run(["bash", "-e", "-c", export["run"]], env=env, capture_output=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(output.exists())
