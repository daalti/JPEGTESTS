import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Ipp test for printing a URF file using attribute value media-type_cardstock
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-47064
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Letter_Color_600.urf=6f574dcc72506c503075530d8e6a9695a466657ddb552ccc4afbab95c54b4c0f
    +name:test_ipp_urf_media_type_cardstock
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_urf_media_type_cardstock
        +guid:1c9cdb2c-f9e6-49be-94a9-f4025f7c3152
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & PrintProtocols=IPP & MediaType=Cardstock

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_urf_media_type_cardstock(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    outputsaver.operation_mode('TIFF')
    if tray.is_size_supported('na_letter_8.5x11in', default) and tray.is_type_supported('cardstock', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'cardstock')

    ipp_test_attribs = {'document-format': 'image/urf', 'media-type': 'cardstock'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '6f574dcc72506c503075530d8e6a9695a466657ddb552ccc4afbab95c54b4c0f')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
