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
    +external_files:printfile61.urf=e93c5e84bab76f8d38ca27f0c36db35562cf080e6d79cf7e686a801d20590001
    +test_classification:System
    +name:test_pdl_apvt_dft2_dox_urf_gray_deviceGray_Duplex_letter_auto_file61
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_dox_urf_gray_deviceGray_Duplex_letter_auto_file61
        +guid:00f59e6f-c1d4-4ddd-982a-5bbea61191b0
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & EngineFirmwareFamily=DoX & Duplexer=True & Certifications=AirPrint & MediaInputInstalled=Automatic

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_dox_urf_gray_deviceGray_Duplex_letter_auto_file61(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('dft2_dox_urf_gray_deviceGray_Duplex_letter_auto_file61.test', 'e93c5e84bab76f8d38ca27f0c36db35562cf080e6d79cf7e686a801d20590001')
    outputsaver.save_output()
