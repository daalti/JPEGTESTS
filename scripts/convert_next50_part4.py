import os
import re
import uuid
import textwrap

src_dir = 'pcl5/pcl5-jedi'
dst_dir = 'pcl5_new/pcl5-jedi'
os.makedirs(dst_dir, exist_ok=True)

files = [
  'test_pcl5_pcl_parsing_deftext2.py',
  'test_pcl5_pcl_parsing_deftext3.py',
  'test_pcl5_pcl_parsing_deftext4.py',
  'test_pcl5_pcl_parsing_deftext5.py',
  'test_pcl5_pcl_parsing_textpars.py',
  'test_pcl5_pcl_parsing_textpars83.py',
  'test_pcl5_pcl_parsing_textpars83_usc2.py',
  'test_pcl5_pcl_pcl_hpgl_effwin2.py',
  'test_pcl5_pcl_pcl_hpgl_gotohpgl.py',
  'test_pcl5_pcl_pcl_hpgl_gotopcl.py',
  'test_pcl5_pcl_pcl_hpgl_hpglsup.py',
  'test_pcl5_pcl_pcl_hpgl_pfancpt2.py',
  'test_pcl5_pcl_pcl_hpgl_pfhoriz2.py',
  'test_pcl5_pcl_pcl_hpgl_pfvert2.py',
  'test_pcl5_pcl_pclcolor_ctfontid.py',
  'test_pcl5_pcl_pclcolor_ctmtrics.py',
  'test_pcl5_pcl_pclcolor_cttfdes.py',
  'test_pcl5_pcl_pclcolor_cttfontm.py',
  'test_pcl5_pcl_pclcolor_cttudssm.py',
  'test_pcl5_pcl_pclcolor_enhlogop.py',
  'test_pcl5_pcl_pclcolor_esc_e_ct.py',
  'test_pcl5_pcl_pclcolor_fallrj.py',
  'test_pcl5_pcl_pclcolor_fgcolor.py',
  'test_pcl5_pcl_pclcolor_finish.py',
  'test_pcl5_pcl_pclcolor_hpgl_rop.py',
  'test_pcl5_pcl_pclcolor_mc.py',
  'test_pcl5_pcl_pclcolor_pc_ct.py',
  'test_pcl5_pcl_pclcolor_pp_ct.py',
  'test_pcl5_pcl_pclcolor_render.py',
  'test_pcl5_pcl_printimageshift_4e_lite_dup.py',
  'test_pcl5_pcl_printimageshift_duplex.py',
  'test_pcl5_pcl_printmod_patcntrl.py',
  'test_pcl5_pcl_printmod_rule5.py',
  'test_pcl5_pcl_printmod_tranmode.py',
  'test_pcl5_pcl_raster_alignjjd.py',
  'test_pcl5_pcl_raster_endrstr.py',
  'test_pcl5_pcl_raster_rasbars_rasbars2.py',
  'test_pcl5_pcl_raster_rasheal.py',
  'test_pcl5_pcl_raster_rastcomp.py',
  'test_pcl5_pcl_raster_rastmode.py',
  'test_pcl5_pcl_raster_rsrcwdth.py',
  'test_pcl5_pcl_rops_basic.py',
  'test_pcl5_pcl_rops_pp.py',
  'test_pcl5_pcl_symset_fmt16sym.py',
  'test_pcl5_pcl_symset_ttudssd.py',
  'test_pcl5_pcl_symset_ttudssm.py',
  'test_pcl5_pcl_symset_ttudssv.py',
  'test_pcl5_pcl_symset_udssman.py',
  'test_pcl5_testfiles_1pageprintfacedown.py',
  'test_pcl5_testfiles_1pageprintfaceup.py',
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
