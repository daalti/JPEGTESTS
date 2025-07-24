import os
import re
import uuid
import textwrap

src_dir = 'pcl5/pcl5-jedi'
dst_dir = 'pcl5_new/pcl5-jedi'
os.makedirs(dst_dir, exist_ok=True)

files = [
    "test_pcl5_pcl_fontdes_2bytetypeface_kgulcp.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_kgungcf.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_khybatf.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_khybatp.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_khydotf.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_khydotp.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_khygulf.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_khygulfbd.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_khygulfit.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_khygulfv.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_khygulfx.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_khygulfy.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_khygulp.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_khygungf.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_khygungp.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_scsfang.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_scsfangbd.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_scsfangit.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_scsfangv.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_scsfangx.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_scshei.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_scskai.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_scssun.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_tckai.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_tcming.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_tcpming.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_tcpmingbd.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_tcpmingit.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_tcpmingv.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_tcpmingx.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_tcpmingy.py",
    "test_pcl5_pcl_fontdes_fntfmt16.py",
    "test_pcl5_pcl_fontdes_fntfmt16_fmt16seg.py",
    "test_pcl5_pcl_fontdes_font_pri_diskpri.py",
    "test_pcl5_pcl_fontdes_font_pri_fpri300.py",
    "test_pcl5_pcl_fontdes_font_pri_simmpri.py",
    "test_pcl5_pcl_fontdes_fontpri5.py",
    "test_pcl5_pcl_fontdes_ftsdisk_jbdtest.py",
    "test_pcl5_pcl_fontdes_ftsdisk_jittest.py",
    "test_pcl5_pcl_fontdes_ftsdisk_jtest.py",
    "test_pcl5_pcl_fontdes_ftsdisk_jvrtest.py",
    "test_pcl5_pcl_fontdes_ftsdisk_kbdtest.py",
    "test_pcl5_pcl_fontdes_ftsdisk_kittest.py",
    "test_pcl5_pcl_fontdes_ftsdisk_ktest.py",
    "test_pcl5_pcl_fontdes_ftsdisk_kvrtest.py",
    "test_pcl5_pcl_fontdes_ftsdisk_sittest.py",
    "test_pcl5_pcl_fontdes_ftsdisk_stest.py",
    "test_pcl5_pcl_fontdes_ftsdisk_svrtest.py",
    "test_pcl5_pcl_fontdes_ftsdisk_tittest.py",
    "test_pcl5_pcl_fontdes_ftsdisk_ttest.py",
]

meta_re = re.compile(r'(\$\$\$\$\$_BEGIN_TEST_METADATA_DECLARATION_\$\$\$\$\$.*?\$\$\$\$\$_END_TEST_METADATA_DECLARATION_\$\$\$\$\$)', re.S)
checksum_re = re.compile(r"'([0-9a-f]{32,})'")

for fname in files:
    with open(os.path.join(src_dir, fname)) as f:
        content = f.read()

    base = fname[len('test_'):-3]
    new_fname = f'test_when_printing_{base}.py'
    dst_path = os.path.join(dst_dir, new_fname)

    m = meta_re.search(content)
    if not m:
        raise ValueError(f'Metadata block not found in {fname}')
    metadata = m.group(1)

    meta_lines = []
    for line in metadata.splitlines():
        if '+asset:' in line:
            line = re.sub(r'\+asset:.*', '+asset:PDL_New', line)
        if '+delivery_team:' in line:
            line = re.sub(r'\+delivery_team:.*', '+delivery_team:QualityGuild', line)
        if '+name:' in line:
            indent = line[:line.find('+')]
            line = f"{indent}+name:TestWhenPrintingJPEGFile::test_when_using_{base}_file_then_succeeds"
        if '+guid:' in line:
            indent = line[:line.find('+')]
            line = f"{indent}+guid:{uuid.uuid4()}"
        meta_lines.append(line)
    metadata_new = '\n'.join('    ' + ln for ln in meta_lines)

    checksum_match = checksum_re.search(content)
    checksum = checksum_match.group(1) if checksum_match else ''

    imports = [
        'import logging',
        'from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType',
        'from dunetuf.print.new.output.output_saver import OutputSaver',
        'from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver',
    ]
    import_block = '\n'.join(imports)

    method_lines = textwrap.dedent(f'''\
    def test_when_using_{base}_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('{checksum}')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
''').splitlines()
    test_method = '\n'.join('    ' + line if line else '' for line in method_lines)

    class_def = textwrap.dedent(f'''\
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
{test_method}
''')

    with open(dst_path, 'w') as out:
        out.write(import_block + '\n\n' + class_def)
