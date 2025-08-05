import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a 1200 URF file using attribute value printquality draft.
    +test_tier:1
    +is_manual:False
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +reqid:DUNE-221028
    +test_framework:TUF
    +external_files:DFT1_Mixed_Gray_DeviceGray.urf=53132fd8c8e7151a893c23a38833de4368fab9d0fcf17c9a57f121a2eda52b7f
    +test_classification:System
    +name:test_ipp_urf_downscaling
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_urf_downscaling
        +guid:6cdfa3c2-6761-4581-9e18-4f1fcd7c383a
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & PrintProtocols=IPP 

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_urf_downscaling(setup_teardown, printjob, outputsaver, tray,cdm,configuration):
    outputsaver.operation_mode('TIFF')
    

    ipp_test_attribs = {'document-format': 'image/urf', 'resolution': '600x600dpi'}
           
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    default = tray.get_default_source()

    printjob.ipp_print(ipp_test_file, '53132fd8c8e7151a893c23a38833de4368fab9d0fcf17c9a57f121a2eda52b7f',timeout=600)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()