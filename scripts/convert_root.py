import os, re, uuid, textwrap

src_dir = 'pcl5'
dst_dir = 'pcl5_new'
os.makedirs(dst_dir, exist_ok=True)

files = [f for f in os.listdir(src_dir) if f.endswith('.py')]

for fname in files:
    base = fname[len('test_'):-3]
    new_fname = f'test_when_printing_{base}.py'
    dst_path = os.path.join(dst_dir, new_fname)
    if os.path.exists(dst_path):
        continue
    with open(os.path.join(src_dir, fname)) as f:
        content = f.read()

    # gather extra imports before metadata
    pre_meta, rest = content.split('"""', 1)
    import_lines = []
    for line in pre_meta.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith('import pytest'):
            continue
        import_lines.append(line)

    # mandatory imports
    imports = [
        'import logging',
        'from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType',
        'from dunetuf.print.new.output.output_saver import OutputSaver',
        'from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver',
    ]
    for line in import_lines:
        if line not in imports:
            imports.append(line)
    import_block = '\n'.join(imports)

    meta_match = re.search(r'(\$\$\$\$\$_BEGIN_TEST_METADATA_DECLARATION_\$\$\$\$\$.*?\$\$\$\$\$_END_TEST_METADATA_DECLARATION_\$\$\$\$\$)', content, re.S)
    if not meta_match:
        raise ValueError(f'Metadata block not found in {fname}')
    metadata = meta_match.group(1)

    lines = []
    for line in metadata.splitlines():
        if '+asset:' in line:
            line = re.sub(r'\+asset:.*', '+asset:PDL_New', line)
        if '+delivery_team:' in line:
            line = re.sub(r'\+delivery_team:.*', '+delivery_team:QualityGuild', line)
        if re.search(r'\+name:', line):
            indent = line[:line.find('+')]
            line = f"{indent}+name:TestWhenPrintingJPEGFile::test_when_using_{base}_file_then_succeeds"
        if re.search(r'\+guid:', line):
            indent = line[:line.find('+')]
            line = f"{indent}+guid:{uuid.uuid4()}"
        lines.append(line)
    lines = ['    ' + ln for ln in lines]
    metadata_new = '\n'.join(lines)

    after_meta = content.split(meta_match.group(0))[-1]
    func_match = re.search(r'def\s+test_[^(]+\(.*?\):\n([\s\S]*)', after_meta)
    body = func_match.group(1) if func_match else ''
    body = textwrap.dedent(body)

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
        ('print_emulation.print_engine_platform', 'self.get_platform()'),
        ('print_emulation.tray.', 'self.media.tray.'),
        ('print_emulation.', 'self.media.'),
        ('tray.get_default_source()', 'self.media.get_default_source()'),
        ('tray.is_size_supported', 'self.media.is_size_supported'),
        ('tray.configure_tray', 'self.media.tray.configure_tray'),
        ('tray.reset_trays()', 'self.media.tray.reset_trays()'),
        ('configuration.familyname', 'self.configuration.familyname'),
    ]
    for old, new in replacements:
        body = body.replace(old, new)

    orig_lines = body.splitlines()
    body_lines = []
    for line in orig_lines:
        m = re.search(r"self.print.raw.start\('([0-9a-f]{32,})'", line)
        if m:
            checksum = m.group(1)
            prefix = re.match(r'^\s*', line).group()
            body_lines.append(f"{prefix}job_id = self.print.raw.start('{checksum}')")
            body_lines.append(f"{prefix}self.print.wait_for_job_completion(job_id)")
            continue
        body_lines.append(line)
    body = '\n'.join(body_lines)
    body = '\n'.join(('        ' + l if l.strip() else '') for l in body.splitlines())

    class_def = textwrap.dedent(f'''
class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        setup_output_saver(cls.outputsaver)

    @classmethod
    def teardown_class(cls):
        """Release shared test resources."""

    def teardown_method(self):
        """Clean up resources after each test."""
        # Clear job queue
        self.job_queue.cancel_all_jobs()
        self.job_queue.wait_for_queue_empty()

        # Clear job history
        self.job_history.clear()
        self.job_history.wait_for_history_empty()

        # Reset media configuration to default
        self.media.update_media_configuration(self.default_configuration)
        tear_down_output_saver(self.outputsaver)
    """
    {metadata_new}
    """
    def test_when_using_{base}_file_then_succeeds(self):
{body}
''')

    with open(dst_path, 'w') as f:
        f.write(import_block + '\n\n' + class_def)
