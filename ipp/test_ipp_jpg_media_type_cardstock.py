import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a JPG file using attribute value media-type_cardstock.
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
    +name:test_ipp_jpg_media_type_cardstock
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_jpg_media_type_cardstock
        +guid:0d476455-9ea6-4f1c-80b9-0bfcd5c0defa
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & MediaType=Cardstock

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_jpg_media_type_cardstock(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_letter_8.5x11in', default) and tray.is_type_supported('cardstock', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'cardstock')

    ipp_test_attribs = {'document-format': 'image/jpeg', 'media-type': 'cardstock'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc')
    outputsaver.save_output()
    tray.reset_trays()
