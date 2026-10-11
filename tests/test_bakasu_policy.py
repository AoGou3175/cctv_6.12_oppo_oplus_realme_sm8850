"""执行真实的 BakaSU 配置片段，核对 main 选择和上游 SUSFS 暂停处理。"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(sys.argv.pop(1))
BASH = 'C:/Program Files/Git/bin/bash.exe' if os.name == 'nt' else shutil.which('bash')
VERSIONS = ('23', '23_gki', '23_mtk', '38', '58', '58_mtk', '69_gki')


def workflow(version):
    path = ROOT / '.github/workflows' / f'fastbuild_6.12.{version}.yml'
    return yaml.load(path.read_text(encoding='utf-8'), Loader=yaml.BaseLoader)


def execute(script, suspended):
    with tempfile.TemporaryDirectory(prefix='bakasu-policy-') as folder:
        root = Path(folder)
        workspace = root / 'kernel_workspace'
        config = workspace / 'common/arch/arm64/configs/gki_defconfig'
        config.parent.mkdir(parents=True)
        config.write_text('', encoding='utf-8')
        compat = workspace / 'KernelSU/kernel/tools/susfs_compat.mk'
        compat.parent.mkdir(parents=True)
        compat.write_text('$(error Please wait susfs update.)\n' if suspended else '', encoding='utf-8')
        # 仅替换外部下载和提交计数；执行的分支、检查、退出和配置写入均来自真实脚本。
        prefix = '''curl() { printf '%s\n' 'printf "%s\\n" "$1" > setup-ref'; }
git() { printf '4526\n'; }
export GITHUB_ENV="$PWD/github-env" GITHUB_OUTPUT="$PWD/github-output"
'''
        result = subprocess.run([BASH, '-e', '-c', prefix + script], cwd=root,
                                capture_output=True, encoding='utf-8', errors='replace')
        ref = workspace / 'setup-ref'
        return result, ref.read_text(encoding='utf-8').strip() if ref.exists() else '', config.read_text(encoding='utf-8')


def action_script(version, kind, susfs):
    child = workflow(version)
    step = next(step for step in child['jobs']['build']['steps'] if step.get('id') == 'ksu_version')
    script = step['run'].replace('${{ inputs.ksu_type }}', kind)
    script = script.replace('${{ inputs.susfs_enable }}', 'true' if susfs else 'false')
    return re.sub(r'\$\{\{ env\.(\w+) \}\}', lambda m: child['env'][m[1]], script)


def local_script(version, branch, susfs):
    text = (ROOT / 'local' / f'builder_6.12.{version}.sh').read_text(encoding='utf-8')
    block = text.split('# ===== 拉取 KSU 并设置版本号 =====', 1)[1].split('elif ', 1)[0]
    return f'cd kernel_workspace\nKSU_BRANCH={branch}\nAPPLY_SUSFS={susfs}\n' + block + '\nfi\n'


class BakaSUPolicyTests(unittest.TestCase):
    def test_default_dispatch_does_not_request_suspended_susfs(self):
        paths = [ROOT / '.github/workflows/build-test_6.12_kpm.yml']
        paths += [ROOT / '.github/workflows' / f'fastbuild_6.12.{v}.yml' for v in VERSIONS]
        for path in paths:
            with self.subTest(path=path.name):
                data = yaml.load(path.read_text(encoding='utf-8'), Loader=yaml.BaseLoader)
                self.assertEqual(data['on']['workflow_dispatch']['inputs']['susfs_enable']['default'], 'false')

    def check_actions(self, kind, susfs, suspended, should_pass):
        for version in VERSIONS:
            with self.subTest(version=version, kind=kind):
                result, ref, config = execute(action_script(version, kind, susfs), suspended)
                self.assertEqual(ref, 'main', result.stdout + result.stderr)
                self.assertEqual(result.returncode == 0, should_pass, result.stdout + result.stderr)
                if should_pass:
                    self.assertIn('CONFIG_KSU_FULL_NAME_FORMAT=', config)
                else:
                    self.assertIn('SUSFS', result.stdout + result.stderr)
                    self.assertEqual(config, '')

    def test_actions_latest_main_without_susfs(self):
        self.check_actions('bakasu', False, True, True)

    def test_actions_suspended_susfs_rejected_without_downgrade(self):
        self.check_actions('bakasu', True, True, False)

    def test_actions_sukisu_alias_obeys_same_suspension(self):
        self.check_actions('sukisu', True, True, False)

    def test_actions_resumed_upstream_can_enable_susfs(self):
        self.check_actions('bakasu', True, False, True)

    def check_local(self, branch, susfs, suspended, should_pass):
        for version in VERSIONS:
            with self.subTest(version=version, branch=branch):
                result, ref, config = execute(local_script(version, branch, susfs), suspended)
                self.assertEqual(ref, 'main', result.stdout + result.stderr)
                self.assertEqual(result.returncode == 0, should_pass, result.stdout + result.stderr)
                self.assertEqual(bool(config), should_pass)

    def test_local_latest_main_without_susfs(self):
        self.check_local('r', 'n', True, True)

    def test_local_suspended_susfs_rejected_without_downgrade(self):
        self.check_local('r', 'y', True, False)

    def test_local_sukisu_alias_obeys_same_suspension(self):
        self.check_local('Y', 'Y', True, False)

    def test_local_resumed_upstream_can_enable_susfs(self):
        self.check_local('r', 'y', False, True)


if __name__ == '__main__':
    unittest.main()
