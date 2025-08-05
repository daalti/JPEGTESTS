import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a JPG file using attribute value orientation-requested_portrait.
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
    +name:test_ipp_jpg_orientation_requested_portrait
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_jpg_orientation_requested_portrait
        +guid:b3ef44bd-3d6d-410a-ad74-fd59f370fae9
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & MediaSizeSupported=custom

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_jpg_orientation_requested_portrait(setup_teardown, printjob, outputsaver, tray):
    ipp_test_attribs = {'document-format': 'image/jpeg', 'orientation-requested': 3}

    if 'portrait' not in printjob.capabilities.ipp.get('orientation-requested-supported'):
        logging.warning('Device does not support portrait as orientation-requested, setting fidelity to false...')
        ipp_test_attribs['ipp-attribute-fidelity'] = 'false'

    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    default = tray.get_default_source()
    if tray.is_size_supported('custom', default) and tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"] >= 94500:
        # the size of print file should in max/min custom size of printer supported, then could set custom size
        tray.configure_tray(default, "custom", 'stationery')

    printjob.ipp_print(ipp_test_file, '746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc')
    outputsaver.save_output()
    tray.reset_trays()
