import os
import re
import uuid
import textwrap

src_dir = 'pcl5/pcl5-jedi'
dst_dir = 'pcl5_new/pcl5-jedi'
os.makedirs(dst_dir, exist_ok=True)

files = [
  'test_pcl5_pcl_fontdes_ftsdisk_tvrtest.py',
  'test_pcl5_pcl_fontdes_height2.py',
  'test_pcl5_pcl_fontdes_pitchm2.py',
  'test_pcl5_pcl_fontdes_ttselfon.py',
  'test_pcl5_pcl_fontf_bt_chrdes4_bt10_300.py',
  'test_pcl5_pcl_fontf_bt_chrdes4_bt12_300.py',
  'test_pcl5_pcl_fontf_bt_chrdes4_bt12_600.py',
  'test_pcl5_pcl_fontf_bt_chrdes4_bt14_300.py',
  'test_pcl5_pcl_fontf_bt_chrdes4_bt14_600.py',
  'test_pcl5_pcl_fontf_bt_chrdes4_bt3_600.py',
  'test_pcl5_pcl_fontf_bt_chrdes4_bt4_300.py',
  'test_pcl5_pcl_fontf_bt_chrdes4_bt4_600.py',
  'test_pcl5_pcl_fontf_bt_chrdes4_bt5_300.py',
  'test_pcl5_pcl_fontf_bt_chrdes4_bt6_300.py',
  'test_pcl5_pcl_fontf_bt_chrdes4_bt6_600.py',
  'test_pcl5_pcl_fontf_bt_chrdes4_bt8_300.py',
  'test_pcl5_pcl_fontf_bt_chrdes4_bt8_600.py',
  'test_pcl5_pcl_fontf_bt_fntdes0_ftbyt16.py',
  'test_pcl5_pcl_fontf_bt_fntdes0_ftbyt3.py',
  'test_pcl5_pcl_fontf_bt_fntdes0_ftbyt41.py',
  'test_pcl5_pcl_fontf_bt_fntdes20_ft20_300.py',
  'test_pcl5_pcl_fontf_if_fntdes10.py',
  'test_pcl5_pcl_fontf_if_ubpcleo.py',
  'test_pcl5_pcl_fontf_tt_ttfdes.py',
  'test_pcl5_pcl_fontmgmt_asscfont.py',
  'test_pcl5_pcl_fontmgmt_fontm5.py',
  'test_pcl5_pcl_fontmgmt_ttfontm.py',
  'test_pcl5_pcl_fontmgmt_ubmanage.py',
  'test_pcl5_pcl_fontr_bt_prspace.py',
  'test_pcl5_pcl_fontr_bt_uline1.py',
  'test_pcl5_pcl_fontr_if_sclmisc.py',
  'test_pcl5_pcl_fontr_if_ubuline.py',
  'test_pcl5_pcl_fontr_if_unhinted.py',
  'test_pcl5_pcl_fontr_tt_pclrmopb.py',
  'test_pcl5_pcl_fontr_tt_pclrmopu.py',
  'test_pcl5_pcl_fontr_tt_tttranmd.py',
  'test_pcl5_pcl_fontr_tt_ttulineu.py',
  'test_pcl5_pcl_macros_macrosrc_disov_nc.py',
  'test_pcl5_pcl_macros_macrosrc_locpr_nc.py',
  'test_pcl5_pcl_macros_macrosrc_mcro_pjl.py',
  'test_pcl5_pcl_macros_macrosrc_mcrob_nc.py',
  'test_pcl5_pcl_macros_macrosrc_mcroesce.py',
  'test_pcl5_pcl_macros_macrosrc_mcros_nc.py',
  'test_pcl5_pcl_macros_macrosrc_othrl_nc.py',
  'test_pcl5_pcl_pagecntl_custommed_custommed_jedi.py',
  'test_pcl5_pcl_pagecntl_margin.py',
  'test_pcl5_pcl_pagecntl_printdir.py',
  'test_pcl5_pcl_pagecntl_textlng.py',
  'test_pcl5_pcl_pagecntl_topmarg.py',
  'test_pcl5_pcl_parsing_deftext1.py',
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
