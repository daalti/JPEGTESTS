import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:printfile55.urf=86c3b078be42caacf7f830435b0f2aaf24403b3d9db92ee936a35607c868a1a2
    +test_classification:System
    +name:test_pdl_apvt_dft2_dox_urf_duplex_150dpi_RGB_normal_letter_auto_file56
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_dox_urf_duplex_150dpi_RGB_normal_letter_auto_file56
        +guid:c40a67d1-32e0-478f-8269-ebffe2142b01
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & EngineFirmwareFamily=DoX & Duplexer=True & Certifications=AirPrint & MediaInputInstalled=Automatic

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_dox_urf_duplex_150dpi_RGB_normal_letter_auto_file56(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('dft2_dox_urf_duplex_150dpi_RGB_normal_letter_auto_file56.test', '86c3b078be42caacf7f830435b0f2aaf24403b3d9db92ee936a35607c868a1a2')
    outputsaver.save_output()
