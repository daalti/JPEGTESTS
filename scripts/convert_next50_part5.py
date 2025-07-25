import os
import re
import uuid
import textwrap

src_dir = 'pcl5/pcl5-jedi'
dst_dir = 'pcl5_new/pcl5-jedi'
os.makedirs(dst_dir, exist_ok=True)

files = [
    'test_pcl5_testfiles_c_ebar_duplex.py',
    'test_pcl5_testfiles_collatedqty2.py',
    'test_pcl5_testfiles_color_cmyrule.py',
    'test_pcl5_testfiles_color_cmyvector.py',
    'test_pcl5_testfiles_color_lsg00121921.py',
    'test_pcl5_testfiles_color_pges.py',
    'test_pcl5_testfiles_gcusrprog.py',
    'test_pcl5_testfiles_gl_2fonts.py',
    'test_pcl5_testfiles_gl_ac.py',
    'test_pcl5_testfiles_gl_bezier.py',
    'test_pcl5_testfiles_gl_bp.py',
    'test_pcl5_testfiles_gl_cp.py',
    'test_pcl5_testfiles_gl_cpdown.py',
    'test_pcl5_testfiles_gl_df.py',
    'test_pcl5_testfiles_gl_di.py',
    'test_pcl5_testfiles_gl_dr.py',
    'test_pcl5_testfiles_gl_dv.py',
    'test_pcl5_testfiles_gl_es.py',
    'test_pcl5_testfiles_gl_ew.py',
    'test_pcl5_testfiles_gl_fi.py',
    'test_pcl5_testfiles_gl_input.py',
    'test_pcl5_testfiles_gl_lb.py',
    'test_pcl5_testfiles_gl_pm_pe.py',
    'test_pcl5_testfiles_gl_ro.py',
    'test_pcl5_testfiles_gl_sb.py',
    'test_pcl5_testfiles_gl_sl.py',
    'test_pcl5_testfiles_gl_sm.py',
    'test_pcl5_testfiles_gl_sv.py',
    'test_pcl5_testfiles_gl_td.py',
    'test_pcl5_testfiles_gl_text.py',
    'test_pcl5_testfiles_gl_text_bg.py',
    'test_pcl5_testfiles_gl_tr.py',
    'test_pcl5_testfiles_gl_ul.py',
    'test_pcl5_testfiles_graphic_state_definelogicalpage.py',
    'test_pcl5_testfiles_graphic_state_duppgsideSelect.py',
    'test_pcl5_testfiles_graphic_state_hpglpclcap.py',
    'test_pcl5_testfiles_graphic_state_multijob.py',
    'test_pcl5_testfiles_graphic_state_pagecheck.py',
    'test_pcl5_testfiles_graphic_state_pagecheckmono.py',
    'test_pcl5_testfiles_graphic_state_pageclip.py',
    'test_pcl5_testfiles_graphic_state_text_vector.py',
    'test_pcl5_testfiles_int.py',
    'test_pcl5_testfiles_internalpages_wrapped_selftest.py',
    'test_pcl5_testfiles_languageswitching_multilingualjob.py',
    'test_pcl5_testfiles_languageswitching_pcl2ps.py',
    'test_pcl5_testfiles_masering_3pg_2mopy.py',
    'test_pcl5_testfiles_media_handling_twopageduplexptvb.py',
    'test_pcl5_testfiles_media_handling_userdefinedcustommedia.py',
    'test_pcl5_testfiles_misc_Alphadiskmacro.py',
    'test_pcl5_testfiles_misc_alphadiskfonts.py',
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
