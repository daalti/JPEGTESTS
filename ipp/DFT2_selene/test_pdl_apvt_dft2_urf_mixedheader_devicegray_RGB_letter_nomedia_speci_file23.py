import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-18912
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:printfile23.urf=f177261fb4c42b5f3e84181769c96db2b6102376df85b5320fbd62187440751f
    +test_classification:System
    +name:test_pdl_apvt_dft2_urf_mixedheader_devicegray_RGB_letter_nomedia_speci_file23
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_urf_mixedheader_devicegray_RGB_letter_nomedia_speci_file23
        +guid:62e04269-e3ed-435c-85fd-9ed76b0f173e
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & EngineFirmwareFamily=Canon & Certifications=AirPrint
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_urf_mixedheader_devicegray_RGB_letter_nomedia_speci_file23(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('dft2_urf_mixedheader_devicegray_RGB_letter_nomedia_speci_file23.test', 'f177261fb4c42b5f3e84181769c96db2b6102376df85b5320fbd62187440751f')
    outputsaver.save_output()