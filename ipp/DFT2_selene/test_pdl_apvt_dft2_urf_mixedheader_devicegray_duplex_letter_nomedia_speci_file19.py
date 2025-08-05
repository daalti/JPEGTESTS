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
    +external_files:printfile19.urf=0a025bf8e6bd519c5a39d7cb7fe0bd33caa19a15a7cd23cb78e43e0719a6b9e0
    +test_classification:System
    +name:test_pdl_apvt_dft2_urf_mixedheader_devicegray_duplex_letter_nomedia_speci_file19
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_urf_mixedheader_devicegray_duplex_letter_nomedia_speci_file19
        +guid:11e413df-c463-4165-99eb-5816a41ced21
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & EngineFirmwareFamily=Canon & Certifications=AirPrint
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_urf_mixedheader_devicegray_duplex_letter_nomedia_speci_file19(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('dft2_urf_mixedheader_devicegray_duplex_letter_nomedia_speci_file19.test', '0a025bf8e6bd519c5a39d7cb7fe0bd33caa19a15a7cd23cb78e43e0719a6b9e0')
    outputsaver.save_output()