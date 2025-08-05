import sys


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Ipp test for printing a URF file using attribute value page-ranges_3-5
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-47064
    +timeout:250
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:LetterUSVND5p.urf=a381c0d4a54e009d86dfba20d0cc8a2d79f24f2da69e17ed66662bb953d82fbf
    +name:test_ipp_urf_page_ranges_3to5
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_urf_page_ranges_3to5
        +guid:2b7cf03f-c3c4-47bf-ba18-8a75eef31cfc
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & PrintProtocols=IPP
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_ipp_urf_page_ranges_3to5(setup_teardown, printjob, outputsaver, tray):
    tray.reset_trays()
    outputsaver.operation_mode('TIFF')
    ipp_test_attribs = {'document-format': 'image/urf', 'page-ranges': '3-5'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, 'a381c0d4a54e009d86dfba20d0cc8a2d79f24f2da69e17ed66662bb953d82fbf', timeout=200)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
