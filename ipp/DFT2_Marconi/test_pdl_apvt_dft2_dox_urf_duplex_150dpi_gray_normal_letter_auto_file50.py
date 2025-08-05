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
    +external_files:printfile49.urf=f0299f7566e990bccca2fbddb4002b456f50071241ee2674545c7b24fe5eac2c
    +test_classification:System
    +name:test_pdl_apvt_dft2_dox_urf_duplex_150dpi_gray_normal_letter_auto_file50
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_dox_urf_duplex_150dpi_gray_normal_letter_auto_file50
        +guid:bb873ca8-6440-425f-a9a0-f2e34e74979b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & EngineFirmwareFamily=DoX & Duplexer=True & Certifications=AirPrint & MediaInputInstalled=Automatic

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_dox_urf_duplex_150dpi_gray_normal_letter_auto_file50(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('dft2_dox_urf_duplex_150dpi_gray_normal_letter_auto_file50.test', 'f0299f7566e990bccca2fbddb4002b456f50071241ee2674545c7b24fe5eac2c')
    outputsaver.save_output()
