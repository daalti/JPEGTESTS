import os
import re
import uuid
import textwrap

src_dir = 'pcl5/pcl5-jedi'
dst_dir = 'pcl5_new/pcl5-jedi'
os.makedirs(dst_dir, exist_ok=True)

files = [
    "test_pcl5_pcl_cap_textpath.py",
    "test_pcl5_pcl_cpedefects_cr43864_jobnamewithamp.py",
    "test_pcl5_pcl_cpedefects_lsg55412.py",
    "test_pcl5_pcl_cpedefects_lsg55412_lsg55412_jedi.py",
    "test_pcl5_pcl_duplex_duplexm1.py",
    "test_pcl5_pcl_duplex_duplexm3.py",
    "test_pcl5_pcl_duplex_duplexm6.py",
    "test_pcl5_pcl_duplex_duplx5a.py",
    "test_pcl5_pcl_duplex_duplx5b1.py",
    "test_pcl5_pcl_duplex_duplx5b2.py",
    "test_pcl5_pcl_duplex_duplx5b3.py",
    "test_pcl5_pcl_duplex_duplx5c.py",
    "test_pcl5_pcl_duplex_duplx5e.py",
    "test_pcl5_pcl_font_andale_selectandalefont_resourcedata.py",
    "test_pcl5_pcl_font_feature_ffont_cf.py",
    "test_pcl5_pcl_font_feature_ffont_cf_hw.py",
    "test_pcl5_pcl_font_feature_fmacro_cf.py",
    "test_pcl5_pcl_font_feature_fmacro_cf_hw.py",
    "test_pcl5_pcl_font_feature_gpri_1.py",
    "test_pcl5_pcl_font_feature_mult_gfont.py",
    "test_pcl5_pcl_font_feature_overpri_1.py",
    "test_pcl5_pcl_font_feature_usb_fmacro_cf.py",
    "test_pcl5_pcl_font_feature_usb_fpri_11.py",
    "test_pcl5_pcl_font_feature_usb_fpri_12.py",
    "test_pcl5_pcl_font_feature_usb_fpri_13.py",
    "test_pcl5_pcl_font_feature_usb_fpri_6.py",
    "test_pcl5_pcl_font_feature_usb_fpri_8.py",
    "test_pcl5_pcl_font_feature_usb_fpri_8_hw.py",
    "test_pcl5_pcl_font_feature_usb_fpri_9.py",
    "test_pcl5_pcl_font_feature_usb_gpri_1.py",
    "test_pcl5_pcl_font_feature_usb_mult_gfont.py",
    "test_pcl5_pcl_font_feature_usb_overpri_1_hw.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_jgoth.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_jminch.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_jpgoth.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_jpminch.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_jpminchbd.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_jpminchit.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_jpminchv.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_jpminchx.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_jpminchy.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_kbatcf.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_kbatcp.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_kdotcf.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_kdotcp.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_kdotcpit.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_kdotcpv.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_kdotcpx.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_kdotcpy.py",
    "test_pcl5_pcl_fontdes_2bytetypeface_kgulcf.py",
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
