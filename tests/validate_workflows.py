"""检查 6.12 上游同步后手动/批量入口、版本和 ZIP 命名。"""
import re
import sys
from pathlib import Path

import yaml


root = Path(sys.argv[1])
workflow_dir = root / '.github' / 'workflows'
versions = ('23', '23_gki', '23_mtk', '38', '58', '58_mtk', '69_gki')
parent_text = (workflow_dir / 'build-test_6.12_kpm.yml').read_text(encoding='utf-8')
parent = yaml.load(parent_text, Loader=yaml.BaseLoader)
dispatch = parent['on']['workflow_dispatch']['inputs']
assert dispatch['ksu_type']['default'] == 'bakasu'
assert dispatch['kpm_enable']['default'] == 'true'
jobs = parent['jobs']
builds = {name: job for name, job in jobs.items() if name.startswith('build_')}
assert set(builds) == {f'build_{version}' for version in versions}
assert set(jobs['release']['needs']) == set(builds)
for job_name in builds:
    assert f'needs.{job_name}.result' in jobs['release']['if']
assert '-ne 7' in parent_text
assert 'android16-6.12-2026-03' in parent_text
zip_names = set()
for version in versions:
    job = builds[f'build_{version}']
    assert job['uses'] == f'./.github/workflows/fastbuild_6.12.{version}.yml'
    child_path = root / job['uses']
    text = child_path.read_text(encoding='utf-8')
    child = yaml.load(text, Loader=yaml.BaseLoader)
    assert not re.search(r'^(<<<<<<<|=======|>>>>>>>)', text, re.M)
    assert 'github.event.inputs.' not in text
    assert 'inputs.KERNEL_SUFFIX' not in text
    assert child['env']['SUB_VERSION'] == version
    assert child['env']['BAKASU_SUSFS_REF'] == '5b76b884c75f729a220bb317aa4a4fc78f0e0e9c'
    assert 'bash -s "$KSU_REF"' in text
    assert 'git rev-list --count HEAD' in text
    assert child['on']['workflow_dispatch']['inputs']['ksu_type']['default'] == 'bakasu'
    call = child['on']['workflow_call']
    assert set(job['with']) == set(call['inputs'])
    assert job['with']['batch_mode'] == 'true'
    for name, spec in call['inputs'].items():
        if name != 'batch_mode':
            expected_type = dispatch[name]['type']
            if expected_type == 'choice':
                expected_type = 'string'
            assert spec['type'] == expected_type, (version, name)
            assert job['with'][name] == '${{ inputs.' + name + ' }}'
    assert call['inputs']['batch_mode']['default'] == 'false'
    for output in ('ksuver', 'ak3name'):
        assert call['outputs'][output]['value'] == '${{ jobs.build.outputs.' + output + ' }}'
    assert child['jobs']['release']['if'] == '${{ !inputs.batch_mode }}'
    templates = re.findall(r'AK3_NAME=(AnyKernel3_[^\r\n]+\.zip)', text)
    assert len(templates) == 2
    for template in templates:
        assert '${{ env.SUB_VERSION }}' in template
        resolved = template.replace('${{ env.SUB_VERSION }}', version)
        assert resolved not in zip_names, (version, resolved)
        zip_names.add(resolved)
    if version == '69_gki':
        assert 'android16-6.12-2026-03' in text
assert len(zip_names) == 14
assert 'BakaSU_CI' not in parent_text
assert 'cctv18/ReSukiSU_CI' in parent_text
print('PASS: 7 versions, 15 reusable inputs each, 14 unique ZIP templates, manual/batch entries')
