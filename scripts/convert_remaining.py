import os
import re
import uuid
import textwrap

src_dir = 'pcl5/pcl5-jedi'
dst_dir = 'pcl5_new/pcl5-jedi'
os.makedirs(dst_dir, exist_ok=True)

files = [
' test_pcl5_testfiles_misc_capmove.py',
' test_pcl5_testfiles_misc_charmotionindex.py',
' test_pcl5_testfiles_misc_displayfunc.py',
' test_pcl5_testfiles_misc_flushallpages.py',
' test_pcl5_testfiles_misc_macro.py',
' test_pcl5_testfiles_misc_plotsize.py',
' test_pcl5_testfiles_misc_rightmargin.py',
' test_pcl5_testfiles_misc_rule.py',
' test_pcl5_testfiles_misc_staff.py',
' test_pcl5_testfiles_misc_textdir.py',
' test_pcl5_testfiles_misc_transparentdata.py',
' test_pcl5_testfiles_misc_underline.py',
' test_pcl5_testfiles_nw_econo_off.py',
' test_pcl5_testfiles_nw_econo_on.py',
' test_pcl5_testfiles_pattern_ctxthatc.py',
' test_pcl5_testfiles_pattern_ctxtshad.py',
' test_pcl5_testfiles_pattern_ctxtusr.py',
' test_pcl5_testfiles_pattern_cusrdef.py',
' test_pcl5_testfiles_pattern_cusrprog.py',
' test_pcl5_testfiles_pattern_cusrrot.py',
' test_pcl5_testfiles_pattern_monoudpat.py',
' test_pcl5_testfiles_pattern_monoudpatrule.py',
' test_pcl5_testfiles_pattern_patctl.py',
' test_pcl5_testfiles_pattern_patrefpt.py',
' test_pcl5_testfiles_performance_simplecolor.py',
' test_pcl5_testfiles_pjl_displaysymbols.py',
' test_pcl5_testfiles_pjl_downloadfonts.py',
' test_pcl5_testfiles_pjl_pjlappendcr.py',
' test_pcl5_testfiles_pjl_pjlfontsource.py',
' test_pcl5_testfiles_pjl_pjlformlines.py',
' test_pcl5_testfiles_pjl_pjllineterm.py',
' test_pcl5_testfiles_pjl_pjlpaper.py',
' test_pcl5_testfiles_raster_clrwheel.py',
' test_pcl5_testfiles_raster_comp55.py',
' test_pcl5_testfiles_raster_dirpixcmy.py',
' test_pcl5_testfiles_raster_emptyras.py',
' test_pcl5_testfiles_raster_implicitxfer.py',
' test_pcl5_testfiles_raster_indxpicyoffset.py',
' test_pcl5_testfiles_raster_indxplan1.py',
' test_pcl5_testfiles_raster_indxplan2.py',
' test_pcl5_testfiles_raster_indxplan5.py',
' test_pcl5_testfiles_raster_lockouts.py',
' test_pcl5_testfiles_raster_missing.py',
' test_pcl5_testfiles_raster_moreplane.py',
' test_pcl5_testfiles_raster_srcheight0.py',
' test_pcl5_testfiles_raster_srcwidth0.py',
' test_pcl5_testfiles_raster_wh.py',
' test_pcl5_testfiles_raster_white_image_on_black_rule.py',
' test_pcl5_testfiles_raster_white_image_on_empty_page.py',
' test_pcl5_testfiles_text_ascii.py',
' test_pcl5_testfiles_text_colortext.py',
' test_pcl5_testfiles_text_courierbitmap.py',
' test_pcl5_testfiles_text_downloadfont.py',
' test_pcl5_testfiles_text_downloadsymset.py',
' test_pcl5_testfiles_text_dumppage2.py',
' test_pcl5_testfiles_text_dwnldbitmap.py',
' test_pcl5_testfiles_text_dwnldintellifont.py',
' test_pcl5_testfiles_text_intfonts.py',
' test_pcl5_testfiles_uncollatedcopies2.py',
' test_pcl5_testfiles_vector_colorrule.py',
' test_pcl5_testfiles_vector_epagerules.py',
' test_pcl5_testfiles_vector_teenyweenydots.py',
' test_pcl5_testfiles_vector_vector.py',
' test_pcl5_testfiles_whql_cd9m_let.py',
' test_pcl5_testfiles_whql_ch20_let.py',
' test_pcl5_testfiles_whql_fnt8_let.py',
' test_pcl5_testfiles_whql_ft_20_let.py',
' test_pcl5_ufst_jvrtest_nofont.py',
' test_pcl5_utf_8_3_byte_straddles_buffer.py',
' test_pcl5_utf_8_3_byte_utf_8.py',
]
files=[f.strip() for f in files]

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
