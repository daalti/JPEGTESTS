import os, re, uuid, textwrap

src_dir = 'pcl5/high-value'
dst_dir = 'pcl5_new/high-value'
os.makedirs(dst_dir, exist_ok=True)

with open('/tmp/highvalue_files.txt') as f:
    files = [line.strip() for line in f if line.strip()]

for fname in files:
    orig_path = os.path.join(src_dir, fname)
    base = fname[len('test_pcl5_highvalue_'):-3]  # remove prefix and .py
    new_fname = f'test_when_printing_pcl5_highvalue_{base}.py'
    dst_path = os.path.join(dst_dir, new_fname)

    with open(orig_path) as f:
        content = f.read()

    # Extract metadata block
    meta_match = re.search(r'(\$\$\$\$\$_BEGIN_TEST_METADATA_DECLARATION_\$\$\$\$\$.*?\$\$\$\$\$_END_TEST_METADATA_DECLARATION_\$\$\$\$\$)', content, re.S)
    if not meta_match:
        raise ValueError(f'Metadata block not found in {fname}')
    metadata = meta_match.group(1)

    # Update metadata lines
    lines = []
    for line in metadata.splitlines():
        if '+asset:' in line:
            line = re.sub(r'\+asset:.*', '+asset:PDL_New', line)
        if '+delivery_team:' in line:
            line = re.sub(r'\+delivery_team:.*', '+delivery_team:QualityGuild', line)
        if re.search(r'\+name:', line):
            indent = line[:line.find('+')]
            line = f"{indent}+name:TestWhenPrintingJPEGFile::test_when_using_pcl5_highvalue_{base}_file_then_succeeds"
        if re.search(r'\+guid:', line):
            indent = line[:line.find('+')]
            line = f"{indent}+guid:{uuid.uuid4()}"
        lines.append(line)
    metadata_new = '\n'.join(lines)

    # Determine if MediaOrientation or TrayLevel were imported
    use_orientation = 'MediaOrientation' in content
    use_traylevel = 'TrayLevel' in content

    imports = ['import logging', 'from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType']
    if use_orientation or use_traylevel:
        imp = 'from dunetuf.print.print_common_types import MediaOrientation, TrayLevel'
        # merge orientation/traylevel into same line? Wait, we already imported others. We'll append additional import line.
        imports.append('from dunetuf.print.print_common_types import MediaOrientation, TrayLevel')
    imports.append('from dunetuf.print.new.output.output_saver import OutputSaver')
    imports.append('from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver')

    import_block = '\n'.join(imports)

    # Build new test body
    # Extract function body after metadata block
    after_meta = content.split(meta_match.group(0))[-1]
    # get lines after def ... to end
    func_match = re.search(r'def\s+test_[^(]+\(.*?\):\n([\s\S]*)', after_meta)
    body = func_match.group(1) if func_match else ''

    # Replace old constructs with new methods
    replacements = [
        ('printjob.print_verify_multi', 'self.print.raw.start'),
        ('printjob.print_verify', 'self.print.raw.start'),
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

    # Replace job start call to capture checksum and create wait lines
    # regex: self.print.raw.start('checksum', ...)
    orig_lines = body.splitlines()
    body_lines = []
    for line in orig_lines:
        m = re.search(r"self.print.raw.start\('([0-9a-f]{32,})'", line)
        if m:
            checksum = m.group(1)
            # remove any additional args like timeout or expected_jobs
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
    def test_when_using_pcl5_highvalue_{base}_file_then_succeeds(self):
{body}
''')

    with open(dst_path, 'w') as f:
        f.write(import_block + '\n\n' + class_def)
