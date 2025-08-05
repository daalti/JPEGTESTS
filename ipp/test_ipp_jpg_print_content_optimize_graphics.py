import pytest


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a JPG file using attribute value print_content_optimize_graphics
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:broken2.jpg=746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc
    +test_classification:System
    +name:test_ipp_jpg_print_content_optimize_graphics
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_jpg_print_content_optimize_graphics
        +guid:1669f7b0-bbcb-493f-aba6-a0a0d6b37d7e
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & MediaSizeSupported=custom

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_jpg_print_content_optimize_graphics(setup_teardown, printjob, outputsaver, tray):
    ipp_test_attribs = {'document-format': 'image/jpeg', 'print-content-optimize': 'graphics'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    default = tray.get_default_source()
    # file size  Width:240030 & Height:320040 in microns
    if tray.is_size_supported('custom', default) and tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"] >= 94500:
        # the size of print file should in max/min custom size of printer supported, then could set custom size
        tray.configure_tray(default, "custom", 'stationery')

    printjob.ipp_print(ipp_test_file, '746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc')
    outputsaver.save_output()
    tray.reset_trays()
