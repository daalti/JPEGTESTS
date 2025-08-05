import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a JPG file using attribute value print-scaling_auto-fit.
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
    +name:test_ipp_jpg_print_scaling_auto_fit
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_jpg_print_scaling_auto_fit
        +guid:37d1acaf-1be8-453b-8e91-ccb5edbd6b2a
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & MediaSizeSupported=custom

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_jpg_print_scaling_auto_fit(setup_teardown, printjob, udw, outputsaver, tray):
    outputsaver.validate_crc_tiff(udw)

    ipp_test_attribs = {'document-format': 'image/jpeg', 'scaling': 'auto-fit'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    default = tray.get_default_source()
    if tray.is_size_supported('custom', default) and tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"] >= 94500:
        # the size of print file should in max/min custom size of printer supported, then could set custom size
        tray.configure_tray(default, "custom", 'stationery')

    printjob.ipp_print(ipp_test_file, '746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    tray.reset_trays()
