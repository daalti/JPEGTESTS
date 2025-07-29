import os
import re
import uuid
import textwrap

src_dir = 'rs'
dst_dir = 'rs_new'
os.makedirs(dst_dir, exist_ok=True)

files = [f for f in os.listdir(src_dir) if f.endswith('.py')]

meta_re = re.compile(r'(\$\$\$\$\$_BEGIN_TEST_METADATA_DECLARATION_\$\$\$\$\$.*?\$\$\$\$\$_END_TEST_METADATA_DECLARATION_\$\$\$\$\$)', re.S)
func_header_re = re.compile(r'def\s+(test_[^\(]+)\([^)]*\):')

for fname in files:
    with open(os.path.join(src_dir, fname)) as f:
        content = f.read()

    needs_outputverifier = 'outputverifier' in content

    # remove fixture definitions
    content = re.sub(r'@pytest\.fixture[\s\S]*', '', content)

    metas = list(meta_re.finditer(content))
    if not metas:
        raise ValueError(f'Metadata block not found in {fname}')

    pre_meta = content[:metas[0].start()]
    pre_meta = pre_meta.rstrip()
    if pre_meta.endswith('"""'):
        pre_meta = pre_meta[:-3]
        if pre_meta.endswith('\n'):
            pre_meta = pre_meta[:-1]
    pre_lines = pre_meta.splitlines()
    import_lines = []
    other_lines = []
    for line in pre_lines:
        stripped = line.strip()
        if stripped.startswith('import ') or stripped.startswith('from '):
            if 'import pytest' in stripped:
                continue
            if stripped and stripped not in import_lines:
                import_lines.append(stripped)
        else:
            if line.strip() or other_lines:
                other_lines.append(line)

    imports = [
        'import logging',
        'from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType',
        'from dunetuf.print.new.output.output_saver import OutputSaver',
        'from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver',
    ]
    if needs_outputverifier:
        imports.append('from dunetuf.print.new.output.output_verifier import OutputVerifier')
    for line in import_lines:
        if line not in imports:
            imports.append(line)
    import_block = '\n'.join(imports)
    other_preamble = '\n'.join(other_lines).strip()

    class_parts = []
    class_parts.append('class TestWhenPrintingJPEGFile(TestWhenPrinting):')
    class_parts.append('    @classmethod')
    class_parts.append('    def setup_class(cls):')
    class_parts.append('        """Initialize shared test resources."""')
    class_parts.append('        super().setup_class()')
    class_parts.append('        cls.outputsaver = OutputSaver()')
    class_parts.append('        setup_output_saver(cls.outputsaver)')
    if needs_outputverifier:
        class_parts.append('        cls.outputverifier = OutputVerifier(cls.outputsaver)')
    class_parts.append('')
    class_parts.append('    @classmethod')
    class_parts.append('    def teardown_class(cls):')
    class_parts.append('        """Release shared test resources."""')
    class_parts.append('')
    class_parts.append('    def teardown_method(self):')
    class_parts.append('        """Clean up resources after each test."""')
    class_parts.append('        # Clear job queue')
    class_parts.append('        self.job_queue.cancel_all_jobs()')
    class_parts.append('        self.job_queue.wait_for_queue_empty()')
    class_parts.append('')
    class_parts.append('        # Clear job history')
    class_parts.append('        self.job_history.clear()')
    class_parts.append('        self.job_history.wait_for_history_empty()')
    class_parts.append('')
    class_parts.append('        # Reset media configuration to default')
    class_parts.append('        self.media.update_media_configuration(self.default_configuration)')
    class_parts.append('        tear_down_output_saver(self.outputsaver)')

    # keep text after last processed part to append later
    leftover_after = ''

    for i, meta in enumerate(metas):
        start = meta.end()
        end = metas[i + 1].start() if i + 1 < len(metas) else len(content)
        region = content[start:end]

        lines = region.splitlines(keepends=True)
        header_idx = None
        for idx, ln in enumerate(lines):
            if func_header_re.match(ln):
                header_idx = idx
                func_name = func_header_re.match(ln).group(1)
                break
        if header_idx is None:
            continue

        body_lines = []
        for ln in lines[header_idx + 1:]:
            if ln.startswith(' ') or ln.startswith('\t') or ln.strip() == '':
                body_lines.append(ln)
            else:
                break

        body = ''.join(body_lines)
        consumed_len = sum(len(l) for l in lines[:header_idx + 1 + len(body_lines)])
        leftover_after += region[consumed_len:]

        orig_basename = func_name[len('test_'):]

        lines = []
        for line in meta.group(1).splitlines():
            if '+asset:' in line:
                line = re.sub(r'\+asset:.*', '+asset:PDL_New', line)
            if '+delivery_team:' in line:
                line = re.sub(r'\+delivery_team:.*', '+delivery_team:QualityGuild', line)
            if re.search(r'\+name:', line):
                indent = line[:line.find('+')]
                line = f"{indent}+name:TestWhenPrintingJPEGFile::test_when_using_{orig_basename}_file_then_succeeds"
            if re.search(r'\+guid:', line):
                indent = line[:line.find('+')]
                line = f"{indent}+guid:{uuid.uuid4()}"
            lines.append(line)
        metadata_new = '\n'.join('    ' + ln for ln in lines)

        body = textwrap.dedent(body)
        if needs_outputverifier:
            body = re.sub(r'\boutputverifier\.', 'self.outputverifier.', body)
            body = body.replace('self.outputverifier.self.outputsaver', 'self.outputverifier.outputsaver')
        replacements = [
            ('printjob.print_verify_multi', 'self.print.raw.start'),
            ('printjob.print_verify', 'self.print.raw.start'),
            ('printjob.start_print', 'self.print.raw.start'),
            ('printjob.wait_for_job_completion', 'self.print.wait_for_job_completion'),
            ('outputsaver.validate_crc_tiff(udw)', 'self.outputsaver.validate_crc_tiff()'),
            ('outputsaver.validate_crc_tiff( udw )', 'self.outputsaver.validate_crc_tiff()'),
            ('outputsaver.validate_crc_tiff', 'self.outputsaver.validate_crc_tiff'),
            ('outputsaver.save_output()', 'self.outputsaver.save_output()'),
            ('outputsaver.operation_mode', 'self.outputsaver.operation_mode'),
            ('outputsaver.get_crc()', 'self.outputsaver.get_crc()'),
            ('outputsaver.verify_pdl_crc', 'self.outputsaver.verify_pdl_crc'),
            ('outputsaver.verify_output_crc', 'self.outputsaver.verify_output_crc'),
            ('outputsaver.clear_output()', 'self.outputsaver.clear_output()'),
            ('print_emulation.print_engine_platform', 'self.get_platform()'),
            ('print_emulation.tray.', 'self.media.tray.'),
            ('print_emulation.', 'self.media.'),
            ('tray.get_default_source()', 'self.media.get_default_source()'),
            ('tray.is_size_supported', 'self.media.is_size_supported'),
            ('tray.configure_tray', 'self.media.tray.configure_tray'),
            ('tray.reset_trays()', 'self.media.tray.reset_trays()'),
            ('configuration.familyname', 'self.configuration.familyname'),
            ('tray.load_simulator_media', 'self.media.tray.load_simulator_media'),
        ]
        for old, new in replacements:
            body = body.replace(old, new)

        lines_body = []
        for line in body.splitlines():
            m = re.search(r"self.print.raw.start\('([0-9a-f]{32,})'", line)
            if m:
                checksum = m.group(1)
                prefix = re.match(r'^\s*', line).group()
                lines_body.append(f"{prefix}job_id = self.print.raw.start('{checksum}')")
                lines_body.append(f"{prefix}self.print.wait_for_job_completion(job_id)")
                continue
            lines_body.append(line)
        body = '\n'.join(lines_body)
        body = '\n'.join(('        ' + l if l.strip() else '') for l in body.splitlines())

        class_parts.append('    """')
        class_parts.append(metadata_new)
        class_parts.append('    """')
        class_parts.append(f'    def test_when_using_{orig_basename}_file_then_succeeds(self):')
        class_parts.append(body)
        class_parts.append('')

    class_def = '\n'.join(class_parts)

    final_content = import_block + '\n\n'
    if other_preamble:
        final_content += other_preamble + '\n\n'
    final_content += class_def
    if leftover_after.strip():
        final_content += '\n' + leftover_after

    dst_path = os.path.join(dst_dir, f'test_when_printing_{fname[len("test_"):-3]}.py')
    with open(dst_path, 'w') as f:
        f.write(final_content)
